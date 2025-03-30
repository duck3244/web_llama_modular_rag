import os
import streamlit as st

from config import CACHE_DIR
from caching import QueryCache


def init_session_state():
    """Streamlit 앱의 세션 상태를 초기화합니다."""
    # 쿼리 캐시 초기화
    if 'query_cache' not in st.session_state:
        os.makedirs(CACHE_DIR, exist_ok=True)
        st.session_state.query_cache = QueryCache()

    # 벡터스토어 초기화
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None

    # RAG 그래프 초기화
    if 'rag_graph' not in st.session_state:
        st.session_state.rag_graph = None

    # PDF 경로 초기화
    if 'pdf_path' not in st.session_state:
        st.session_state.pdf_path = None

    # 결과 초기화
    if 'result' not in st.session_state:
        st.session_state.result = None

    # 처리 시간 초기화
    if 'processing_time' not in st.session_state:
        st.session_state.processing_time = None

    # 메모리 사용량 초기화
    if 'memory_usage' not in st.session_state:
        st.session_state.memory_usage = []
