import streamlit as st
import plotly.graph_objects as go

from PIL import Image
from graphviz import Digraph

from st_components.memory import get_memory_trend


def visualize_graph():
    """RAG 그래프 구조를 시각화하여 이미지로 반환합니다."""
    try:
        # 직접 그래프 내용 작성
        dot = Digraph(comment='RAG Pipeline')

        # 노드 추가
        dot.node('start', 'Start', shape='ellipse')
        dot.node('doc_retriever', '문서 검색', shape='box')
        dot.node('context_builder', '컨텍스트 생성', shape='box')
        dot.node('answer_generator', '답변 생성', shape='box')
        dot.node('end', 'End', shape='ellipse')

        # 엣지 추가
        dot.edge('start', 'doc_retriever')
        dot.edge('doc_retriever', 'context_builder')
        dot.edge('context_builder', 'answer_generator')
        dot.edge('answer_generator', 'end')

        # 임시 파일로 저장
        temp_path = "temp_graph"
        dot.render(temp_path, format="png", cleanup=True)
        
        # 이미지 로드
        image = Image.open(f"{temp_path}.png")
        return image
        
    except Exception as e:
        st.error(f"그래프 시각화 중 오류가 발생했습니다: {str(e)}")
        return None


def display_memory_chart():
    """메모리 사용량 추이 차트를 표시합니다."""
    memory_data = get_memory_trend()
    
    if not memory_data:
        return
        
    x, y = memory_data
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name='메모리 사용량'
    ))
    
    fig.update_layout(
        title="메모리 사용량 추이",
        xaxis_title="실행 단계",
        yaxis_title="메모리 (MB)",
        height=250,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
