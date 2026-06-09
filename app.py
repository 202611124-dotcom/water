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
# 2. 글로벌 CSS 인젝션 (프리미엄 디자인)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── 전체 배경 & 기본 텍스트 ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.main, .block-container,
div[class*="block-container"],
div[class*="stMarkdown"],
div[class*="element-container"] {
    background-color: #070F1C !important;
    color: #E2EEF4 !important;
    font-family: 'Inter', sans-serif !important;
}

/* 모든 p, span, div 텍스트 기본색 강제 */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] h5,
[data-testid="stAppViewContainer"] label {
    color: #E2EEF4 !important;
}

/* stMarkdown 내부 텍스트 */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em {
    color: #E2EEF4 !important;
}

/* st.caption 텍스트 */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: #7A9BB0 !important;
}

/* 섹션 헤더 (#### 등) */
[data-testid="stHeadingWithActionElements"] h4,
[data-testid="stHeadingWithActionElements"] h3,
[data-testid="stHeadingWithActionElements"] h2 {
    color: #E2EEF4 !important;
}

/* ── 사이드바 ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background: linear-gradient(180deg, #0D1B2E 0%, #091525 100%) !important;
    border-right: 1px solid rgba(14,165,201,0.15) !important;
}
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] strong {
    color: #C8DDE9 !important;
    background-color: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #7A9BB0 !important;
}

/* 사이드바 헤더 */
.sidebar-brand {
    text-align: center;
    padding: 1.2rem 0 0.6rem;
}
.sidebar-brand h1 {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #22D3EE, #0EA5C9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    margin: 0;
}
.sidebar-brand p {
    font-size: 0.75rem;
    color: #5B8FA0 !important;
    margin: 0.2rem 0 0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* 입력 필드 */
[data-testid="stNumberInput"] input {
    background: rgba(14,165,201,0.07) !important;
    border: 1px solid rgba(14,165,201,0.25) !important;
    border-radius: 10px !important;
    color: #E2EEF4 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0.75rem !important;
    transition: border-color 0.2s;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #22D3EE !important;
    box-shadow: 0 0 0 3px rgba(34,211,238,0.15) !important;
}

/* 레이블 */
[data-testid="stNumberInput"] label,
[data-testid="stSidebar"] label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    color: #8DB4C4 !important;
    text-transform: uppercase !important;
}

