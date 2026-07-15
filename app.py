import streamlit as st
import pandas as pd
import joblib

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* ── Deep Midnight Blue & Real Gold Theme ── */
.stApp {
    background: linear-gradient(135deg, #05080f 0%, #0a0f1a 30%, #0f1625 60%, #0a0f1a 100%);
    min-height: 100vh;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-icon {
    font-size: 3.5rem;
    margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 30px rgba(212, 175, 55, 0.3));
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    background: linear-gradient(180deg, #f5e56b 0%, #d4af37 30%, #b8860b 60%, #d4af37 80%, #f5e56b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: 1px;
    text-shadow: 0 0 40px rgba(212, 175, 55, 0.15);
}
.hero p {
    color: #8a9bb5;
    font-size: 0.92rem;
    margin-top: 0.5rem;
    font-weight: 300;
    letter-spacing: 0.5px;
}

/* ── Card ── */
.card {
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border: 1px solid rgba(212, 175, 55, 0.12);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.card-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    background: linear-gradient(90deg, #d4af37, #f5e56b, #b8860b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(212, 175, 55, 0.1);
    padding-bottom: 0.8rem;
}

/* ── Labels ── */
label, .stNumberInput > label, .stSelectbox > label, .stSlider > label {
    color: #b0c4de !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.3px;
}

/* ── Number inputs ── */
.stNumberInput input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212, 175, 55, 0.15) !important;
    border-radius: 10px !important;
    color: #e8e8e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}
.stNumberInput input:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.12) !important;
    background: rgba(212, 175, 55, 0.03) !important;
}

/* ── Selectbox ── */
.stSelectbox select {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212, 175, 55, 0.15) !important;
    border-radius: 10px !important;
    color: #e8e8e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1rem !important;
}
.stSelectbox select:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.12) !important;
}

