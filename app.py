import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ─────────────────────────────────────────────
# 1. 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Water Mind · 수질 AI 분석",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# 2. 글로벌 CSS — Lab White 컨셉
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── 리셋 & 전체 배경 ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.main, .block-container {
    background-color: #F2F5F8 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #0B1929 !important;
}

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] label {
    color: #0B1929 !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em {
    color: #0B1929 !important;
}

/* ── 사이드바 ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background: #0B1929 !important;
    border-right: none !important;
}

[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] label {
    color: #C9D8E8 !important;
    background-color: transparent !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #4A6680 !important;
}

/* 사이드바 브랜드 */
.sidebar-brand {
    padding: 2rem 0 1.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 1.6rem;
}
.sidebar-wordmark {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 400;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #3A7BD5 !important;
    margin: 0 0 0.5rem;
}
.sidebar-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #EAF1F8 !important;
    margin: 0;
    letter-spacing: -0.4px;
    line-height: 1.2;
}
.sidebar-subtitle {
    font-size: 0.78rem;
    color: #3A5A78 !important;
    margin: 0.35rem 0 0;
    line-height: 1.4;
}

/* 사이드바 구분 헤더 */
.sidebar-section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2A4A60 !important;
    margin: 1.4rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.sidebar-section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.07);
}

/* 입력 필드 */
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #EAF1F8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    padding: 0.55rem 0.8rem !important;
    transition: border-color 0.15s, box-shadow 0.15s;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #3A7BD5 !important;
    box-shadow: 0 0 0 3px rgba(58,123,213,0.18) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #3A5A78 !important;
}
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.08) !important;
    color: #6A8FAA !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(58,123,213,0.2) !important;
    color: #EAF1F8 !important;
}

/* 분석 버튼 */
[data-testid="stButton"] > button[kind="primary"] {
    background: #3A7BD5 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1rem !important;
    transition: background 0.15s, transform 0.1s !important;
    box-shadow: 0 2px 16px rgba(58,123,213,0.3) !important;
    margin-top: 0.5rem;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #2D68BE !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(58,123,213,0.45) !important;
}
[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ── 메인 영역 타이틀 ── */
.page-header {
    padding: 2.8rem 0 2rem;
    border-bottom: 1px solid #D8E2EC;
    margin-bottom: 2rem;
}
.header-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #3A7BD5;
    margin-bottom: 0.8rem;
}
.header-title {
    font-family: 'DM Sans', sans-serif;
    font-size: clamp(1.8rem, 3vw, 2.8rem);
    font-weight: 700;
    color: #0B1929;
    letter-spacing: -1.2px;
    line-height: 1.1;
    margin: 0 0 0.8rem;
}
.header-title em {
    font-style: normal;
    color: #3A7BD5;
}
.header-desc {
    font-size: 0.92rem;
    color: #4A6680;
    line-height: 1.65;
    max-width: 500px;
    font-weight: 400;
}

/* ── 메트릭 패널 ── */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #DDE7F0 !important;
    border-radius: 12px !important;
    padding: 1.1rem 1.3rem !important;
    box-shadow: 0 1px 4px rgba(11,25,41,0.06) !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    font-family: 'DM Mono', monospace !important;
    color: #7A97B2 !important;
    font-size: 0.65rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #0B1929 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.55rem !important;
    font-weight: 500 !important;
    letter-spacing: -0.5px !important;
}
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] div {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    color: #3A7BD5 !important;
}

