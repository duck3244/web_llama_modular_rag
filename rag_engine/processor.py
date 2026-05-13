import gc
import time
import streamlit as st

from graph_builder import build_rag_graph
from data_loader import create_vectorstore_from_pdf, get_cache_key
from st_components.memory import print_memory_usage, cleanup_memory


def run_optimized_rag(pdf_path, query):
    """CPU에 최적화된 RAG 시스템을 실행합니다."""
    start_time = time.time()

    with st.spinner("처리 중..."):
        pdf_key = get_cache_key(pdf_path)
        st.info(f"시작 시점 메모리 사용량: {print_memory_usage()}")

        cached_result = st.session_state.query_cache.get_cached_result(query, pdf_key)
        if cached_result:
            st.success("캐시된 결과를 사용합니다.")
            elapsed_time = time.time() - start_time
            st.session_state.processing_time = elapsed_time
            st.info(f"처리 소요 시간 (캐시): {elapsed_time:.2f}초 | 메모리 사용량: {print_memory_usage()}")
            return cached_result

        if st.session_state.vectorstore is None or st.session_state.pdf_path != pdf_path:
            with st.spinner(f"PDF 처리 중: {pdf_path}"):
                st.session_state.vectorstore = create_vectorstore_from_pdf(pdf_path)
                st.session_state.pdf_path = pdf_path
                st.session_state.rag_graph = None  # 새 PDF일 땐 그래프도 재구축
                gc.collect()
                st.info(f"벡터 저장소 생성 후 메모리 사용량: {print_memory_usage()}")

        if st.session_state.rag_graph is None:
            with st.spinner("RAG 그래프 구축 중..."):
                st.session_state.rag_graph = build_rag_graph(st.session_state.vectorstore)

        with st.spinner(f"쿼리 처리 중: '{query}'"):
            result = st.session_state.rag_graph.invoke({"query": query})

        st.session_state.query_cache.cache_result(query, result, pdf_key)

        elapsed_time = time.time() - start_time
        st.session_state.processing_time = elapsed_time
        st.info(f"총 처리 소요 시간: {elapsed_time:.2f}초 | 최종 메모리 사용량: {print_memory_usage()}")

        cleanup_memory()
        return result
