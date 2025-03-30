import os
import gc
import time
import streamlit as st

from st_components.session import init_session_state
from st_components.memory import print_memory_usage, init_memory_tracking
from st_components.ui import setup_ui, display_results, render_instructions
from st_components.visualization import visualize_graph, display_memory_chart

from rag_engine.processor import run_optimized_rag

from config import CACHE_DIR

# 페이지 설정
st.set_page_config(
    page_title="RAG 시스템",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# UI 스타일 설정
setup_ui()

# 세션 상태 초기화
init_session_state()

# 메모리 트래킹 초기화
init_memory_tracking()

# 사이드바 : 파일 업로드 및 시스템 정보
with st.sidebar:
    st.markdown('<p class="sub-header">📁 PDF 문서 업로드</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        # 업로드된 파일 저장
        pdf_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"업로드 완료: {uploaded_file.name}")
    else:
        st.info("PDF 파일을 업로드하면 RAG 시스템이 준비됩니다.")
        pdf_path = None
    
    st.divider()
    
    st.markdown('<p class="sub-header">⚙️ 시스템 정보</p>', unsafe_allow_html=True)
    st.markdown('<p class="memory-info">현재 메모리 사용량: ' + print_memory_usage() + '</p>', unsafe_allow_html=True)
    
    if st.session_state.processing_time is not None:
        st.markdown(f'<p class="memory-info">최근 처리 시간: {st.session_state.processing_time:.2f}초</p>', unsafe_allow_html=True)
    
    # 메모리 사용량 그래프
    if len(st.session_state.memory_usage) > 1:
        display_memory_chart()
    
    # RAG 그래프 시각화
    st.markdown('<p class="sub-header">🔄 RAG 파이프라인</p>', unsafe_allow_html=True)
    graph_image = visualize_graph()
    if graph_image:
        st.image(graph_image, caption="RAG 워크플로우", use_column_width=True)


# 메인 화면
st.markdown('<p class="main-header">📚 한국어 RAG 시스템</p>', unsafe_allow_html=True)
st.markdown('<p class="info-text">PDF 문서에서 정보를 검색하고 질문에 답변합니다.</p>', unsafe_allow_html=True)

# 질문 입력
query = st.text_input("질문을 입력하세요", value="", key="query_input", 
                    placeholder="예: 명동에 처음 온 외국인 관광객이 가볼만한 장소를 알려줘?")

# 실행 버튼
col1, col2 = st.columns([1, 5])
with col1:
    search_button = st.button("검색", key="search_button", type="primary", use_container_width=True)
with col2:
    st.empty()

# 질문 처리 및 결과 표시
if search_button and query and pdf_path:
    st.session_state.result = run_optimized_rag(pdf_path, query)
    display_results()
    
elif search_button and not pdf_path:
    st.error("PDF 파일을 먼저 업로드해주세요.")
elif search_button and not query:
    st.error("질문을 입력해주세요.")
elif st.session_state.result is not None:
    # 이전 결과 유지
    display_results()

# 사용 안내
if not st.session_state.result:
    render_instructions()

# 푸터
st.markdown("---")
st.markdown('<p class="memory-info">RAG(Retrieval-Augmented Generation) 시스템 - CPU 최적화 버전</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    # 필요한 디렉토리 생성
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    os.makedirs("vector_db", exist_ok=True)
