from typing import List

import streamlit as st
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer, models

from config import EMBEDDING_MODEL_NAME, DEVICE


def _build_st_model(model_name: str, device: str) -> SentenceTransformer:
    """sentence-transformers 2.5.x에는 SentenceTransformer(model_kwargs=...)가 없으므로
    내부 models.Transformer를 직접 만들어 use_safetensors=True를 주입한다.
    (transformers 4.49+ / torch <2.6 환경에서 .bin 로드가 CVE-2025-32434로 차단되는 문제 회피)
    """
    word_emb = models.Transformer(
        model_name,
        model_args={"use_safetensors": True},
    )
    pooling = models.Pooling(
        word_emb.get_word_embedding_dimension(),
        pooling_mode_mean_tokens=True,
    )
    return SentenceTransformer(modules=[word_emb, pooling], device=device)


class SafeTensorsHFEmbeddings(Embeddings):
    """Chroma/langchain용 Embeddings 인터페이스 래퍼."""

    def __init__(self, model_name: str, device: str = "cpu", batch_size: int = 8):
        self.model = _build_st_model(model_name, device)
        self.batch_size = batch_size

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        vectors = self.model.encode(
            [t.replace("\n", " ") for t in texts],
            batch_size=self.batch_size,
            normalize_embeddings=True,
        )
        return vectors.tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


@st.cache_resource(show_spinner="임베딩 모델 로드 중...")
def get_embedding_model():
    """세션당 1회만 로드되는 임베딩 모델"""
    return SafeTensorsHFEmbeddings(EMBEDDING_MODEL_NAME, device=DEVICE)
