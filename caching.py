import os
import pickle
import hashlib

from config import CACHE_DIR


class QueryCache:
    """쿼리 + PDF 조합 기반 결과 캐싱"""

    def __init__(self, cache_dir=CACHE_DIR):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_cache_key(self, query, pdf_key=""):
        return hashlib.md5(f"{pdf_key}::{query}".encode()).hexdigest()

    def get_cached_result(self, query, pdf_key=""):
        cache_path = os.path.join(self.cache_dir, f"{self.get_cache_key(query, pdf_key)}.pkl")
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None

    def cache_result(self, query, result, pdf_key=""):
        cache_path = os.path.join(self.cache_dir, f"{self.get_cache_key(query, pdf_key)}.pkl")
        with open(cache_path, 'wb') as f:
            pickle.dump(result, f)