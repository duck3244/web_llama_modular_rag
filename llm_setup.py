import torch
import streamlit as st

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from config import LLAMA_MODEL_PATH, DEVICE, TEMPERATURE, MAX_NEW_TOKENS


@st.cache_resource(show_spinner="LLM 로드 중...")
def setup_llama_model():
    """세션당 1회만 로드되는 Llama 모델"""
    tokenizer = AutoTokenizer.from_pretrained(LLAMA_MODEL_PATH)

    model = AutoModelForCausalLM.from_pretrained(
        LLAMA_MODEL_PATH,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
        device_map=DEVICE,
    )
    model.eval()

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        repetition_penalty=1.1,
        batch_size=1,
    )

    return HuggingFacePipeline(pipeline=pipe)