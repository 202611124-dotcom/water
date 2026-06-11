import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(
    page_title="Water Mind · 수질 AI 분석",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════
   BASE RESET
═══════════════════════════════════════ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.main, .block-container {
    background-color: #F7F9FC !important;
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
}

/* 전역 텍스트 색상 — 밝은 배경 위에서 확실한 대비 */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] label {
    color: #111827 !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em {
    color: #111827 !important;
}

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background: #111827 !important;
    border-right: 1px solid #1F2937 !important;
}

/* 사이드바 내 모든 텍스트 — 확실히 밝게 */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] li {
    color: #D1D5DB !important;
    background-color: transparent !important;
}
[data-testid="stSidebar"] label {
    color: #D1D5DB !important;
    background-color: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #9CA3AF !important;
}

/* 사이드바 브랜드 */
.sb-brand {
    padding: 1.8rem 0 1.4rem;
    border-bottom: 1px solid #374151;
    margin-bottom: 1.4rem;
}
.sb-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    text-transform: none;
    color: #93C5FD !important;
    margin: 0 0 0.4rem;
}
.sb-title {
    font-family: 'Inter', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #F9FAFB !important;
    margin: 0;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.sb-desc {
    font-size: 0.82rem;
    color: #D1D5DB !important;
    margin: 0.5rem 0 0;
    line-height: 1.6;
}

/* 사이드바 섹션 라벨 */
.sb-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0;
    text-transform: none;
    color: #E5E7EB !important;
    margin: 1.2rem 0 0.7rem;
}

/* 입력 필드 */
[data-testid="stNumberInput"] input {
    background: #1F2937 !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
    color: #F9FAFB !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0.75rem !important;
    transition: border-color 0.15s;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    color: #D1D5DB !important;
}
[data-testid="stNumberInput"] button {
    background: #1F2937 !important;
    border-color: #374151 !important;
    color: #9CA3AF !important;
}
[data-testid="stNumberInput"] button:hover {
    background: #374151 !important;
    color: #F9FAFB !important;
}

/* 분석 버튼 */
[data-testid="stButton"] > button[kind="primary"] {
    background: #2563EB !important;
    border: none !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    padding: 0.7rem 1rem !important;
    transition: background 0.15s, transform 0.1s, box-shadow 0.15s !important;
    box-shadow: 0 1px 8px rgba(37,99,235,0.35) !important;
    margin-top: 0.4rem;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #1D4ED8 !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.45) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ═══════════════════════════════════════
   MAIN — PAGE HEADER
═══════════════════════════════════════ */
.page-header {
    padding: 2.5rem 0 1.8rem;
    border-bottom: 1px solid #E5E7EB;
    margin-bottom: 2rem;
}
.ph-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    color: #2563EB;
    margin-bottom: 0.7rem;
}
.ph-title {
    font-family: 'Inter', sans-serif;
    font-size: clamp(1.8rem, 3vw, 2.6rem);
    font-weight: 700;
    color: #111827;
    letter-spacing: -1px;
    line-height: 1.15;
    margin: 0 0 0.75rem;
}
.ph-title em {
    font-style: normal;
    color: #2563EB;
}
.ph-desc {
    font-size: 0.95rem;
    color: #374151;
    line-height: 1.6;
    max-width: 480px;
}

/* ═══════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════ */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 1.1rem 1.3rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    font-family: 'Inter', sans-serif !important;
    color: #6B7280 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #111827 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 500 !important;
    letter-spacing: -0.5px !important;
}
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] div {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    color: #2563EB !important;
}

/* ═══════════════════════════════════════
   SECTION LABEL
═══════════════════════════════════════ */
.sec-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    color: #6B7280;
    letter-spacing: 0;
    text-transform: none;
    margin: 0 0 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #E5E7EB;
}

