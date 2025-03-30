import gc
import time
import streamlit as st

from graph_builder import build_rag_graph
from data_loader import create_vectorstore_from_pdf
from st_components.memory import print_memory_usage, cleanup_memory


def run_optimized_rag(pdf_path, query):
    """CPU에 최적화된 RAG 시스템을 실행합니다."""
    start_time = time.time()
    
    with st.spinner("처리 중..."):
        initial_memory = print_memory_usage()
        st.info(f"시작 시점 메모리 사용량: {initial_memory}")
        
        # 이전 결과 캐시 확인
        cached_result = st.session_state.query_cache.get_cached_result(query)
        if cached_result:
            st.success("캐시된 결과를 사용합니다.")
            elapsed_time = time.time() - start_time
            st.session_state.processing_time = elapsed_time
            current_memory = print_memory_usage()
            st.info(f"처리 소요 시간 (캐시): {elapsed_time:.2f}초 | 메모리 사용량: {current_memory}")
            return cached_result
        
        # 벡터 저장소 생성 또는 불러오기
        if st.session_state.vectorstore is None or st.session_state.pdf_path != pdf_path:
            with st.spinner(f"PDF 처리 중: {pdf_path}"):
                st.session_state.vectorstore = create_vectorstore_from_pdf(pdf_path)
                st.session_state.pdf_path = pdf_path
                
                # 중간 메모리 정리
                gc.collect()
                vector_store_memory = print_memory_usage()
                st.info(f"벡터 저장소 생성 후 메모리 사용량: {vector_store_memory}")
        
        # RAG 그래프 구축
        if st.session_state.rag_graph is None:
            with st.spinner("RAG 그래프 구축 중..."):
                st.session_state.rag_graph = build_rag_graph(st.session_state.vectorstore)
        
        # 초기 상태 설정
        initial_state = {"query": query}
        
        # 그래프 실행
        with st.spinner(f"쿼리 처리 중: '{query}'"):
            result = st.session_state.rag_graph.invoke(initial_state)
        
        # 결과 캐싱
        with st.spinner("결과 캐싱 중..."):
            st.session_state.query_cache.cache_result(query, result)
        
        # 소요 시간 계산
        elapsed_time = time.time() - start_time
        st.session_state.processing_time = elapsed_time
        
        # 최종 메모리 사용량
        final_memory = print_memory_usage()
        st.info(f"총 처리 소요 시간: {elapsed_time:.2f}초 | 최종 메모리 사용량: {final_memory}")
        
        # 메모리 정리
        cleanup_memory()
        
        return result
