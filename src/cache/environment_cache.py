import os
import time
from typing import Any, Dict, Tuple, Optional


class EnvironmentCache:
    def __init__(self, ttl: int = 300):
        self._caches: Dict[str, Dict[str, Tuple[float, Any]]] = {}
        self._ttl = ttl

    def _get_env_key(self, environment: Optional[str]) -> str:
        return environment or "active"

    def get(self, environment: Optional[str], key: str) -> Optional[Any]:
        env_key = self._get_env_key(environment)
        if env_key in self._caches and key in self._caches[env_key]:
            timestamp, value = self._caches[env_key][key]
            if time.time() - timestamp < self._ttl:
                return value
            else:
                del self._caches[env_key][key]
        return None

    def set(self, environment: Optional[str], key: str, value: Any) -> None:
        env_key = self._get_env_key(environment)
        if env_key not in self._caches:
            self._caches[env_key] = {}
        self._caches[env_key][key] = (time.time(), value)

    def invalidate(self, environment: Optional[str] = None) -> None:
        if environment:
            env_key = self._get_env_key(environment)
            if env_key in self._caches:
                del self._caches[env_key]
        else:
            self._caches.clear()


global_cache = EnvironmentCache()
