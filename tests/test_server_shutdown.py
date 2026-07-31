"""Regression tests for the MCP server's shutdown lifecycle.

These spawn the real server entry point (``python -m src.server``) and assert
that it terminates cleanly when an agent disconnects (stdin EOF) or when a
termination signal is delivered. They guard against the historic defect where
SIGINT/SIGTERM left the process wedged because the blocked stdin read runs in
a non-cancellable anyio worker thread.
"""
import json
import os
import signal
import subprocess
import sys
import threading
import time

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON = sys.executable
_IS_WINDOWS = sys.platform.startswith("win")


def _handshake(proc):
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"},
        },
    }
    # Drain stdout on a background thread so the server never blocks on a full
    # pipe, and collect lines so we can confirm it actually came up.
    responses = []

    def _drain():
        for line in proc.stdout:
            responses.append(line)

    threading.Thread(target=_drain, daemon=True).start()
    proc.stdin.write(json.dumps(init_req) + "\n")
    proc.stdin.flush()
    proc.stdin.write(
        json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"
    )
    proc.stdin.flush()
    deadline = time.time() + 5
    while time.time() < deadline and proc.poll() is None:
        if any('"protocolVersion"' in r for r in responses):
            break
        time.sleep(0.02)
    assert any(
        '"protocolVersion"' in r for r in responses
    ), "server did not respond to initialize request"


def _spawn():
    return subprocess.Popen(
        [PYTHON, "-m", "src.server"],
        cwd=REPO_ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )


def _wait_exit(proc, timeout=8):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            return True
        time.sleep(0.02)
    return False


def _finalize(proc):
    try:
        proc.stdin.close()
    except Exception:
        pass
    if proc.poll() is None:
        proc.kill()
        proc.wait()


@pytest.mark.skipif(_IS_WINDOWS, reason="POSIX signal semantics required")
@pytest.mark.parametrize("sig", [signal.SIGINT, signal.SIGTERM])
def test_server_shuts_down_on_signal(sig):
    proc = _spawn()
    try:
        _handshake(proc)
        proc.send_signal(sig)
        assert _wait_exit(proc, timeout=6), "server did not exit after signal"
        assert proc.returncode == 0
        err = proc.stderr.read()
        assert err == "", f"unexpected stderr on shutdown: {err!r}"
    finally:
        _finalize(proc)


def test_server_shuts_down_on_stdin_eof():
    proc = _spawn()
    try:
        _handshake(proc)
        proc.stdin.close()
        assert _wait_exit(proc, timeout=6), "server did not exit on stdin EOF"
        assert proc.returncode == 0
        err = proc.stderr.read()
        assert err == "", f"unexpected stderr on shutdown: {err!r}"
    finally:
        _finalize(proc)


@pytest.mark.skipif(_IS_WINDOWS, reason="POSIX signal semantics required")
def test_server_exits_immediately_on_second_signal():
    proc = _spawn()
    try:
        _handshake(proc)
        proc.send_signal(signal.SIGINT)
        time.sleep(0.2)
        proc.send_signal(signal.SIGINT)
        assert _wait_exit(proc, timeout=5), "server did not exit after second signal"
        assert proc.returncode == 0
    finally:
        _finalize(proc)
