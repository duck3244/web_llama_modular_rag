import os
import psutil
import streamlit as st


def init_memory_tracking():
    """메모리 트래킹 관련 상태를 초기화합니다."""
    if 'memory_usage' not in st.session_state:
        st.session_state.memory_usage = []


def print_memory_usage():
    """현재 메모리 사용량을 측정하고 반환합니다."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    usage_mb = memory_info.rss / 1024 / 1024
    
    # 세션 상태에 메모리 사용량 기록
    if 'memory_usage' in st.session_state:
        st.session_state.memory_usage.append(usage_mb)
    
    return f"{usage_mb:.2f} MB"


def get_memory_trend():
    """메모리 사용량 추이 데이터를 반환합니다."""
    if 'memory_usage' not in st.session_state or len(st.session_state.memory_usage) <= 1:
        return None
    
    x = list(range(len(st.session_state.memory_usage)))
    y = st.session_state.memory_usage
    
    return x, y


def cleanup_memory():
    """메모리 정리 작업을 수행합니다."""
    import gc
    gc.collect()
    return print_memory_usage()
