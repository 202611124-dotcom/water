import streamlit as st
import pandas as pd
import numpy as np
import pickle

# 1. 페이지 웹 브라우저 탭 설정 및 와이드 레이아웃 적용
st.set_page_config(
    page_title="Water Mind - 수질 AI 분류",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------
# 2. 파일 불러오기 로직 (캐싱 처리)
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
    scaler, model, train_bounds = load_individual_resources()
except FileNotFoundError:
    st.error("🚨 `scaler.pkl`, `model.pkl`, `train_bounds.pkl` 파일 중 일부가 폴더에 없습니다. 구글 드라이브에서 다운받아 이 스크립트와 같은 폴더에 넣어주세요!")
    st.stop()


# -----------------------------------------------------------------
# 3. 레이아웃 분할 및 UI 디자인
# -----------------------------------------------------------------

# [좌측 사이드바]: 데이터 입력 구역
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1548880338-7416bad859e4?q=80&w=300", use_container_width=True) # 상단 이쁜 물 이미지
    st.markdown("### 🧪 측정 데이터 입력")
    st.write("실측하신 수질 데이터 수치를 입력해 주세요.")
    
    # 세련된 넘버패드 스타일 입력창 (디폴트값 설정)
    ph = st.number_input("📌 pH (산성도)", min_value=0.0, max_value=14.0, value=7.0, step=0.1, help="6.5 ~ 8.5 사이가 식수 적합 기준입니다.")
    hardness = st.number_input("📌 경도 (Hardness)", min_value=0.0, max_value=500.0, value=150.0, step=1.0, help="물에 녹아있는 칼슘과 마그네슘의 총량입니다.")
    solids = st.number_input("📌 총용존고형물 (Solids)", min_value=0.0, max_value=5000.0, value=1000.0, step=10.0, help="물속에 녹아있는 유/무기 물질의 총량입니다.")
    
    st.markdown("---")
    # 사이드바 예측 버튼
    predict_btn = st.button("🚀 수질 분석 시작", use_container_width=True, type="primary")


# [우측 메인 대시보드]: 메인 타이틀 및 결과 출력 구역
st.title("💧 수질 AI 군집 분석 대시보드")
st.markdown("본 시스템은 **K-Means 머신러닝 알고리즘**을 활용하여 입력된 수질 특성을 실시간으로 군집화하고 분석합니다.")
st.write("← 좌측 사이드바에 수치를 입력한 후 **'수질 분석 시작'** 버튼을 눌러주세요.")

if predict_btn:
    # 1. 입력 데이터를 데이터프레임으로 변환
    new_water = pd.DataFrame([[ph, hardness, solids]], columns=['pH(산성도)', '경도', '총용존고형물'])
    
    # 2. 이상치 처리 (Z-Score 상/하한값 클리핑)
    for col in ['pH(산성도)', '경도', '총용존고형물']:
        lower = train_bounds[col]['lower']
        upper = train_bounds[col]['upper']
        new_water[col] = np.where(new_water[col] < lower, lower, new_water[col])
        new_water[col] = np.where(new_water[col] > upper, upper, new_water[col])
        
    # 3. 스케일링 및 모델 예측
    new_water_scaled = scaler.transform(new_water)
    pred_cluster = model.predict(new_water_scaled)[0]
    
    # 디자인 요소: 입력된 값을 상단에 대시보드 카드로 시각화
    st.markdown("### 📊 현재 입력된 데이터 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="입력된 pH", value=f"{ph}")
    col2.metric(label="입력된 경도", value=f"{hardness} mg/L")
    col3.metric(label="입력된 고형물(Solids)", value=f"{solids} ppm")
    
    st.markdown("---")
    st.markdown("### 🎯 AI 모델 분석 결과")
    
    # 군집 결과에 따라 테마 색상 및 카드 디자인 다원화
    if pred_cluster == 2:
        st.success("### 🌱 [군집 2] 가장 평범하고 안전한 일반 수질 영역")
        
        # 내부 레이아웃 분할로 깔끔한 정보 전달
        res_col1, res_col2 = st.columns([1, 2])
        res_col1.markdown("#### 💡 상태 요약\n- **안전성:** 매우 높음\n- **용도:** 생활용수 및 식수 적합")
        res_col2.info("전체 데이터 밀집도가 가장 높은 '정상 영역'의 물입니다. 산성도와 미네랄, 고형물 농도가 치우치지 않고 황금 밸런스를 유지하고 있어 필터링이나 별도의 정수 처리 효율이 가장 좋은 대중적인 수질 상태입니다.")
        
    elif pred_cluster == 0:
        st.warning("### 🔴 [군집 0] 총용존고형물(Solids) 과다 누적 영역")
        
        res_col1, res_col2 = st.columns([1, 2])
        res_col1.markdown("#### 💡 상태 요약\n- **안전성:** 주의 필요\n- **용도:** 공업용수 활용 권장")
        res_col2.error("산점도 상단(빨간색 영역)에 해당하는 수질입니다. 물속에 녹아있는 총 고형물의 양이 지나치게 많아 탁도가 높거나 텁텁한 맛이 날 수 있습니다. 역삼토압(RO) 필터 등을 통한 정밀 고형물 제거 공정이 권장됩니다.")
        
    else:
        st.info("### 🟢 [군집 1] 미네랄 농도가 높은 센물(경수) 영역")
        
        res_col1, res_col2 = st.columns([1, 2])
        res_col1.markdown("#### 💡 상태 요약\n- **안전성:** 보통 (특이 수질)\n- **용도:** 마그네슘/칼슘 풍부 광천수")
        res_col2.warning("산점도 우측 하단(초록색 영역)에 해당하는 수질입니다. 고형물 농도는 낮으나 칼슘과 마그네슘 같은 미네랄 성분이 매우 강합니다. 보일러나 배관에 물때(스케일)를 유발할 수 있으므로 연수기 사용을 고려해 볼 수 있습니다.")

else:
    # 버튼을 누르기 전 첫 화면 가이드 뷰 디자인
    st.info("💡 위의 입력 데이터 요약 카드는 사이드바에서 값을 입력하고 분석 버튼을 누르면 실시간으로 갱신됩니다.")
