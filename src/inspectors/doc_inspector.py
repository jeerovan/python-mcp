import pydoc
import math
import re
from collections import Counter
from typing import Any, Dict, List


class DocumentationInspector:
    @staticmethod
    def search_docs(query: str) -> Dict[str, Any]:
        """Searches for module/package documentation using pydoc."""
        try:
            doc = pydoc.render_doc(query)
            return {"query": query, "documentation": doc}
        except Exception as e:
            return {"query": query, "error": str(e)}

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    @staticmethod
    def _tf(tokens: List[str]) -> Dict[str, float]:
        counts = Counter(tokens)
        total = len(tokens) or 1
        return {term: freq / total for term, freq in counts.items()}

    @staticmethod
    def _cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        common = set(vec_a) & set(vec_b)
        dot = sum(vec_a[t] * vec_b[t] for t in common)
        mag_a = math.sqrt(sum(v * v for v in vec_a.values())) or 1
        mag_b = math.sqrt(sum(v * v for v in vec_b.values())) or 1
        return dot / (mag_a * mag_b)

    @staticmethod
    def semantic_search(query: str, top_k: int = 5) -> Dict[str, Any]:
        """Semantic search over rendered module documentation.

        Candidate corpus built from importable top-level modules.
        TF cosine similarity used as ranking score.
        """
        import pkgutil
        candidates: List[Dict[str, Any]] = []
        query_tokens = DocumentationInspector._tokenize(query)
        query_vec = DocumentationInspector._tf(query_tokens)

        for mod_info in pkgutil.iter_modules():
            name = mod_info.name
            try:
                doc = pydoc.render_doc(name)
                tokens = DocumentationInspector._tokenize(doc)
                vec = DocumentationInspector._tf(tokens)
                score = DocumentationInspector._cosine_similarity(query_vec, vec)
                candidates.append({
                    "module": name,
                    "score": score,
                    "documentation": doc[:500],
                })
            except Exception:
                continue

        candidates.sort(key=lambda c: c["score"], reverse=True)
        return {
            "query": query,
            "top_k": top_k,
            "results": candidates[:top_k],
        }