/* ── Sliders ── */
.stSlider div[data-baseweb="slider"] {
    background: rgba(255,255,255,0.05) !important;
}
.stSlider div[data-baseweb="slider"] div[role="slider"] {
    background: linear-gradient(135deg, #d4af37, #f5e56b) !important;
    border-color: #d4af37 !important;
    box-shadow: 0 0 15px rgba(212, 175, 55, 0.3) !important;
}
.stSlider div[data-baseweb="slider"] div[data-testid="stThumbValue"] {
    color: #d4af37 !important;
}

/* ── Rating hints ── */
.rating-hint {
    font-size: 0.7rem;
    color: #5a6b85;
    font-weight: 300;
    display: block;
    margin-top: 0.15rem;
}
.rating-hint span {
    color: #8a9bb5;
    font-weight: 400;
}
.rating-hint .gold {
    color: #d4af37;
    font-weight: 500;
}

/* ── Predict button ── */
.stButton > button {
    width: 100%;
    padding: 0.9rem 2rem;
    font-family: 'Sora', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #05080f !important;
    background: linear-gradient(135deg, #d4af37 0%, #f5e56b 30%, #d4af37 60%, #b8860b 100%);
    background-size: 200% 200%;
    border: 1px solid rgba(212, 175, 55, 0.3) !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.5px;
    margin-top: 0.5rem;
    box-shadow: 0 4px 24px rgba(212, 175, 55, 0.2) !important;
    text-transform: uppercase;
    animation: goldShimmer 3s ease-in-out infinite;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 40px rgba(212, 175, 55, 0.35) !important;
    background: linear-gradient(135deg, #f5e56b 0%, #d4af37 40%, #f5e56b 70%, #d4af37 100%);
    background-size: 200% 200%;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

@keyframes goldShimmer {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Result box ── */
.result-box {
    background: linear-gradient(145deg, rgba(212, 175, 55, 0.06), rgba(212, 175, 55, 0.02));
    border: 1px solid rgba(212, 175, 55, 0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    text-align: center;
    animation: fadeIn 0.6s ease;
    box-shadow: 0 8px 32px rgba(212, 175, 55, 0.05);
}
.result-emoji { 
    font-size: 3.2rem; 
    display: block;
    margin-bottom: 0.5rem;
}
.result-label {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8a9bb5;
    margin: 0.2rem 0;
}
.result-price {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(180deg, #f5e56b 0%, #d4af37 30%, #b8860b 50%, #d4af37 70%, #f5e56b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.3rem 0;
    text-shadow: 0 0 40px rgba(212, 175, 55, 0.1);
}
.result-conf {
    font-size: 0.8rem;
    color: #5a6b85;
    font-weight: 300;
}
.result-divider {
    border: none;
    border-top: 1px solid rgba(212, 175, 55, 0.1);
    margin: 1rem 0;
}
.result-detail {
    color: #8a9bb5;
    font-size: 0.85rem;
}
.result-detail span {
    color: #d4af37;
    font-weight: 500;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid rgba(212, 175, 55, 0.05);
    margin: 1.5rem 0;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Gold accent elements ── */
.gold-text {
    background: linear-gradient(90deg, #d4af37, #f5e56b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.gold-border {
    border-color: #d4af37 !important;
}

/* ── Checkbox styling ── */
.stCheckbox > label {
    color: #b0c4de !important;
}
.stCheckbox span[data-testid="stCheckbox"] {
    border-color: rgba(212, 175, 55, 0.3) !important;
}
.stCheckbox span[data-testid="stCheckbox"] input:checked {
    background-color: #d4af37 !important;
    border-color: #d4af37 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #0a0f1a;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #d4af37, #b8860b);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #f5e56b;
}
</style>
""", unsafe_allow_html=True)

# ── Load models ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    model = joblib.load("house_price_model.pkl")
    columns = joblib.load("columns.pkl")
    return model, columns

model, columns = load_models()

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-icon">🏠</div>
    <h1>House Price Prediction</h1>
    <p>Enter the property details below — get an instant AI-powered price estimate</p>
</div>
""", unsafe_allow_html=True)

# ── Section 1 · Property Details ──────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">📐 Property Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    bedrooms = st.number_input("🛏️ Bedrooms", min_value=0, max_value=10, value=3)
    sqft_living = st.number_input("📏 Living Area (sqft)", min_value=0, value=1800)
    floors = st.selectbox("🏗️ Floors", [1, 1.5, 2, 2.5, 3, 3.5])
    
    view = st.slider("👁️ View Rating", 0, 4, 0)
    st.markdown('<span class="rating-hint"><span>0</span> = No view · <span class="gold">2</span> = Average · <span class="gold">4</span> = Excellent</span>', unsafe_allow_html=True)
    
    yr_built = st.number_input("📅 Year Built", min_value=1900, max_value=2026, value=1995)

with col2:
    bathrooms = st.number_input("🚿 Bathrooms", min_value=0.0, step=0.5, value=2.0)
    sqft_lot = st.number_input("🌳 Lot Area (sqft)", min_value=0, value=5000)
    waterfront = st.selectbox("🌊 Waterfront", [0, 1], format_func=lambda x: "✅ Yes" if x == 1 else "❌ No")
    
    condition = st.slider("🔧 Condition Rating", 1, 5, 3)
    st.markdown('<span class="rating-hint"><span>1</span> = Poor · <span class="gold">3</span> = Average · <span class="gold">5</span> = Excellent</span>', unsafe_allow_html=True)
    
    yr_renovated = st.number_input("🔨 Year Renovated", min_value=0, max_value=2026, value=0)

st.markdown('</div>', unsafe_allow_html=True)

# ── Section 2 · Location & Sale Info ──────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">📍 Location & Sale Information</div>', unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)
with col3:
    city = st.selectbox("🏙️ City", [
        "Seattle", "Renton", "Bellevue", "Redmond", "Kirkland",
        "Issaquah", "Kent", "Auburn", "Sammamish", "Federal Way",
        "Shoreline", "Woodinville", "Maple Valley", "Mercer Island",
        "Burien", "Snoqualmie", "Kenmore", "Des Moines", "North Bend",
        "Covington", "Duvall", "Lake Forest Park", "Bothell", "Newcastle",
        "Tukwila", "SeaTac", "Vashon", "Enumclaw", "Carnation",
        "Normandy Park", "Clyde Hill", "Fall City", "Medina", "Black Diamond",
        "Ravensdale", "Pacific", "Algona", "Yarrow Point", "Skykomish",
        "Milton", "Preston", "Inglewood-Finn Hill", "Snoqualmie Pass",
        "Beaux Arts Village"
    ])
with col4:
    month = st.selectbox("📆 Sale Month", [5, 6, 7], format_func=lambda x: ["May", "June", "July"][x-5])
with col5:
    day = st.slider("📅 Sale Day", 1, 31, 15)

st.markdown('</div>', unsafe_allow_html=True)

# ── Predict ────────────────────────────────────────────────────────────────────
if st.button("✨  Predict Price"):
    input_data = pd.DataFrame(0, index=[0], columns=columns)
    input_data["bedrooms"] = bedrooms
    input_data["bathrooms"] = bathrooms
    input_data["sqft_living"] = sqft_living
    input_data["sqft_lot"] = sqft_lot
    input_data["floors"] = floors
    input_data["waterfront"] = waterfront
    input_data["view"] = view
    input_data["condition"] = condition
    input_data["yr_built"] = yr_built
    input_data["yr_renovated"] = yr_renovated
    input_data["month"] = month
    input_data["day"] = day

    city_column = f"city_{city}"
    if city_column in input_data.columns:
        input_data[city_column] = 1

    prediction = model.predict(input_data)[0]

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-box">
        <div class="result-emoji">🏡</div>
        <div class="result-label">Estimated Property Value</div>
        <div class="result-price">${prediction:,.2f}</div>
        <hr class="result-divider">
        <div class="result-detail">
            <span>{bedrooms}</span> beds · <span>{bathrooms}</span> baths · <span>{sqft_living:,}</span> sqft<br>
            <span>{city}</span> · Built in <span>{yr_built}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)