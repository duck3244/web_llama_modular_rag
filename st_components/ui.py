import streamlit as st


def setup_ui():
    """Streamlit UI의 기본 스타일을 설정합니다."""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E88E5;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #424242;
        }
        .info-text {
            font-size: 1rem;
            color: #616161;
        }
        .highlight {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
        }
        .memory-info {
            font-size: 0.9rem;
            color: #616161;
        }
    </style>
    """, unsafe_allow_html=True)


def display_results():
    """결과를 표시합니다."""
    result_container = st.container()
    
    with result_container:
        st.markdown('<div class="highlight">', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">Q: {st.session_state.result["query"]}</p>', unsafe_allow_html=True)
        
        if "answer" in st.session_state.result and st.session_state.result["answer"]:
            st.markdown(f'<p class="info-text">A: {st.session_state.result["answer"]}</p>', unsafe_allow_html=True)
        else:
            st.warning("응답을 생성할 수 없습니다.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 참조 문서 표시 (확장 가능)
        if "documents" in st.session_state.result and st.session_state.result["documents"]:
            with st.expander("참조 문서 보기"):
                for i, doc in enumerate(st.session_state.result["documents"][:2]):
                    st.markdown(f"**문서 {i + 1}**")
                    st.markdown(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
                    st.divider()


def render_instructions():
    """사용 안내를 표시합니다."""
    st.markdown("""
    ## 시스템 사용 방법
    1. 왼쪽 사이드바에서 PDF 문서를 업로드하세요.
    2. 상단 입력창에 질문을 입력하세요.
    3. '검색' 버튼을 클릭하여 답변을 받으세요.
    
    ### 예시 질문
    - 명동에 처음 온 외국인 관광객이 가볼만한 장소를 알려줘?
    - 중구 지역의 역사적 명소는 어디인가요?
    - 서울에서 쇼핑하기 좋은 곳을 추천해주세요.
    """)