/* ── 결과 카드 ── */
.result-wrap {
    margin-top: 2rem;
}
.result-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 2rem 2.2rem 1.8rem;
    border: 1px solid #DDE7F0;
    box-shadow: 0 2px 12px rgba(11,25,41,0.06);
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
}
.result-card-safe::before    { background: #22C55E; }
.result-card-danger::before  { background: #EF4444; }
.result-card-mineral::before { background: #3A7BD5; }

.result-status-row {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 1.1rem;
}
.status-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-safe    { background: #22C55E; box-shadow: 0 0 0 3px rgba(34,197,94,0.18); }
.dot-danger  { background: #EF4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.18); }
.dot-mineral { background: #3A7BD5; box-shadow: 0 0 0 3px rgba(58,123,213,0.18); }

.status-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}
.label-safe    { color: #16A34A; }
.label-danger  { color: #DC2626; }
.label-mineral { color: #2563EB; }

.result-heading {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #0B1929;
    letter-spacing: -0.5px;
    margin: 0 0 0.65rem;
    line-height: 1.2;
}
.result-body {
    font-size: 0.9rem;
    color: #4A6680;
    line-height: 1.75;
    max-width: 640px;
    margin: 0;
}

/* 태그 */
.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 1.4rem;
    padding-top: 1.2rem;
    border-top: 1px solid #EEF3F8;
}
.tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    padding: 0.25rem 0.7rem;
    border-radius: 4px;
    font-weight: 400;
}
.tag-green   { background: #F0FDF4; color: #15803D; border: 1px solid #BBF7D0; }
.tag-red     { background: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; }
.tag-blue    { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }

/* ── pH 스펙트럼 바 (시그니처 요소) ── */
.ph-spectrum-wrap {
    background: #FFFFFF;
    border: 1px solid #DDE7F0;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-top: 1.8rem;
    box-shadow: 0 1px 4px rgba(11,25,41,0.05);
}
.spectrum-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7A97B2;
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.spectrum-label span {
    font-size: 0.85rem;
    letter-spacing: -0.2px;
    color: #0B1929 !important;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
}
.ph-bar-track {
    height: 14px;
    border-radius: 7px;
    background: linear-gradient(to right,
        #EF4444 0%,
        #F97316 10%,
        #FACC15 20%,
        #A3E635 30%,
        #4ADE80 40%,
        #22C55E 50%,
        #34D399 55%,
        #67E8F9 65%,
        #60A5FA 75%,
        #818CF8 85%,
        #A855F7 100%
    );
    position: relative;
    margin-bottom: 0.5rem;
}
.ph-bar-pointer {
    position: absolute;
    top: -4px;
    width: 22px;
    height: 22px;
    background: #FFFFFF;
    border: 2.5px solid #0B1929;
    border-radius: 50%;
    transform: translateX(-50%);
    box-shadow: 0 2px 8px rgba(11,25,41,0.2);
    transition: left 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.ph-bar-ticks {
    display: flex;
    justify-content: space-between;
    padding: 0 0;
    margin-top: 0.4rem;
}
.ph-tick {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #9AB4C8;
    text-align: center;
}
.ph-zone-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.3rem;
}
.ph-zone-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.ph-zone-acid   { color: #EF4444; }
.ph-zone-normal { color: #22C55E; text-align: center; flex: 1; }
.ph-zone-alka   { color: #818CF8; text-align: right; }

/* ── 경고 아이템 ── */
.alert-section-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7A97B2;
    margin: 2.2rem 0 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.alert-section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #DDE7F0;
}
.alert-list {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}
.alert-item {
    display: grid;
    grid-template-columns: 2.2rem 1fr;
    gap: 0;
    background: #FFFFFF;
    border: 1px solid #DDE7F0;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(11,25,41,0.04);
}
.alert-stripe {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}
.stripe-warn   { background: #FFFBEB; border-right: 1px solid #FDE68A; }
.stripe-danger { background: #FEF2F2; border-right: 1px solid #FECACA; }
.stripe-info   { background: #EFF6FF; border-right: 1px solid #BFDBFE; }
.alert-content {
    padding: 0.75rem 1rem;
}
.alert-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.83rem;
    font-weight: 600;
    color: #0B1929 !important;
    margin-bottom: 0.2rem;
}
.alert-desc {
    font-size: 0.78rem;
    color: #4A6680 !important;
    line-height: 1.55;
}

/* ── 빈 화면 가이드 ── */
.guide-panel {
    background: #FFFFFF;
    border: 1px dashed #C5D5E4;
    border-radius: 16px;
    padding: 3.5rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
}
.guide-monogram {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.25em;
    color: #9AB4C8;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.guide-heading {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #1E3448;
    margin-bottom: 0.5rem;
    letter-spacing: -0.3px;
}
.guide-text {
    font-size: 0.85rem;
    color: #7A97B2;
    line-height: 1.65;
    max-width: 380px;
    margin: 0 auto;
}
.guide-arrow {
    display: inline-block;
    margin-top: 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3A7BD5;
    border: 1px solid #BFDBFE;
    border-radius: 4px;
    padding: 0.3rem 0.8rem;
    background: #EFF6FF;
}

/* 섹션 헤더 */
.section-heading {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7A97B2;
    margin: 0 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #DDE7F0;
}

/* 숨김 */
#MainMenu, footer, header { visibility: hidden; }
hr { border-color: #DDE7F0 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F2F5F8; }
::-webkit-scrollbar-thumb { background: #C5D5E4; border-radius: 3px; }
[data-testid="stTooltipIcon"] { color: #9AB4C8 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 3. 리소스 로드
# ─────────────────────────────────────────────
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
    st.error("🚨 `scaler.pkl`, `model.pkl`, `train_bounds.pkl` 파일이 없습니다. 스크립트와 같은 폴더에 넣어주세요.")
    st.stop()


# ─────────────────────────────────────────────
# 4. 사이드바
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <p class="sidebar-wordmark">수질 AI 분석 시스템</p>
        <h1 class="sidebar-title">Water<br>Mind</h1>
        <p class="sidebar-subtitle">K-Means 머신러닝 기반<br>실시간 수질 특성 분류</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section-label">측정 데이터 입력</p>', unsafe_allow_html=True)

    ph       = st.number_input("pH  — 산성도",          min_value=0.0,  max_value=14.0,   value=7.0,    step=0.1,  help="식수 적합 기준: 6.5 ~ 8.5")
    hardness = st.number_input("Hardness  — 경도",       min_value=0.0,  max_value=500.0,  value=150.0,  step=1.0,  help="칼슘·마그네슘 총량 (mg/L)")
    solids   = st.number_input("Solids  — 총용존고형물", min_value=0.0,  max_value=5000.0, value=1000.0, step=10.0, help="용해된 유·무기 물질 총량 (ppm)")

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    predict_btn = st.button("분석 실행", use_container_width=True, type="primary")

    st.markdown("---")
    st.caption("입력값은 저장되지 않으며 분석은 즉시 수행됩니다.")


# ─────────────────────────────────────────────
# 5. 메인 영역
# ─────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <p class="header-eyebrow">Water Quality Analysis · AI-Powered</p>
    <h1 class="header-title">지금 이 물,<br><em>어떤 상태인가요?</em></h1>
    <p class="header-desc">
        pH·경도·총용존고형물 세 수치를 입력하면
        AI가 수질 유형을 즉시 분류하고 사용 가능 여부를 알려드립니다.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 6. 결과 렌더링
# ─────────────────────────────────────────────
if predict_btn:

    # 전처리 & 예측
    new_water = pd.DataFrame(
        [[ph, hardness, solids]],
        columns=['pH(산성도)', '경도', '총용존고형물']
    )
    for col in ['pH(산성도)', '경도', '총용존고형물']:
        lower = train_bounds[col]['lower']
        upper = train_bounds[col]['upper']
        new_water[col] = np.clip(new_water[col], lower, upper)

    new_water_scaled = scaler.transform(new_water)
    pred_cluster = model.predict(new_water_scaled)[0]

    # 입력값 요약
    st.markdown('<p class="section-heading">입력된 수질 데이터</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("pH — 산성도",    f"{ph:.1f}",          delta="기준 6.5 ~ 8.5")
    c2.metric("경도 (mg/L)",    f"{hardness:.0f}")
    c3.metric("총용존고형물 (ppm)", f"{solids:.0f}")

    # pH 스펙트럼 바 (시그니처)
    ph_pct = (ph / 14.0) * 100
    st.markdown(f"""
    <div class="ph-spectrum-wrap">
        <div class="spectrum-label">
            pH 스펙트럼 위치
            <span>{ph:.1f}</span>
        </div>
        <div class="ph-bar-track">
            <div class="ph-bar-pointer" style="left:{ph_pct}%"></div>
        </div>
        <div class="ph-bar-ticks">
            <span class="ph-tick">0</span>
            <span class="ph-tick">1</span>
            <span class="ph-tick">2</span>
            <span class="ph-tick">3</span>
            <span class="ph-tick">4</span>
            <span class="ph-tick">5</span>
            <span class="ph-tick">6</span>
            <span class="ph-tick">7</span>
            <span class="ph-tick">8</span>
            <span class="ph-tick">9</span>
            <span class="ph-tick">10</span>
            <span class="ph-tick">11</span>
            <span class="ph-tick">12</span>
            <span class="ph-tick">13</span>
            <span class="ph-tick">14</span>
        </div>
        <div class="ph-zone-labels">
            <span class="ph-zone-label ph-zone-acid">산성</span>
            <span class="ph-zone-label ph-zone-normal">중성 (식수 적합 구간)</span>
            <span class="ph-zone-label ph-zone-alka">알칼리성</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 분류 결과 카드
    st.markdown('<div class="result-wrap">', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">분석 결과</p>', unsafe_allow_html=True)

    if pred_cluster == 2:
        st.markdown("""
        <div class="result-card result-card-safe">
            <div class="result-status-row">
                <span class="status-dot dot-safe"></span>
                <span class="status-label label-safe">양호한 수질 — Cluster 2</span>
            </div>
            <p class="result-heading">균형 잡힌 깨끗한 물입니다</p>
            <p class="result-body">
                산성도·미네랄·고형물이 모두 고르게 분포된 수질입니다.
                별도의 정수 처리 없이도 생활용수와 식수로 적합하며,
                일반 필터만으로도 충분한 정수 효율을 기대할 수 있습니다.
            </p>
            <div class="tag-row">
                <span class="tag tag-green">생활용수 적합</span>
                <span class="tag tag-green">식수 적합</span>
                <span class="tag tag-green">일반 필터로 충분</span>
                <span class="tag tag-green">안전성 높음</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif pred_cluster == 0:
        st.markdown("""
        <div class="result-card result-card-danger">
            <div class="result-status-row">
                <span class="status-dot dot-danger"></span>
                <span class="status-label label-danger">주의 필요 — Cluster 0</span>
            </div>
            <p class="result-heading">고형물이 지나치게 많은 물입니다</p>
            <p class="result-body">
                물속에 녹아있는 총 고형물(TDS)이 기준치보다 높습니다.
                탁도가 높거나 텁텁한 맛이 날 수 있으며, 장기 음용은 권장하지 않습니다.
                역삼투압(RO) 필터 등 정밀 고형물 제거 공정이 필요합니다.
            </p>
            <div class="tag-row">
                <span class="tag tag-red">식수 부적합</span>
                <span class="tag tag-red">공업용수 권장</span>
                <span class="tag tag-red">RO 필터 필요</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="result-card result-card-mineral">
            <div class="result-status-row">
                <span class="status-dot dot-mineral"></span>
                <span class="status-label label-mineral">미네랄 풍부 — Cluster 1</span>
            </div>
            <p class="result-heading">미네랄이 강한 센물(경수)입니다</p>
            <p class="result-body">
                칼슘·마그네슘 같은 미네랄 성분이 풍부한 경수입니다.
                총 고형물 자체는 낮지만 배관과 보일러에 스케일이 쌓일 수 있습니다.
                미네랄 광천수로 활용하거나, 필요 시 연수기 설치를 고려하세요.
            </p>
            <div class="tag-row">
                <span class="tag tag-blue">미네랄 광천수</span>
                <span class="tag tag-blue">연수기 권장</span>
                <span class="tag tag-blue">스케일 주의</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # pH / 경도 추가 경고
    ph_alerts = []
    if ph < 5.5:
        ph_alerts.append(("danger", "🔴", "pH 심각하게 낮음 — 강산성", f"입력값 {ph:.1f} — 기준치(6.5)보다 훨씬 낮습니다. 배관 부식 및 인체 자극을 유발할 수 있어 즉각적인 중화 처리가 필요합니다."))
    elif ph < 6.5:
        ph_alerts.append(("warn", "🟡", "pH 낮음 — 약산성", f"입력값 {ph:.1f} — 식수 기준(6.5~8.5)보다 낮습니다. 장기 음용 시 치아 부식 가능성이 있으며, 중화 필터 사용을 권장합니다."))
    elif ph > 9.5:
        ph_alerts.append(("danger", "🔴", "pH 심각하게 높음 — 강알칼리성", f"입력값 {ph:.1f} — 기준치(8.5)를 크게 초과합니다. 소화기 자극 및 미네랄 불균형을 유발할 수 있습니다."))
    elif ph > 8.5:
        ph_alerts.append(("warn", "🟡", "pH 높음 — 약알칼리성", f"입력값 {ph:.1f} — 식수 기준(6.5~8.5)보다 높습니다. 쓴맛이 느껴질 수 있으며 장기 음용 시 주의가 필요합니다."))

    hard_alerts = []
    if hardness < 30:
        hard_alerts.append(("info", "🔵", "경도 매우 낮음 — 극연수", f"입력값 {hardness:.0f} mg/L — 미네랄이 거의 없는 증류수에 가까운 상태입니다. 장기 음용 시 칼슘·마그네슘 부족으로 이어질 수 있습니다."))
    elif hardness < 60:
        hard_alerts.append(("warn", "🟡", "경도 낮음 — 연수", f"입력값 {hardness:.0f} mg/L — 미네랄 함량이 적은 연수입니다. 음용에는 문제없으나 뼈 건강을 위해 식이 미네랄 보충을 권장합니다."))
    elif hardness > 400:
        hard_alerts.append(("danger", "🔴", "경도 매우 높음 — 과경수", f"입력값 {hardness:.0f} mg/L — 칼슘·마그네슘이 지나치게 많습니다. 배관 스케일이 심하게 쌓이며 쓴맛·텁텁한 맛이 납니다. 연수기 또는 이온교환 필터가 필요합니다."))
    elif hardness > 200:
        hard_alerts.append(("warn", "🟡", "경도 높음 — 경수", f"입력값 {hardness:.0f} mg/L — 미네랄 함량이 높은 경수입니다. 음용은 가능하나 보일러·커피머신 등 기기에 물때가 쌓일 수 있습니다."))

    all_alerts = ph_alerts + hard_alerts
    if all_alerts:
        st.markdown('<p class="alert-section-header">추가 항목별 진단</p>', unsafe_allow_html=True)
        alert_html = '<div class="alert-list">'
        for level, icon, title, desc in all_alerts:
            stripe_class = f"stripe-{'danger' if level == 'danger' else 'info' if level == 'info' else 'warn'}"
            alert_html += f"""
            <div class="alert-item">
                <div class="alert-stripe {stripe_class}">{icon}</div>
                <div class="alert-content">
                    <p class="alert-title">{title}</p>
                    <p class="alert-desc">{desc}</p>
                </div>
            </div>"""
        alert_html += '</div>'
        st.markdown(alert_html, unsafe_allow_html=True)

else:
    # 빈 화면 가이드
    st.markdown("""
    <div class="guide-panel">
        <p class="guide-monogram">Water Mind · 수질 분석 대기 중</p>
        <p class="guide-heading">측정값을 입력해 주세요</p>
        <p class="guide-text">
            왼쪽 사이드바에서 pH, 경도, 총용존고형물 수치를 입력한 뒤
            「분석 실행」을 누르면 AI가 즉시 수질 유형을 분류합니다.
        </p>
        <span class="guide-arrow">← 사이드바에서 값 입력</span>
    </div>
    """, unsafe_allow_html=True)