/* 분석 버튼 */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0EA5C9, #0284C7) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.7rem 1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(14,165,201,0.35) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #22D3EE, #0EA5C9) !important;
    box-shadow: 0 6px 28px rgba(34,211,238,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── 메인 타이틀 영역 ── */
.hero-section {
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #0EA5C9;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    line-height: 1.1;
    color: #F0F8FF;
    letter-spacing: -1.5px;
    margin: 0 0 0.8rem;
}
.hero-title span {
    background: linear-gradient(135deg, #22D3EE 30%, #0EA5C9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 0.95rem;
    color: #7A9BB0;
    line-height: 1.6;
    max-width: 560px;
}

/* ── 물결 구분선 ── */
.wave-divider {
    margin: 1.5rem 0;
    height: 2px;
    background: linear-gradient(90deg, #0EA5C9, #22D3EE 40%, transparent);
    border-radius: 2px;
}

/* ── 지표 카드 ── */
.metrics-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-card {
    flex: 1;
    background: rgba(14,165,201,0.06);
    border: 1px solid rgba(14,165,201,0.18);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #0EA5C9, #22D3EE);
}
.metric-card:hover {
    border-color: rgba(34,211,238,0.35);
}
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5B8FA0;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #E8F4FA;
    line-height: 1;
}
.metric-unit {
    font-size: 0.78rem;
    color: #5B8FA0;
    margin-top: 0.3rem;
}

/* ── 결과 카드 ── */
.result-card {
    border-radius: 20px;
    padding: 2rem 2.2rem;
    position: relative;
    overflow: hidden;
    margin-top: 1rem;
}
.result-card-safe {
    background: linear-gradient(135deg, rgba(6,95,70,0.25), rgba(4,120,87,0.12));
    border: 1px solid rgba(16,185,129,0.3);
}
.result-card-danger {
    background: linear-gradient(135deg, rgba(127,29,29,0.3), rgba(153,27,27,0.12));
    border: 1px solid rgba(239,68,68,0.3);
}
.result-card-mineral {
    background: linear-gradient(135deg, rgba(30,58,138,0.3), rgba(37,99,235,0.12));
    border: 1px solid rgba(96,165,250,0.3);
}

.result-badge {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.badge-safe   { background: rgba(16,185,129,0.2); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }
.badge-danger { background: rgba(239,68,68,0.2);  color: #F87171; border: 1px solid rgba(248,113,113,0.3); }
.badge-mineral{ background: rgba(96,165,250,0.2); color: #93C5FD; border: 1px solid rgba(147,197,253,0.3); }

.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #F0F8FF;
    margin: 0 0 0.5rem;
    letter-spacing: -0.5px;
}
.result-desc {
    font-size: 0.95rem;
    color: #9BBFD0;
    line-height: 1.7;
    max-width: 620px;
}

/* 태그 리스트 */
.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1.2rem;
}
.tag {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}
.tag-green  { background: rgba(16,185,129,0.15); color: #6EE7B7; }
.tag-red    { background: rgba(239,68,68,0.15);  color: #FCA5A5; }
.tag-blue   { background: rgba(96,165,250,0.15); color: #BFDBFE; }

/* ── pH / 경도 경고 알림 카드 ── */
.alert-row {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    margin-top: 1.2rem;
}
.alert-item {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    background: rgba(251,191,36,0.07);
    border: 1px solid rgba(251,191,36,0.25);
    border-left: 3px solid #FBBF24;
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
}
.alert-item.alert-high {
    background: rgba(239,68,68,0.07);
    border-color: rgba(239,68,68,0.25);
    border-left-color: #EF4444;
}
.alert-item.alert-low {
    background: rgba(139,92,246,0.07);
    border-color: rgba(139,92,246,0.25);
    border-left-color: #A78BFA;
}
.alert-icon {
    font-size: 1.15rem;
    line-height: 1.4;
    flex-shrink: 0;
}
.alert-text strong {
    display: block;
    font-size: 0.82rem;
    font-weight: 700;
    color: #F0F8FF !important;
    margin-bottom: 0.15rem;
}
.alert-text span {
    font-size: 0.8rem;
    color: #9BBFD0 !important;
    line-height: 1.5;
}

/* 빈 화면 가이드 */
.guide-card {
    background: rgba(14,165,201,0.05);
    border: 1px dashed rgba(14,165,201,0.25);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    margin-top: 1.5rem;
}
.guide-icon {
    font-size: 3rem;
    margin-bottom: 0.8rem;
}
.guide-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #C8DDE9;
    margin-bottom: 0.5rem;
}
.guide-text {
    font-size: 0.88rem;
    color: #5B8FA0;
    line-height: 1.6;
}

/* Streamlit 기본 요소 숨기기 / 오버라이드 */
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stMetric"] {
    background: rgba(14,165,201,0.06) !important;
    border: 1px solid rgba(14,165,201,0.18) !important;
    border-radius: 14px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #7A9BB0 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #E8F4FA !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] div,
[data-testid="stMetricDelta"] svg {
    color: #22D3EE !important;
}

/* 숫자 입력 화살표 버튼 배경 */
[data-testid="stNumberInput"] button {
    background: rgba(14,165,201,0.1) !important;
    border-color: rgba(14,165,201,0.2) !important;
    color: #E2EEF4 !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(14,165,201,0.25) !important;
}

/* 구분선 */
hr { border-color: rgba(14,165,201,0.15) !important; }

/* 사이드바 구분선 */
[data-testid="stSidebar"] hr { border-color: rgba(14,165,201,0.2) !important; }

/* 툴팁 */
[data-testid="stTooltipIcon"] { color: #3B6F87 !important; }

/* 스크롤바 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #070F1C; }
::-webkit-scrollbar-thumb { background: #1B3A50; border-radius: 3px; }
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
# 4. 사이드바 UI
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h1>💧 Water Mind</h1>
        <p>수질 AI 분석 시스템</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # 물 이미지
    st.image(
        "https://images.unsplash.com/photo-1548880338-7416bad859e4?q=80&w=400",
        use_container_width=True,
        output_format="auto"
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("**측정 데이터 입력**")
    st.caption("실측한 수질 수치를 아래에 입력하세요.")

    ph       = st.number_input("pH  (산성도)",        min_value=0.0,  max_value=14.0,   value=7.0,    step=0.1,  help="6.5~8.5 사이가 식수 적합 기준")
    hardness = st.number_input("경도  (Hardness)",     min_value=0.0,  max_value=500.0,  value=150.0,  step=1.0,  help="칼슘·마그네슘 총량 (mg/L)")
    solids   = st.number_input("총용존고형물 (Solids)", min_value=0.0,  max_value=5000.0, value=1000.0, step=10.0, help="물에 녹아있는 유·무기 물질 총량 (ppm)")

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    predict_btn = st.button("🔬  수질 분석하기", use_container_width=True, type="primary")

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.72rem;color:#3B6F87;text-align:center;line-height:1.5'>"
        "K-Means 머신러닝 기반<br>실시간 수질 특성 분류 시스템"
        "</p>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# 5. 메인 대시보드
# ─────────────────────────────────────────────

# 히어로 타이틀
st.markdown("""
<div class="hero-section">
    <p class="hero-eyebrow">AI-Powered Water Analysis</p>
    <h1 class="hero-title">지금 이 물,<br><span>어떤 상태인가요?</span></h1>
    <p class="hero-sub">
        pH·경도·총용존고형물 세 가지 수치만 입력하면,
        AI가 수질 특성을 즉시 분석해 드립니다.
    </p>
</div>
<div class="wave-divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 6. 예측 + 결과 렌더링
# ─────────────────────────────────────────────
if predict_btn:

    # 데이터 전처리
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

    # ── 입력값 요약 카드 ──
    st.markdown("#### 입력된 수질 데이터")
    c1, c2, c3 = st.columns(3)
    c1.metric("pH (산성도)",       f"{ph:.1f}",        delta="적합 범위 6.5 ~ 8.5")
    c2.metric("경도",              f"{hardness:.0f} mg/L")
    c3.metric("총용존고형물",       f"{solids:.0f} ppm")

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("#### 분석 결과")

    # ── 결과별 카드 렌더링 ──
    if pred_cluster == 2:
        st.markdown("""
        <div class="result-card result-card-safe">
            <span class="result-badge badge-safe">✅ 양호한 수질</span>
            <p class="result-title">균형 잡힌 깨끗한 물입니다</p>
            <p class="result-desc">
                산성도·미네랄·고형물이 모두 고르게 분포된 수질입니다.
                별도의 정수 처리 없이도 생활용수·식수로 적합하며,
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
            <span class="result-badge badge-danger">⚠️ 주의 필요</span>
            <p class="result-title">고형물이 지나치게 많은 물입니다</p>
            <p class="result-desc">
                물속에 녹아있는 총 고형물(Solids)이 기준치보다 높습니다.
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
            <span class="result-badge badge-mineral">💎 미네랄 풍부</span>
            <p class="result-title">미네랄이 강한 센물(경수)입니다</p>
            <p class="result-desc">
                칼슘·마그네슘 같은 미네랄 성분이 풍부한 경수입니다.
                고형물 자체는 낮지만, 배관과 보일러에 물때(스케일)가 쌓일 수 있습니다.
                미네랄 광천수로 활용하거나, 필요 시 연수기 설치를 고려해 보세요.
            </p>
            <div class="tag-row">
                <span class="tag tag-blue">미네랄 광천수</span>
                <span class="tag tag-blue">연수기 권장</span>
                <span class="tag tag-blue">스케일 주의</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── pH / 경도 추가 경고 판정 ──
    # pH 기준: 정상 6.5~8.5 / 주의 5.5~6.5 또는 8.5~9.5 / 위험 <5.5 또는 >9.5
    ph_alerts = []
    if ph < 5.5:
        ph_alerts.append(("high", "🔴", "pH 심각하게 낮음 (강산성)", f"입력값 {ph:.1f} — 기준치(6.5)보다 훨씬 낮습니다. 강한 산성으로 배관 부식 및 인체 자극을 유발할 수 있어 즉각적인 중화 처리가 필요합니다."))
    elif ph < 6.5:
        ph_alerts.append(("low", "🟡", "pH 낮음 (약산성)", f"입력값 {ph:.1f} — 식수 기준(6.5~8.5)보다 낮습니다. 장기 음용 시 치아 부식 가능성이 있으며, 중화 필터 사용을 권장합니다."))
    elif ph > 9.5:
        ph_alerts.append(("high", "🔴", "pH 심각하게 높음 (강알칼리성)", f"입력값 {ph:.1f} — 기준치(8.5)를 크게 초과합니다. 강한 알칼리성으로 소화기 자극 및 미네랄 불균형을 유발할 수 있습니다."))
    elif ph > 8.5:
        ph_alerts.append(("low", "🟡", "pH 높음 (약알칼리성)", f"입력값 {ph:.1f} — 식수 기준(6.5~8.5)보다 높습니다. 쓴맛이 느껴질 수 있으며 장기 음용 시 주의가 필요합니다."))

    # 경도 기준: 정상 60~200 / 연수 <60 / 경수 200~400 / 과경수 >400
    hard_alerts = []
    if hardness < 30:
        hard_alerts.append(("low", "🟣", "경도 매우 낮음 (극연수)", f"입력값 {hardness:.0f} mg/L — 미네랄이 거의 없는 증류수에 가까운 상태입니다. 장기 음용 시 칼슘·마그네슘 부족으로 이어질 수 있습니다."))
    elif hardness < 60:
        hard_alerts.append(("low", "🟡", "경도 낮음 (연수)", f"입력값 {hardness:.0f} mg/L — 미네랄 함량이 적은 연수입니다. 음용에는 문제없으나 뼈 건강을 위해 식이 미네랄 보충을 권장합니다."))
    elif hardness > 400:
        hard_alerts.append(("high", "🔴", "경도 매우 높음 (과경수)", f"입력값 {hardness:.0f} mg/L — 칼슘·마그네슘이 지나치게 많습니다. 배관 스케일이 심하게 쌓이고 쓴맛·텁텁한 맛이 강하게 납니다. 연수기 또는 이온교환 필터가 필요합니다."))
    elif hardness > 200:
        hard_alerts.append(("low", "🟡", "경도 높음 (경수)", f"입력값 {hardness:.0f} mg/L — 미네랄 함량이 높은 경수입니다. 음용은 가능하나 보일러·커피머신 등 기기에 물때가 쌓일 수 있습니다."))

    all_alerts = ph_alerts + hard_alerts

    if all_alerts:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown("#### 추가 항목별 진단")
        alert_html = '<div class="alert-row">'
        for level, icon, title, desc in all_alerts:
            css_class = f"alert-item alert-{'high' if level == 'high' else 'low'}"
            alert_html += f"""
            <div class="{css_class}">
                <span class="alert-icon">{icon}</span>
                <div class="alert-text">
                    <strong>{title}</strong>
                    <span>{desc}</span>
                </div>
            </div>"""
        alert_html += '</div>'
        st.markdown(alert_html, unsafe_allow_html=True)


    st.markdown("""
    <div class="guide-card">
        <div class="guide-icon">🔬</div>
        <p class="guide-title">분석 준비 완료</p>
        <p class="guide-text">
            왼쪽 사이드바에서 pH, 경도, 총용존고형물 수치를 입력한 뒤<br>
            <strong style="color:#22D3EE">「수질 분석하기」</strong> 버튼을 누르면 즉시 결과가 나타납니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