/* ═══════════════════════════════════════
   pH SPECTRUM BAR
═══════════════════════════════════════ */
.spectrum-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.4rem 1.6rem 1.2rem;
    margin-top: 1.4rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.spectrum-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1rem;
}
.spectrum-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    color: #6B7280;
}
.spectrum-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    font-weight: 500;
    color: #111827;
}
.ph-track {
    height: 12px;
    border-radius: 6px;
    background: linear-gradient(to right,
        #EF4444 0%, #F97316 12%, #FACC15 22%,
        #84CC16 32%, #22C55E 46%, #10B981 54%,
        #06B6D4 64%, #60A5FA 74%, #818CF8 85%, #A855F7 100%
    );
    position: relative;
}
.ph-pointer {
    position: absolute;
    top: 50%;
    width: 20px;
    height: 20px;
    background: #FFFFFF;
    border: 2px solid #111827;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 2px 6px rgba(0,0,0,0.18);
}
.ph-axis {
    display: flex;
    justify-content: space-between;
    margin-top: 0.55rem;
}
.ph-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #9CA3AF;
}
.ph-zones {
    display: flex;
    justify-content: space-between;
    margin-top: 0.25rem;
}
.ph-zone {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
}
.zone-acid   { color: #EF4444; }
.zone-mid    { color: #16A34A; flex: 1; text-align: center; }
.zone-alka   { color: #818CF8; }

/* ═══════════════════════════════════════
   RESULT CARD
═══════════════════════════════════════ */
.result-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.8rem 2rem 1.6rem;
    margin-top: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 3px 0 0 3px;
}
.rc-safe::before    { background: #22C55E; }
.rc-danger::before  { background: #EF4444; }
.rc-mineral::before { background: #3B82F6; }

.rc-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.9rem;
}
.badge-safe    { background: #F0FDF4; color: #15803D; border: 1px solid #BBF7D0; }
.badge-danger  { background: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; }
.badge-mineral { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }

.rc-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    display: inline-block;
}
.dot-safe    { background: #22C55E; }
.dot-danger  { background: #EF4444; }
.dot-mineral { background: #3B82F6; }

.rc-title {
    font-family: 'Inter', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.4px;
    margin: 0 0 0.55rem;
    line-height: 1.3;
}
.rc-body {
    font-size: 0.9rem;
    color: #374151;
    line-height: 1.7;
    max-width: 600px;
    margin: 0;
}
.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 1.2rem;
    padding-top: 1rem;
    border-top: 1px solid #F3F4F6;
}
.tag {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.22rem 0.65rem;
    border-radius: 6px;
}
.tag-g { background: #F0FDF4; color: #166534; border: 1px solid #D1FAE5; }
.tag-r { background: #FEF2F2; color: #991B1B; border: 1px solid #FEE2E2; }
.tag-b { background: #EFF6FF; color: #1E40AF; border: 1px solid #DBEAFE; }

/* ═══════════════════════════════════════
   ALERT ITEMS
═══════════════════════════════════════ */
.alert-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.alert-item {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 0.85rem 1rem 0.85rem 1.1rem;
    display: flex;
    gap: 0.85rem;
    align-items: flex-start;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    border-left-width: 3px;
}
.al-danger  { border-left-color: #EF4444; }
.al-warn    { border-left-color: #F59E0B; }
.al-info    { border-left-color: #3B82F6; }

.al-icon { font-size: 1rem; line-height: 1.5; flex-shrink: 0; }
.al-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.84rem;
    font-weight: 600;
    color: #111827 !important;
    margin-bottom: 0.15rem;
}
.al-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: #4B5563 !important;
    line-height: 1.55;
}

/* ═══════════════════════════════════════
   EMPTY GUIDE
═══════════════════════════════════════ */
.guide-wrap {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 3.5rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.guide-icon {
    width: 48px; height: 48px;
    background: #EFF6FF;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    margin: 0 auto 1.1rem;
}
.guide-title {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.4rem;
}
.guide-text {
    font-size: 0.88rem;
    color: #6B7280;
    line-height: 1.6;
    max-width: 340px;
    margin: 0 auto;
}
.guide-hint {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    margin-top: 1.4rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    color: #2563EB;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 6px;
    padding: 0.3rem 0.75rem;
}

/* ═══════════════════════════════════════
   MISC
═══════════════════════════════════════ */
#MainMenu, footer, header { visibility: hidden; }
hr { border-color: #E5E7EB !important; }
[data-testid="stSidebar"] hr { border-color: #1F2937 !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F7F9FC; }
::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 3px; }
[data-testid="stTooltipIcon"] svg { color: #9CA3AF !important; }
</style>
""", unsafe_allow_html=True)


# ─── 리소스 로드 ───────────────────────────────
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
    st.error("🚨 `scaler.pkl`, `model.pkl`, `train_bounds.pkl` 파일이 없습니다.")
    st.stop()


# ─── 사이드바 ──────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <p class="sb-eyebrow">Water Quality · AI Analysis</p>
        <h1 class="sb-title">Water<br>Mind</h1>
        <p class="sb-desc">K-Means 머신러닝 기반<br>실시간 수질 특성 분류 시스템</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sb-label">측정 데이터 입력</p>', unsafe_allow_html=True)

    ph       = st.number_input("pH  —  산성도",          min_value=0.0,  max_value=14.0,   value=7.0,    step=0.1,  help="식수 적합 기준: 6.5 ~ 8.5")
    hardness = st.number_input("Hardness  —  경도",       min_value=0.0,  max_value=500.0,  value=150.0,  step=1.0,  help="칼슘·마그네슘 총량 (mg/L)")
    solids   = st.number_input("Solids  —  총용존고형물", min_value=0.0,  max_value=5000.0, value=1000.0, step=10.0, help="용해된 유·무기 물질 총량 (ppm)")

    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
    predict_btn = st.button("분석 실행", use_container_width=True, type="primary")

    st.markdown("---")
    st.caption("입력값은 저장되지 않으며 분석은 즉시 수행됩니다.")


# ─── 메인 헤더 ────────────────────────────────
st.markdown("""
<div class="page-header">
    <p class="ph-eyebrow">AI-Powered Water Quality Analysis</p>
    <h1 class="ph-title">지금 이 물,<br><em>어떤 상태인가요?</em></h1>
    <p class="ph-desc">pH·경도·총용존고형물 세 수치를 입력하면 AI가 수질 유형을 즉시 분류하고 사용 가능 여부를 알려드립니다.</p>
</div>
""", unsafe_allow_html=True)


# ─── 결과 ─────────────────────────────────────
if predict_btn:

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

    # 입력 요약
    st.markdown('<p class="sec-label">입력된 수질 데이터</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("pH — 산성도",       f"{ph:.1f}",       delta="기준 6.5 ~ 8.5")
    c2.metric("경도 (mg/L)",        f"{hardness:.0f}")
    c3.metric("총용존고형물 (ppm)", f"{solids:.0f}")

    # pH 스펙트럼 바
    ph_pct = (ph / 14.0) * 100
    st.markdown(f"""
    <div class="spectrum-card">
        <div class="spectrum-header">
            <span class="spectrum-title">pH 스펙트럼 위치</span>
            <span class="spectrum-value">{ph:.1f}</span>
        </div>
        <div class="ph-track">
            <div class="ph-pointer" style="left:{ph_pct}%"></div>
        </div>
        <div class="ph-axis">
            <span class="ph-num">0</span><span class="ph-num">1</span>
            <span class="ph-num">2</span><span class="ph-num">3</span>
            <span class="ph-num">4</span><span class="ph-num">5</span>
            <span class="ph-num">6</span><span class="ph-num">7</span>
            <span class="ph-num">8</span><span class="ph-num">9</span>
            <span class="ph-num">10</span><span class="ph-num">11</span>
            <span class="ph-num">12</span><span class="ph-num">13</span>
            <span class="ph-num">14</span>
        </div>
        <div class="ph-zones">
            <span class="ph-zone zone-acid">산성</span>
            <span class="ph-zone zone-mid">중성 · 식수 적합</span>
            <span class="ph-zone zone-alka">알칼리성</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 분류 결과
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    st.markdown('<p class="sec-label">분석 결과</p>', unsafe_allow_html=True)

    if pred_cluster == 2:
        st.markdown("""
        <div class="result-card rc-safe">
            <span class="rc-badge badge-safe"><span class="rc-dot dot-safe"></span>양호한 수질</span>
            <p class="rc-title">균형 잡힌 깨끗한 물입니다</p>
            <p class="rc-body">산성도·미네랄·고형물이 모두 고르게 분포된 수질입니다.
            별도의 정수 처리 없이도 생활용수와 식수로 적합하며,
            일반 필터만으로 충분한 정수 효율을 기대할 수 있습니다.</p>
            <div class="tag-row">
                <span class="tag tag-g">생활용수 적합</span>
                <span class="tag tag-g">식수 적합</span>
                <span class="tag tag-g">일반 필터로 충분</span>
                <span class="tag tag-g">안전성 높음</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif pred_cluster == 0:
        st.markdown("""
        <div class="result-card rc-danger">
            <span class="rc-badge badge-danger"><span class="rc-dot dot-danger"></span>주의 필요</span>
            <p class="rc-title">고형물이 지나치게 많은 물입니다</p>
            <p class="rc-body">물속에 녹아있는 총 고형물(TDS)이 기준치보다 높습니다.
            탁도가 높거나 텁텁한 맛이 날 수 있으며, 장기 음용은 권장하지 않습니다.
            역삼투압(RO) 필터 등 정밀 고형물 제거 공정이 필요합니다.</p>
            <div class="tag-row">
                <span class="tag tag-r">식수 부적합</span>
                <span class="tag tag-r">공업용수 권장</span>
                <span class="tag tag-r">RO 필터 필요</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="result-card rc-mineral">
            <span class="rc-badge badge-mineral"><span class="rc-dot dot-mineral"></span>미네랄 풍부</span>
            <p class="rc-title">미네랄이 강한 센물(경수)입니다</p>
            <p class="rc-body">칼슘·마그네슘 같은 미네랄 성분이 풍부한 경수입니다.
            총 고형물 자체는 낮지만 배관과 보일러에 스케일이 쌓일 수 있습니다.
            미네랄 광천수로 활용하거나 필요 시 연수기 설치를 고려하세요.</p>
            <div class="tag-row">
                <span class="tag tag-b">미네랄 광천수</span>
                <span class="tag tag-b">연수기 권장</span>
                <span class="tag tag-b">스케일 주의</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 추가 경고
    ph_alerts = []
    if ph < 5.5:
        ph_alerts.append(("danger", "🔴", "pH 심각하게 낮음 — 강산성", f"입력값 {ph:.1f} · 기준치(6.5)보다 훨씬 낮습니다. 강한 산성으로 배관 부식 및 인체 자극을 유발할 수 있으며, 즉각적인 중화 처리가 필요합니다."))
    elif ph < 6.5:
        ph_alerts.append(("warn", "🟡", "pH 낮음 — 약산성", f"입력값 {ph:.1f} · 식수 기준(6.5~8.5)보다 낮습니다. 장기 음용 시 치아 부식 가능성이 있으며, 중화 필터 사용을 권장합니다."))
    elif ph > 9.5:
        ph_alerts.append(("danger", "🔴", "pH 심각하게 높음 — 강알칼리성", f"입력값 {ph:.1f} · 기준치(8.5)를 크게 초과합니다. 소화기 자극 및 미네랄 불균형을 유발할 수 있습니다."))
    elif ph > 8.5:
        ph_alerts.append(("warn", "🟡", "pH 높음 — 약알칼리성", f"입력값 {ph:.1f} · 식수 기준(6.5~8.5)보다 높습니다. 쓴맛이 느껴질 수 있으며 장기 음용 시 주의가 필요합니다."))

    hard_alerts = []
    if hardness < 30:
        hard_alerts.append(("info", "🔵", "경도 매우 낮음 — 극연수", f"입력값 {hardness:.0f} mg/L · 미네랄이 거의 없는 증류수에 가까운 상태입니다. 장기 음용 시 칼슘·마그네슘 부족으로 이어질 수 있습니다."))
    elif hardness < 60:
        hard_alerts.append(("warn", "🟡", "경도 낮음 — 연수", f"입력값 {hardness:.0f} mg/L · 미네랄 함량이 적은 연수입니다. 음용에는 문제없으나 뼈 건강을 위해 식이 미네랄 보충을 권장합니다."))
    elif hardness > 400:
        hard_alerts.append(("danger", "🔴", "경도 매우 높음 — 과경수", f"입력값 {hardness:.0f} mg/L · 칼슘·마그네슘이 지나치게 많습니다. 배관 스케일이 심하게 쌓이며 쓴맛·텁텁한 맛이 납니다. 연수기 또는 이온교환 필터가 필요합니다."))
    elif hardness > 200:
        hard_alerts.append(("warn", "🟡", "경도 높음 — 경수", f"입력값 {hardness:.0f} mg/L · 미네랄 함량이 높은 경수입니다. 음용은 가능하나 보일러·커피머신 등 기기에 물때가 쌓일 수 있습니다."))

    all_alerts = ph_alerts + hard_alerts
    if all_alerts:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<p class="sec-label">추가 항목별 진단</p>', unsafe_allow_html=True)
        alert_html = '<div class="alert-list">'
        for level, icon, title, desc in all_alerts:
            css = f"al-{'danger' if level == 'danger' else 'info' if level == 'info' else 'warn'}"
            alert_html += f"""
            <div class="alert-item {css}">
                <span class="al-icon">{icon}</span>
                <div>
                    <p class="al-title">{title}</p>
                    <p class="al-desc">{desc}</p>
                </div>
            </div>"""
        alert_html += '</div>'
        st.markdown(alert_html, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="guide-wrap">
        <div class="guide-icon">💧</div>
        <p class="guide-title">측정값을 입력해 주세요</p>
        <p class="guide-text">왼쪽 사이드바에서 pH, 경도, 총용존고형물 수치를 입력한 뒤 「분석 실행」을 누르면 AI가 즉시 수질 유형을 분류합니다.</p>
        <span class="guide-hint">← 사이드바에서 값 입력</span>
    </div>
    """, unsafe_allow_html=True)
