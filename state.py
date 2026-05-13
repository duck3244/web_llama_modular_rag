from langchain_core.documents import Document
from typing import TypedDict, List, Optional


class RAGState(TypedDict):
    """RAG 파이프라인의 상태"""
    query: str
    documents: Optional[List[Document]]
    context: Optional[str]
    answer: Optional[str]