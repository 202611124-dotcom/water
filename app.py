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

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E5E7EB !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] li {
    color: #111827 !important;
    background-color: transparent !important;
}
[data-testid="stSidebar"] label {
    color: #374151 !important;
    background-color: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #6B7280 !important;
}

.sb-brand {
    padding: 1.8rem 0 1.4rem;
    border-bottom: 1px solid #E5E7EB;
    margin-bottom: 1.4rem;
}
.sb-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    color: #2563EB !important;
    margin: 0 0 0.4rem;
}
.sb-title {
    font-family: 'Inter', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #111827 !important;
    margin: 0;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.sb-desc {
    font-size: 0.82rem;
    color: #4B5563 !important;
    margin: 0.5rem 0 0;
    line-height: 1.6;
}

.sb-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    color: #111827 !important;
    margin: 1.2rem 0 0.7rem;
}

[data-testid="stNumberInput"] input {
    background: #F9FAFB !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    color: #111827 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0.75rem !important;
    transition: border-color 0.15s;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    color: #374151 !important;
}
[data-testid="stNumberInput"] button {
    background: #F3F4F6 !important;
    border-color: #D1D5DB !important;
    color: #374151 !important;
}
[data-testid="stNumberInput"] button:hover {
    background: #E5E7EB !important;
    color: #111827 !important;
}

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
.rc-warn::before    { background: #F59E0B; }

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
.badge-warn    { background: #FFFBEB; color: #B45309; border: 1px solid #FDE68A; }

.rc-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    display: inline-block;
}
.dot-safe    { background: #22C55E; }
.dot-danger  { background: #EF4444; }
.dot-mineral { background: #3B82F6; }
.dot-warn    { background: #F59E0B; }

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
.tag-y { background: #FFFBEB; color: #92400E; border: 1px solid #FDE68A; }

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

#MainMenu, footer, header { visibility: hidden; }
hr { border-color: #E5E7EB !important; }
[data-testid="stSidebar"] hr { border-color: #E5E7EB !important; }
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


# ─── 상태 분류 헬퍼 ───────────────────────────
def get_ph_status(ph):
    if ph < 5.5:   return "critical_low"
    elif ph < 6.5: return "low"
    elif ph > 9.5: return "critical_high"
    elif ph > 8.5: return "high"
    else:          return "normal"

def get_hardness_status(h):
    if h < 30:    return "very_soft"
    elif h < 60:  return "soft"
    elif h > 400: return "very_hard"
    elif h > 200: return "hard"
    else:         return "normal"

def build_result(cluster, ph, hardness):
    """
    클러스터 + pH 상태 + 경도 상태를 종합해
    (card_css, badge_css, dot_css, badge_label, title, body, tags) 반환
    """
    ps = get_ph_status(ph)
    hs = get_hardness_status(hardness)

    ph_ok      = ps == "normal"
    hard_ok    = hs == "normal"
    ph_danger  = ps in ("critical_low", "critical_high")
    hard_danger= hs == "very_hard"
    ph_warn    = ps in ("low", "high")
    hard_warn  = hs in ("soft", "hard", "very_soft")

    # ── pH 설명 조각 ──────────────────────────
    ph_note = {
        "critical_low":  f"pH {ph:.1f}로 강산성이라 배관 부식 및 인체 자극 위험이 있습니다.",
        "low":           f"pH {ph:.1f}로 식수 기준(6.5)에 못 미치는 약산성입니다.",
        "critical_high": f"pH {ph:.1f}로 강알칼리성이라 소화기 자극 및 미네랄 불균형을 유발할 수 있습니다.",
        "high":          f"pH {ph:.1f}로 식수 기준(8.5)을 초과하는 약알칼리성입니다.",
        "normal":        f"pH {ph:.1f}로 식수 기준(6.5~8.5) 범위 안에 있습니다.",
    }[ps]

    # ── 경도 설명 조각 ────────────────────────
    hard_note = {
        "very_soft": f"경도 {hardness:.0f} mg/L로 미네랄이 거의 없는 극연수입니다.",
        "soft":      f"경도 {hardness:.0f} mg/L로 미네랄 함량이 낮은 연수입니다.",
        "very_hard": f"경도 {hardness:.0f} mg/L로 칼슘·마그네슘이 과도한 극경수입니다.",
        "hard":      f"경도 {hardness:.0f} mg/L로 미네랄 함량이 높은 경수입니다.",
        "normal":    f"경도 {hardness:.0f} mg/L로 미네랄이 적절하게 함유되어 있습니다.",
    }[hs]

    # ── 클러스터별 기본 베이스 ────────────────
    if cluster == 2:
        # 고형물 기준 "양호"
        if ph_ok and hard_ok:
            return (
                "rc-safe", "badge-safe", "dot-safe", "양호한 수질",
                "세 가지 항목 모두 기준 범위 안입니다",
                f"{ph_note} {hard_note} 총용존고형물도 기준치 이내로, 별도 정수 처리 없이 생활용수·식수로 사용할 수 있습니다.",
                [("g","생활용수 적합"), ("g","식수 적합"), ("g","일반 필터로 충분"), ("g","안전성 높음")]
            )
        elif ph_danger or hard_danger:
            return (
                "rc-danger", "badge-danger", "dot-danger", "주의 필요",
                "총용존고형물은 양호하나 다른 항목에 문제가 있습니다",
                f"고형물 수준은 정상 범위이지만, {ph_note} 또한 {hard_note} 음용 전 해당 항목의 개선이 필요합니다.",
                [("r","조건부 사용"), ("y","pH 조정 필요") if ph_danger else ("y","연수기 권장"), ("g","고형물 정상")]
            )
        else:
            return (
                "rc-warn", "badge-warn", "dot-warn", "부분적 주의",
                "총용존고형물은 양호하나 일부 항목을 확인하세요",
                f"고형물 수준은 적정하지만 {ph_note} 또한 {hard_note} 장기 음용 시 주의가 필요합니다.",
                [("g","고형물 정상"), ("y","pH 확인 권장") if ph_warn else ("y","경도 확인 권장"), ("g","생활용수 적합")]
            )

    elif cluster == 0:
        # 고형물 기준 "위험"
        if ph_ok and hard_ok:
            return (
                "rc-danger", "badge-danger", "dot-danger", "주의 필요",
                "고형물이 지나치게 많은 물입니다",
                f"총용존고형물(TDS)이 기준치를 초과합니다. {ph_note} {hard_note} pH와 경도는 정상이지만 고형물이 많아 장기 음용은 권장하지 않으며, 역삼투압(RO) 필터 등 정밀 정수 처리가 필요합니다.",
                [("r","식수 부적합"), ("r","RO 필터 필요"), ("y","공업용수 권장"), ("g","pH·경도 정상")]
            )
        elif ph_danger or hard_danger:
            return (
                "rc-danger", "badge-danger", "dot-danger", "복합적 문제",
                "고형물 과다에 pH·경도 이상까지 복합 문제입니다",
                f"총용존고형물이 기준치를 초과한 데다, {ph_note} 또한 {hard_note} 음용에 적합하지 않으며 전문적인 수처리 설비가 필요합니다.",
                [("r","음용 금지"), ("r","전문 수처리 필요"), ("r","RO 필터 필요")]
            )
        else:
            return (
                "rc-danger", "badge-danger", "dot-danger", "주의 필요",
                "고형물 과다에 경미한 pH·경도 이상이 동반됩니다",
                f"총용존고형물이 기준치를 초과합니다. 추가로 {ph_note} 또한 {hard_note} 역삼투압(RO) 필터와 함께 pH 또는 경도 조정도 함께 고려하세요.",
                [("r","식수 부적합"), ("r","RO 필터 필요"), ("y","복합 처리 권장")]
            )

    else:
        # cluster == 1 — 고형물 낮음, 미네랄 풍부
        if ph_ok and hard_ok:
            return (
                "rc-mineral", "badge-mineral", "dot-mineral", "미네랄 풍부",
                "미네랄이 강한 센물(경수)입니다",
                f"칼슘·마그네슘 같은 미네랄이 풍부한 경수입니다. {ph_note} {hard_note} 총용존고형물 자체는 낮지만 배관·보일러에 스케일이 쌓일 수 있으니 연수기 설치를 고려하세요.",
                [("b","미네랄 광천수"), ("b","연수기 권장"), ("y","스케일 주의"), ("g","고형물 낮음")]
            )
        elif ph_danger:
            return (
                "rc-danger", "badge-danger", "dot-danger", "주의 필요",
                "미네랄 풍부 + pH 이상이 동반됩니다",
                f"미네랄 함량은 풍부하지만, {ph_note} {hard_note} pH 개선 후 용도에 맞게 사용하세요.",
                [("r","pH 조정 필요"), ("b","미네랄 풍부"), ("y","스케일 주의"), ("g","고형물 낮음")]
            )
        else:
            return (
                "rc-mineral", "badge-mineral", "dot-mineral", "미네랄 풍부",
                "미네랄이 강한 센물(경수)입니다",
                f"칼슘·마그네슘이 풍부한 경수입니다. {ph_note} {hard_note} 배관·보일러 스케일에 유의하고 필요 시 연수기를 설치하세요.",
                [("b","미네랄 광천수"), ("b","연수기 권장"), ("y","스케일 주의"),
                 ("y","pH 확인 권장") if ph_warn else ("g","고형물 낮음")]
            )


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
    st.caption("⚠ 모델은 총용존고형물 기준으로 클러스터를 분류합니다. pH·경도는 규칙 기반으로 별도 반영됩니다.")


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

    # ── 통합 결과 카드 ─────────────────────────
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    st.markdown('<p class="sec-label">분석 결과</p>', unsafe_allow_html=True)

    card_css, badge_css, dot_css, badge_label, title, body, tags = build_result(pred_cluster, ph, hardness)

    tag_html = "".join(
        f'<span class="tag tag-{color}">{label}</span>'
        for color, label in tags
    )

    st.markdown(f"""
    <div class="result-card {card_css}">
        <span class="rc-badge {badge_css}"><span class="rc-dot {dot_css}"></span>{badge_label}</span>
        <p class="rc-title">{title}</p>
        <p class="rc-body">{body}</p>
        <div class="tag-row">{tag_html}</div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="guide-wrap">
        <div class="guide-icon">💧</div>
        <p class="guide-title">측정값을 입력해 주세요</p>
        <p class="guide-text">왼쪽 사이드바에서 pH, 경도, 총용존고형물 수치를 입력한 뒤 「분석 실행」을 누르면 AI가 즉시 수질 유형을 분류합니다.</p>
        <span class="guide-hint">← 사이드바에서 값 입력</span>
    </div>
    """, unsafe_allow_html=True)
