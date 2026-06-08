import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="수질 군집 예측 시스템", layout="centered")
st.title("💧 수질 데이터 기반 군집 예측 시스템")

# -----------------------------------------------------------------
# [수정] 각각 따로 분리된 3개의 파일 불러오기
# -----------------------------------------------------------------
@st.cache_resource
def load_individual_resources():
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('train_bounds.pkl', 'rb') as f:
        train_bounds = pickle.load(f)
    return scaler, model, train_bounds

try:
    # 3개의 파일에서 각각 객체를 읽어옵니다.
    scaler, model, train_bounds = load_individual_resources()
except FileNotFoundError:
    st.error("🚨 'scaler.pkl', 'model.pkl', 'train_bounds.pkl' 파일 중 일부가 없습니다. 파일 위치를 확인해주세요!")
    st.stop()

# (이후 입력 UI 및 예측 버튼 로직은 이전 코드와 완벽히 동일합니다!)
