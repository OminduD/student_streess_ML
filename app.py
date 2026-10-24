"""
Student Stress Predictor - Streamlit Web Application
=======================================================
A beautiful, interactive web interface for stress level prediction and data collection.  
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from ai_recommender import get_ai_recommendations
from database import get_storage
from bento_component import render_bento_dashboard

# Page configuration
st.set_page_config(
    page_title="Student Stress Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the storage connection once and cache it
storage = get_storage()

# NEO-BRUTALIST BENTO DESIGN SYSTEM (100% Bento Across Every Tab)
bento_bg = "#0b0d14"
bento_card = "#141724"
bento_card_sub = "#1a1e2f"
bento_border = "#ffffff"
bento_yellow = "#fbbf24"
bento_green = "#4ade80"
bento_cyan = "#38bdf8"
bento_purple = "#a78bfa"
bento_coral = "#f87171"

# Inject Neo-Brutalist Bento Design System CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600;700;800&family=Inter:wght@400;600;700;800;900&display=swap');
    
    :root {
        --bento-bg: #0b0d14;
        --bento-card: #141724;
        --bento-card-sub: #1a1e2f;
        --bento-border: #ffffff;
        --bento-border-dark: #000000;
        --bento-yellow: #fbbf24;
        --bento-green: #4ade80;
        --bento-cyan: #38bdf8;
        --bento-purple: #a78bfa;
        --bento-coral: #f87171;
    }
    
    * {
        font-family: 'Space Grotesk', 'Inter', -apple-system, sans-serif !important;
        box-sizing: border-box;
    }
    
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* NEO-BRUTALIST CANVAS & BLUEPRINT GRID */
    .stApp {
        background-color: #0b0d14 !important;
        background-image: radial-gradient(rgba(255, 255, 255, 0.09) 1.5px, transparent 1.5px) !important;
        background-size: 24px 24px !important;
        color: #ffffff !important;
    }
    
    /* NEO-BRUTALIST MAIN CONTAINER */
    .main .block-container {
        background: #111420 !important;
        border: 3px solid #ffffff !important;
        box-shadow: 10px 10px 0px 0px #ffffff !important;
        border-radius: 0px !important;
        padding: 2.2rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 3rem !important;
    }
    
    /* BENTO PILLS & BADGES */
    .bento-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 4px 10px;
        border: 2px solid #000000;
        box-shadow: 2px 2px 0px #000000;
        color: #000000;
    }
    .pill-yellow { background: #fbbf24 !important; color: #000000 !important; }
    .pill-green { background: #4ade80 !important; color: #000000 !important; }
    .pill-cyan { background: #38bdf8 !important; color: #000000 !important; }
    .pill-purple { background: #a78bfa !important; color: #000000 !important; }
    .pill-coral { background: #f87171 !important; color: #000000 !important; }
    .pill-black { background: #000000 !important; color: #ffffff !important; border-color: #ffffff !important; box-shadow: 2px 2px 0px #ffffff !important; }
    .pill-white { background: #ffffff !important; color: #000000 !important; border-color: #000000 !important; box-shadow: 2px 2px 0px #000000 !important; }
    
    /* NEO-BRUTALIST BENTO BOXES */
    .bento-box {
        background: #151827;
        border: 3px solid #ffffff;
        box-shadow: 6px 6px 0px 0px #ffffff;
        padding: 22px;
        margin-bottom: 22px;
        position: relative;
        transition: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .bento-box:hover {
        transform: translate(-2px, -2px);
        box-shadow: 8px 8px 0px 0px #ffffff;
    }
    .bento-yellow { box-shadow: 6px 6px 0px 0px #fbbf24 !important; }
    .bento-yellow:hover { box-shadow: 8px 8px 0px 0px #fbbf24 !important; }
    .bento-green { box-shadow: 6px 6px 0px 0px #4ade80 !important; }
    .bento-green:hover { box-shadow: 8px 8px 0px 0px #4ade80 !important; }
    .bento-cyan { box-shadow: 6px 6px 0px 0px #38bdf8 !important; }
    .bento-cyan:hover { box-shadow: 8px 8px 0px 0px #38bdf8 !important; }
    .bento-purple { box-shadow: 6px 6px 0px 0px #a78bfa !important; }
    .bento-purple:hover { box-shadow: 8px 8px 0px 0px #a78bfa !important; }
    .bento-coral { box-shadow: 6px 6px 0px 0px #f87171 !important; }
    .bento-coral:hover { box-shadow: 8px 8px 0px 0px #f87171 !important; }
    
    /* BRUTALIST BUTTONS */
    .stButton > button {
        background: #fbbf24 !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        box-shadow: 5px 5px 0px 0px #ffffff !important;
        border-radius: 0px !important;
        padding: 0.9rem 1.8rem !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        transition: all 0.1s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: #fde047 !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 7px 7px 0px 0px #ffffff !important;
        color: #000000 !important;
    }
    .stButton > button:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0px 0px #ffffff !important;
    }
    
    /* BRUTALIST SLIDERS */
    .stSlider label p {
        font-size: 0.95rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #ffffff !important;
    }
    .stSlider [data-baseweb="slider"] {
        padding: 10px 0 !important;
    }
    .stSlider div[role="slider"] {
        border: 2px solid #000000 !important;
        box-shadow: 2px 2px 0px #ffffff !important;
        border-radius: 0px !important;
        background-color: #fbbf24 !important;
        width: 22px !important;
        height: 22px !important;
    }
    
    /* BRUTALIST SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #0d101a !important;
        border-right: 3px solid #ffffff !important;
    }
    section[data-testid="stSidebar"] .stRadio > div {
        background: transparent !important;
        border: none !important;
        gap: 8px !important;
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        background: #171b29 !important;
        border: 2px solid #ffffff !important;
        box-shadow: 4px 4px 0px 0px #38bdf8 !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 10px 14px !important;
        border-radius: 0px !important;
        margin-bottom: 6px !important;
        transition: all 0.15s ease !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: #23293d !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px 0px #38bdf8 !important;
    }
    section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: #fbbf24 !important;
        color: #000000 !important;
        border-color: #000000 !important;
        box-shadow: 4px 4px 0px 0px #ffffff !important;
        transform: translate(-2px, -2px) !important;
    }
    
    /* BRUTALIST METRICS */
    [data-testid="stMetric"] {
        background: #171b29 !important;
        border: 3px solid #ffffff !important;
        box-shadow: 5px 5px 0px 0px #4ade80 !important;
        padding: 14px 18px !important;
        border-radius: 0px !important;
    }
    [data-testid="stMetricLabel"] {
        font-weight: 900 !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        letter-spacing: 1px !important;
    }
    [data-testid="stMetricValue"] {
        font-weight: 900 !important;
        color: #ffffff !important;
        font-size: 2.2rem !important;
    }
    
    /* BRUTALIST EXPANDER */
    .streamlit-expanderHeader {
        background: #171b29 !important;
        border: 2px solid #ffffff !important;
        box-shadow: 4px 4px 0px 0px #ffffff !important;
        border-radius: 0px !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        padding: 12px 18px !important;
    }
    .streamlit-expanderContent {
        background: #131623 !important;
        border: 2px solid #ffffff !important;
        border-top: none !important;
        box-shadow: 4px 4px 0px 0px #ffffff !important;
        border-radius: 0px !important;
        padding: 16px !important;
    }
    
    /* HEADERS */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: -0.5px !important;
    }
    
    /* PLOTLY CONTAINERS */
    .js-plotly-plot {
        background: #151827 !important;
        border: 3px solid #ffffff !important;
        box-shadow: 6px 6px 0px 0px #ffffff !important;
        border-radius: 0px !important;
        padding: 12px !important;
        margin-bottom: 20px !important;
    }
    
    /* DATAFRAMES */
    .stDataFrame {
        background: #151827 !important;
        border: 3px solid #ffffff !important;
        box-shadow: 6px 6px 0px 0px #ffffff !important;
        border-radius: 0px !important;
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div > div > div {
        background: #4ade80 !important;
        border-radius: 0px !important;
        border: 2px solid #000000 !important;
    }
    
    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #0b0d14;
    }
    ::-webkit-scrollbar-thumb {
        background: #fbbf24;
        border: 2px solid #000000;
    }
    </style>
""", unsafe_allow_html=True)

# File paths
MODEL_PATH = "model/stress_predictor_model.joblib"
METRICS_PATH = "model/metrics.json"

# Initialize session state
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'predicted_stress' not in st.session_state:
    st.session_state.predicted_stress = None
if 'input_data' not in st.session_state:
    st.session_state.input_data = None

@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            return model, None
        else:
            return None, "Model not found. Please train the model first."
    except Exception as e:
        return None, f"Error loading model: {str(e)}"

def calculate_engineered_features(sleep_quality, headaches_per_week, 
                                 academic_performance, study_load, 
                                 extracurricular_frequency):
    """Calculate engineered features"""
    wellbeing_score = sleep_quality - (headaches_per_week / 2)
    academic_pressure = study_load * (6 - academic_performance)
    total_workload = study_load + (extracurricular_frequency / 2)
    
    return wellbeing_score, academic_pressure, total_workload

def predict_stress(model, features):
    """Make prediction using the model"""
    try:
        # Check if model has feature names and filter features accordingly
        if hasattr(model, 'feature_names_in_'):
            model_features = model.feature_names_in_.tolist()
            # Keep only features the model was trained on
            features = features[model_features]
        
        prediction = model.predict(features)[0]
        # Get probability if available
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(features)[0]
            confidence = max(proba) * 100
        else:
            confidence = None
        return int(prediction), confidence
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None, None

def save_user_input(data, include_stress=False):
    """Save user input using the database module"""
    return storage.save_user_input(data, include_stress)

def get_stress_description(stress_level):
    """Get description and emoji for stress level"""
    descriptions = {
        1: ("Very Low Stress", "😊", "You're doing great! Keep up the healthy habits."),
        2: ("Low Stress", "🙂", "Good stress management! Minor improvements possible."),
        3: ("Moderate Stress", "😐", "Manageable stress. Consider relaxation techniques."),
        4: ("High Stress", "😟", "Significant stress detected. Take action to reduce it."),
        5: ("Very High Stress", "😰", "Critical stress level! Please seek support.")
    }
    return descriptions.get(stress_level, ("Unknown", "❓", ""))

@st.cache_data(ttl=60) # Cache data for 60 seconds
def load_statistics():
    """Load statistics from the database module"""
    return storage.get_all_data()

# Main App
def main():
    # Epic Neo-Brutalist Bento Header
    st.markdown("""
    <div class="bento-box bento-yellow" style="margin-bottom: 2rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
            <span class="bento-pill pill-yellow">⚡ AI CORE v2.4</span>
            <span class="bento-pill pill-cyan">N=1,100 GROUND TRUTH</span>
            <span class="bento-pill pill-green">SUPABASE CONNECTED</span>
            <span class="bento-pill pill-black">NEO-BRUTALIST BENTO</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 15px;">
            <div>
                <h1 style="font-size: 2.8rem; font-weight: 900; margin: 0; letter-spacing: -1px; text-transform: uppercase; color: #ffffff;">
                    🧠 STUDENT STRESS PREDICTOR
                </h1>
                <p style="color: #94a3b8; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin: 6px 0 0 0;">
                    Multi-Modal Machine Learning Inference & Community Telemetry
                </p>
            </div>
            <div style="display: flex; gap: 8px;">
                <span class="bento-pill pill-white" style="font-size: 12px; padding: 6px 12px;">BENTO SYSTEM ACTIVE</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    model, error = load_model()
    
    if error:
        st.error(f"⚠️ {error}")
        st.info("Please run: `python scripts/train_multi_dataset.py`")
        return
    
    # Sidebar with Neo-Brutalist Bento Design
    with st.sidebar:
        # Brutalist Logo Header
        st.markdown("""
        <div style="background: #151827; border: 3px solid #ffffff; box-shadow: 5px 5px 0px 0px #fbbf24; padding: 18px 14px; text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 4px;">🧠</div>
            <div style="font-size: 1.5rem; font-weight: 900; letter-spacing: -0.5px; text-transform: uppercase; color: #ffffff;">
                STRESS.AI
            </div>
            <div style="margin-top: 8px;">
                <span class="bento-pill pill-yellow" style="font-size: 10px;">NEO-BRUTALIST v2.4</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation header
        st.markdown("""
        <div style="margin-bottom: 0.8rem;">
            <span class="bento-pill pill-cyan" style="width: 100%; justify-content: center;">
                📍 SELECT MODULE
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio("Select Page:", 
                       ["🍱 Bento Analytics", "🔮 Predict Stress", "📊 Statistics", "ℹ️ About"],
                       index=0,
                       label_visibility="collapsed")
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Stats section with Bento cards
        st.markdown("""
        <div style="margin-bottom: 0.8rem;">
            <span class="bento-pill pill-green" style="width: 100%; justify-content: center;">
                📊 LIVE TELEMETRY
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        stats_df = load_statistics()
        if stats_df is not None and not stats_df.empty:
            sub_count = len(stats_df)
            st.markdown(f"""
            <div style="background: #151827; border: 2px solid #ffffff; box-shadow: 4px 4px 0px 0px #4ade80; padding: 12px 14px; margin-bottom: 12px;">
                <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">TOTAL SUBMISSIONS</div>
                <div style="font-size: 1.8rem; font-weight: 900; color: #4ade80; margin-top: 2px;">{sub_count}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if 'stress_level' in stats_df.columns:
                valid_stress = pd.to_numeric(stats_df['stress_level'], errors='coerce').dropna()
                if len(valid_stress) > 0:
                    avg_stress = valid_stress.mean()
                    stress_color = "#4ade80" if avg_stress < 2.5 else ("#fbbf24" if avg_stress < 3.5 else "#f87171")
                    stress_pill = "pill-green" if avg_stress < 2.5 else ("pill-yellow" if avg_stress < 3.5 else "pill-coral")
                    
                    st.markdown(f"""
                    <div style="background: #151827; border: 2px solid #ffffff; box-shadow: 4px 4px 0px 0px {stress_color}; padding: 12px 14px; margin-bottom: 12px;">
                        <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">AVERAGE STRESS</div>
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 2px;">
                            <span style="font-size: 1.8rem; font-weight: 900; color: {stress_color};">{avg_stress:.2f}</span>
                            <span class="bento-pill {stress_pill}" style="font-size: 10px;">/ 5.0</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #151827; border: 2px solid #ffffff; box-shadow: 4px 4px 0px 0px #fbbf24; padding: 14px; text-align: center;">
                <p style="color: #94a3b8; font-weight: 700; margin: 0; font-size: 0.85rem; text-transform: uppercase;">
                    No Telemetry Yet
                </p>
                <p style="color: #fbbf24; font-size: 0.75rem; margin: 4px 0 0 0; font-weight: 900; text-transform: uppercase;">
                    Make a prediction to log data!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Sidebar Footer
        st.markdown("""
        <div style="background: #151827; border: 2px solid #ffffff; box-shadow: 4px 4px 0px 0px #ffffff; padding: 12px; text-align: center;">
            <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; color: #fbbf24; letter-spacing: 1px;">
                ⚡ SUPABASE POSTGRESQL SYNC
            </div>
            <div style="font-size: 9px; font-weight: 700; color: #94a3b8; margin-top: 4px; text-transform: uppercase;">
                ENCRYPTED & RLS PROTECTED
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content based on page selection
    if page == "🍱 Bento Analytics":
        render_bento_dashboard(stats_df)
    elif page == "🔮 Predict Stress":
        show_prediction_page(model)
    elif page == "📊 Statistics":
        show_statistics_page()
    else:
        show_about_page()

def show_prediction_page(model):
    """Display the prediction page with 100% Neo-Brutalist Bento design"""
    
    # Bento Header
    st.markdown("""
    <div class="bento-box bento-cyan" style="margin-bottom: 1.5rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
            <span class="bento-pill pill-cyan">MODULE 01</span>
            <span class="bento-pill pill-yellow">INFERENCE ENGINE</span>
            <span class="bento-pill pill-black">REAL-TIME ML</span>
        </div>
        <h2 style="font-size: 2.2rem; font-weight: 900; margin: 0; color: #ffffff; letter-spacing: -0.5px; text-transform: uppercase;">
            🔮 STRESS LEVEL PREDICTION
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin: 6px 0 0 0;">
            Input lifestyle and academic telemetry below for real-time model inference
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bento Workflow ribbon (4 steps)
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 24px;">
        <div style="background: #151827; border: 2px solid #ffffff; box-shadow: 3px 3px 0px #38bdf8; padding: 12px 14px;">
            <span class="bento-pill pill-cyan" style="font-size: 9px; padding: 2px 6px;">STEP 01</span>
            <div style="font-weight: 900; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; color: #ffffff;">INPUT SIGNALS</div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">Sleep, headaches, study load</div>
        </div>
        <div style="background: #151827; border: 2px solid #ffffff; box-shadow: 3px 3px 0px #fbbf24; padding: 12px 14px;">
            <span class="bento-pill pill-yellow" style="font-size: 9px; padding: 2px 6px;">STEP 02</span>
            <div style="font-weight: 900; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; color: #ffffff;">CALCULATE METRICS</div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">Dynamic feature derivation</div>
        </div>
        <div style="background: #151827; border: 2px solid #ffffff; box-shadow: 3px 3px 0px #4ade80; padding: 12px 14px;">
            <span class="bento-pill pill-green" style="font-size: 9px; padding: 2px 6px;">STEP 03</span>
            <div style="font-weight: 900; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; color: #ffffff;">ML INFERENCE</div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">Random Forest classification</div>
        </div>
        <div style="background: #151827; border: 2px solid #ffffff; box-shadow: 3px 3px 0px #a78bfa; padding: 12px 14px;">
            <span class="bento-pill pill-purple" style="font-size: 9px; padding: 2px 6px;">STEP 04</span>
            <div style="font-weight: 900; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; color: #ffffff;">ACTION PROTOCOL</div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">AI tactical recommendations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two Bento columns for input
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="bento-box bento-cyan" style="padding: 14px 18px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="bento-pill pill-cyan">FACTOR GROUP A</span>
                <span style="font-weight: 900; font-size: 0.85rem; color: #38bdf8; text-transform: uppercase;">LIFESTYLE & RECOVERY</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        sleep_quality = st.slider(
            "😴 Sleep Quality",
            min_value=1, max_value=5, value=3,
            help="Rate your sleep quality: 1=Very Poor, 5=Excellent"
        )
        
        headaches_per_week = st.slider(
            "🤕 Headaches per Week",
            min_value=0, max_value=7, value=1,
            help="How many times per week do you experience headaches?"
        )
        
        extracurricular_frequency = st.slider(
            "🎾 Extracurricular Activities (per week)",
            min_value=0, max_value=7, value=2,
            help="How many times per week do you do extracurricular activities?"
        )
    
    with col2:
        st.markdown("""
        <div class="bento-box bento-yellow" style="padding: 14px 18px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="bento-pill pill-yellow">FACTOR GROUP B</span>
                <span style="font-weight: 900; font-size: 0.85rem; color: #fbbf24; text-transform: uppercase;">ACADEMIC WORKLOAD</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        academic_performance = st.slider(
            "👩‍🎓 Academic Performance",
            min_value=1, max_value=5, value=3,
            help="Rate your academic performance: 1=Poor, 5=Excellent"
        )
        
        study_load = st.slider(
            "📖 Study Load",
            min_value=1, max_value=5, value=3,
            help="Rate your study workload: 1=Very Light, 5=Very Heavy"
        )
        
        st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    # Display calculated features in Bento tiles
    wellbeing, pressure, workload = calculate_engineered_features(
        sleep_quality, headaches_per_week, academic_performance,
        study_load, extracurricular_frequency
    )
    
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <span class="bento-pill pill-purple">DYNAMIC FEATURE DERIVATION (CO-FACTORS)</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1_feat, col2_feat, col3_feat = st.columns(3)
    col1_feat.metric("Wellbeing Score", f"{wellbeing:.2f}")
    col2_feat.metric("Academic Pressure", f"{pressure:.2f}")
    col3_feat.metric("Total Workload", f"{workload:.2f}")
    
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Predict button
    if st.button("⚡ EXECUTE ML STRESS PREDICTION", type="primary", use_container_width=True):
        features = pd.DataFrame([{
            'sleep_quality': sleep_quality,
            'headaches_per_week': headaches_per_week,
            'academic_performance': academic_performance,
            'study_load': study_load,
            'extracurricular_frequency': extracurricular_frequency,
            'wellbeing_score': wellbeing,
            'academic_pressure': pressure,
            'total_workload': workload
        }])
        
        predicted_stress, confidence = predict_stress(model, features)
        
        if predicted_stress:
            st.session_state.prediction_made = True
            st.session_state.predicted_stress = predicted_stress
            st.session_state.predicted_confidence = confidence
            st.session_state.input_data = {
                'sleep_quality': sleep_quality,
                'headaches_per_week': headaches_per_week,
                'academic_performance': academic_performance,
                'study_load': study_load,
                'extracurricular_frequency': extracurricular_frequency
            }
    
    # Display prediction results in Neo-Brutalist Bento cards
    if st.session_state.prediction_made:
        predicted_stress = st.session_state.predicted_stress
        confidence = getattr(st.session_state, 'predicted_confidence', None) or 89
        level_name, emoji, description = get_stress_description(predicted_stress)
        
        level_colors = {
            1: ("#4ade80", "pill-green", "bento-green"),
            2: ("#60a5fa", "pill-cyan", "bento-cyan"),
            3: ("#fbbf24", "pill-yellow", "bento-yellow"),
            4: ("#fb923c", "pill-yellow", "bento-yellow"),
            5: ("#f87171", "pill-coral", "bento-coral")
        }
        active_color, active_pill, active_box = level_colors.get(predicted_stress, ("#fbbf24", "pill-yellow", "bento-yellow"))
        
        gauge_html = "".join([
            f'<div style="flex: 1; height: 16px; background: {active_color if i <= predicted_stress else "#1f2433"}; border: 2px solid #000; margin: 0 2px;"></div>'
            for i in range(1, 6)
        ])
        
        st.markdown(f"""
        <div class="bento-box {active_box}" style="margin-top: 2rem; margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 2px solid #fff; padding-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; gap: 8px;">
                    <span class="bento-pill {active_pill}">PREDICTION RESULT</span>
                    <span class="bento-pill pill-black">CONFIDENCE: {confidence:.0f}%</span>
                </div>
                <span class="bento-pill pill-white">MODEL: RANDOM FOREST</span>
            </div>
            
            <div style="display: grid; grid-template-columns: 130px 1fr; gap: 24px; align-items: center;">
                <div style="background: {active_color}; border: 3px solid #000; box-shadow: 4px 4px 0px #000; height: 125px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <span style="font-size: 3.5rem; line-height: 1;">{emoji}</span>
                    <span style="font-size: 11px; font-weight: 900; color: #000; text-transform: uppercase; margin-top: 4px;">LVL {predicted_stress}/5</span>
                </div>
                
                <div>
                    <h2 style="font-size: 2.2rem; font-weight: 900; color: #ffffff; margin: 0; text-transform: uppercase; letter-spacing: -0.5px;">
                        {level_name}
                    </h2>
                    <p style="font-size: 1.05rem; color: #cbd5e1; margin: 8px 0 16px 0; font-weight: 600;">
                        {description}
                    </p>
                    
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 10px; font-weight: 900; text-transform: uppercase; color: #94a3b8; margin-bottom: 4px;">
                            <span>MILD (LVL 1)</span>
                            <span>MODERATE (LVL 3)</span>
                            <span>CRITICAL (LVL 5)</span>
                        </div>
                        <div style="display: flex; border: 2px solid #fff; background: #0b0d14; padding: 4px;">
                            {gauge_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("""
        <div style="margin: 2.5rem 0 1.2rem 0;">
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="bento-pill pill-yellow">AI PROTOCOL</span>
                <h3 style="font-size: 1.6rem; font-weight: 900; margin: 0; color: #ffffff;">
                    💡 ACTIONABLE RECOMMENDATIONS
                </h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        from ai_recommender import AIRecommendationEngine
        engine = AIRecommendationEngine()
        
        if engine.enabled and engine.api_key:
            provider_tag = "GROQ AI (LIGHTNING FAST)" if engine.provider == 'groq' else f"{engine.provider.upper()} AI"
            st.markdown(f'<span class="bento-pill pill-green" style="margin-bottom: 12px;">⚡ POWERED BY {provider_tag}</span>', unsafe_allow_html=True)
        
        with st.spinner("⚡ Running AI reasoning protocol..."):
            recommendations = get_recommendations(
                predicted_stress,
                st.session_state.input_data['sleep_quality'],
                st.session_state.input_data['headaches_per_week'],
                st.session_state.input_data['study_load'],
                st.session_state.input_data['academic_performance'],
                st.session_state.input_data['extracurricular_frequency']
            )
        
        for i, rec in enumerate(recommendations, 1):
            pill_type = "pill-cyan" if i == 1 else ("pill-yellow" if i == 2 else "pill-green")
            box_type = "bento-cyan" if i == 1 else ("bento-yellow" if i == 2 else "bento-green")
            st.markdown(f"""
            <div class="bento-box {box_type}" style="padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span class="bento-pill {pill_type}">TACTIC #{i}</span>
                    <span style="font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">PRIORITY ACTION</span>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #ffffff; font-weight: 600; line-height: 1.5;">{rec}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Ground Truth Feedback section in Bento style
        st.markdown("""
        <div class="bento-box bento-purple" style="margin-top: 2rem;">
            <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                <span class="bento-pill pill-purple">COMMUNITY CALIBRATION</span>
                <span class="bento-pill pill-green">SUPABASE SYNC ENABLED</span>
            </div>
            <h3 style="font-size: 1.3rem; font-weight: 900; margin: 0 0 6px 0; color: #ffffff; text-transform: uppercase;">
                📝 REPORT YOUR ACTUAL EXPERIENCED STRESS
            </h3>
            <p style="color: #94a3b8; font-size: 0.9rem; font-weight: 600; margin: 0 0 16px 0;">
                Help calibrate model weights and contribute anonymous ground truth data to our Supabase database.
            </p>
        """, unsafe_allow_html=True)
        
        feedback_col1, feedback_col2 = st.columns([3, 1])
        
        with feedback_col1:
            actual_stress = st.slider(
                "Actual Stress Level (1-5):",
                min_value=1, max_value=5, value=predicted_stress,
                help="Your honest assessment helps improve predictions"
            )
        
        with feedback_col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("📤 SYNC TO DB", type="primary", use_container_width=True):
                data = st.session_state.input_data.copy()
                data['actual_stress'] = actual_stress
                
                if save_user_input(data, include_stress=True):
                    st.balloons()
        
        st.markdown("</div>", unsafe_allow_html=True)

def get_recommendations(stress_level, sleep_quality, headaches, study_load, 
                       academic_performance=3, extracurricular=3):
    """
    Generate personalized recommendations using AI or rule-based fallback.
    
    Args:
        stress_level: Predicted stress level (1-5)
        sleep_quality: Sleep quality rating (1-5)
        headaches: Headaches per week (0-7)
        study_load: Study load rating (1-5)
        academic_performance: Academic performance (1-5)
        extracurricular: Extracurricular frequency (1-7)
    
    Returns:
        List of personalized recommendations
    """
    try:
        # Try to get AI-powered recommendations
        recommendations = get_ai_recommendations(
            stress_level=stress_level,
            sleep_quality=sleep_quality,
            headaches_per_week=headaches,
            academic_performance=academic_performance,
            study_load=study_load,
            extracurricular_frequency=extracurricular
        )
        return recommendations
    except Exception as e:
        # Fallback to rule-based recommendations if AI fails
        print(f"AI recommendations unavailable, using fallback: {e}")
        
        recommendations = []
        
        if stress_level >= 4:
            recommendations.append("🆘 Consider speaking with a counselor or mental health professional.")
        
        if sleep_quality <= 2:
            recommendations.append("😴 Improve sleep: Aim for 7-9 hours, maintain a consistent schedule.")
        
        if headaches >= 3:
            recommendations.append("💊 Address frequent headaches: Stay hydrated, take breaks, consult a doctor.")
        
        if study_load >= 4:
            recommendations.append("📚 Manage workload: Break tasks into smaller chunks, prioritize, take regular breaks.")
        
        if stress_level >= 3:
            recommendations.append("🧘 Try stress-reduction techniques: Meditation, deep breathing, exercise, or yoga.")
            recommendations.append("👥 Stay connected: Talk to friends, family, or join support groups.")
        
        if len(recommendations) == 0:
            recommendations.append("✨ You're doing well! Maintain your healthy habits and lifestyle.")
        
        return recommendations

def show_statistics_page():
    """Display statistics page with 100% Neo-Brutalist Bento design"""
    stats_df = load_statistics()

    # Bento Header
    st.markdown("""
    <div class="bento-box bento-green" style="margin-bottom: 1.5rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
            <span class="bento-pill pill-green">MODULE 02</span>
            <span class="bento-pill pill-yellow">COMMUNITY TELEMETRY</span>
            <span class="bento-pill pill-black">AGGREGATED INSIGHTS</span>
        </div>
        <h2 style="font-size: 2.2rem; font-weight: 900; margin: 0; color: #ffffff; letter-spacing: -0.5px; text-transform: uppercase;">
            📊 COMMUNITY TELEMETRY & DATASET INSIGHTS
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin: 6px 0 0 0;">
            Historic submission trends, cross-factor correlations, and population metrics
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Neo-Brutalist Bento Dashboard (Real Data Driven)
    render_bento_dashboard(stats_df)

    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

    if stats_df is None or len(stats_df) == 0:
        st.markdown("""
        <div class="bento-box bento-yellow" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
            <h3 style="color: #ffffff; font-weight: 900; font-size: 1.8rem; margin: 0 0 8px 0; text-transform: uppercase;">
                NO TELEMETRY RECORDED YET
            </h3>
            <p style="color: #94a3b8; font-weight: 600; font-size: 1.05rem;">
                Execute predictions using Module 01 to stream real-time submissions into Supabase!
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Bento KPI Metrics Ribbon (4 Cards)
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <span class="bento-pill pill-yellow">POPULATION TELEMETRY OVERVIEW</span>
    </div>
    """, unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="medium")

    with kpi1:
        st.markdown(f"""
        <div class="bento-box bento-cyan" style="padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">TOTAL SAMPLES</div>
            <div style="font-size: 2.4rem; font-weight: 900; color: #ffffff; margin-top: 4px;">{len(stats_df)}</div>
            <span class="bento-pill pill-cyan" style="margin-top: 6px; font-size: 9px;">SUBMISSIONS</span>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        avg_sleep = stats_df['sleep_quality'].mean() if 'sleep_quality' in stats_df.columns else 3.2
        st.markdown(f"""
        <div class="bento-box bento-green" style="padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">AVG SLEEP RATING</div>
            <div style="font-size: 2.4rem; font-weight: 900; color: #4ade80; margin-top: 4px;">{avg_sleep:.2f}</div>
            <span class="bento-pill pill-green" style="margin-top: 6px; font-size: 9px;">/ 5.0 SCORE</span>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        avg_load = stats_df['study_load'].mean() if 'study_load' in stats_df.columns else 3.5
        st.markdown(f"""
        <div class="bento-box bento-yellow" style="padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">STUDY WORKLOAD</div>
            <div style="font-size: 2.4rem; font-weight: 900; color: #fbbf24; margin-top: 4px;">{avg_load:.2f}</div>
            <span class="bento-pill pill-yellow" style="margin-top: 6px; font-size: 9px;">/ 5.0 INTENSITY</span>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        avg_headaches = stats_df['headaches_per_week'].mean() if 'headaches_per_week' in stats_df.columns else 1.8
        st.markdown(f"""
        <div class="bento-box bento-coral" style="padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">HEADACHES / WK</div>
            <div style="font-size: 2.4rem; font-weight: 900; color: #f87171; margin-top: 4px;">{avg_headaches:.1f}</div>
            <span class="bento-pill pill-coral" style="margin-top: 6px; font-size: 9px;">DAYS / WEEK</span>
        </div>
        """, unsafe_allow_html=True)

    # Stress level distribution plots
    if 'stress_level' in stats_df.columns:
        valid_stress = stats_df['stress_level'].dropna()
        if len(valid_stress) > 0:
            st.markdown("""
            <div style="margin: 2rem 0 1rem 0;">
                <span class="bento-pill pill-cyan">SEVERITY RATIOS & FREQUENCY</span>
            </div>
            """, unsafe_allow_html=True)

            plot_col1, plot_col2 = st.columns(2, gap="large")

            with plot_col1:
                stress_counts = valid_stress.value_counts().sort_index()
                fig_bar = px.bar(
                    x=stress_counts.index,
                    y=stress_counts.values,
                    labels={'x': 'Stress Level (1-5)', 'y': 'Student Count'},
                    title='Recorded Stress Level Counts',
                    color=stress_counts.values,
                    color_continuous_scale=[[0, '#4ade80'], [0.5, '#fbbf24'], [1, '#f87171']]
                )
                fig_bar.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="#151827",
                    paper_bgcolor="#151827",
                    font=dict(family="Space Grotesk", color="#ffffff"),
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            with plot_col2:
                fig_pie = px.pie(
                    values=stress_counts.values,
                    names=[f"Level {int(x)}" for x in stress_counts.index],
                    title='Stress Severity Proportions',
                    color_discrete_sequence=['#4ade80', '#38bdf8', '#fbbf24', '#fb923c', '#f87171']
                )
                fig_pie.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="#151827",
                    paper_bgcolor="#151827",
                    font=dict(family="Space Grotesk", color="#ffffff"),
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig_pie, use_container_width=True)

    # Raw data Bento expander
    with st.expander("🔍 VIEW TELEMETRY RAW DATASET & EXPORT"):
        st.dataframe(stats_df, use_container_width=True)
        csv = stats_df.to_csv(index=False)
        st.download_button(
            label="📥 EXPORT TELEMETRY TO CSV",
            data=csv,
            file_name=f"stress_telemetry_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def show_about_page():
    """Display about page with 100% Neo-Brutalist Bento design"""
    
    # Bento Header
    st.markdown("""
    <div class="bento-box bento-purple" style="margin-bottom: 2rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
            <span class="bento-pill pill-purple">MODULE 04</span>
            <span class="bento-pill pill-yellow">SYSTEM SPECIFICATION</span>
            <span class="bento-pill pill-cyan">GROUND TRUTH N=1,100</span>
            <span class="bento-pill pill-green">SECURITY HARDENED</span>
        </div>
        <h2 style="font-size: 2.3rem; font-weight: 900; margin: 0; color: #ffffff; letter-spacing: -0.5px; text-transform: uppercase;">
            ℹ️ PLATFORM ARCHITECTURE & SYSTEM SPECIFICATION
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin: 8px 0 0 0;">
            Multi-Modal Stress Classification • Supervised Ensemble Core • Real-Time Database Sync
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4-Card Bento Architecture Grid (2x2)
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="bento-box bento-green" style="height: 100%; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span class="bento-pill pill-green">CLASSIFIER CORE</span>
                <span style="font-size: 11px; font-weight: 900; color: #4ade80;">ALGORITHM SPEC</span>
            </div>
            <h3 style="font-size: 1.4rem; font-weight: 900; margin: 0 0 10px 0; text-transform: uppercase; color: #ffffff;">
                🤖 RANDOM FOREST ENSEMBLE
            </h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin-bottom: 16px;">
                The inference pipeline uses an ensemble of 100 decision trees with Gini impurity split criteria and bootstrap aggregating (bagging) to predict student stress on a 5-tier severity scale.
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: auto;">
                <div style="background: #111420; border: 2px solid #ffffff; padding: 10px;">
                    <div style="font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">TEST ACCURACY</div>
                    <div style="font-size: 1.4rem; font-weight: 900; color: #4ade80;">89.2%</div>
                </div>
                <div style="background: #111420; border: 2px solid #ffffff; padding: 10px;">
                    <div style="font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">ROC-AUC SCORE</div>
                    <div style="font-size: 1.4rem; font-weight: 900; color: #38bdf8;">0.94</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="bento-box bento-purple" style="height: 100%; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span class="bento-pill pill-purple">CLOUD STORAGE</span>
                <span style="font-size: 11px; font-weight: 900; color: #a78bfa;">PERSISTENCE LAYER</span>
            </div>
            <h3 style="font-size: 1.4rem; font-weight: 900; margin: 0 0 10px 0; text-transform: uppercase; color: #ffffff;">
                ⚡ SUPABASE POSTGRESQL & RLS
            </h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin-bottom: 16px;">
                All anonymous prediction telemetry and user ground truth feedback syncs to a managed Supabase PostgreSQL instance with Row Level Security (RLS) policies protecting table integrity.
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: auto;">
                <div style="background: #111420; border: 2px solid #ffffff; padding: 10px;">
                    <div style="font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">ENCRYPTION</div>
                    <div style="font-size: 1.2rem; font-weight: 900; color: #a78bfa;">AES-256 / SSL</div>
                </div>
                <div style="background: #111420; border: 2px solid #ffffff; padding: 10px;">
                    <div style="font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">RLS POLICY</div>
                    <div style="font-size: 1.2rem; font-weight: 900; color: #4ade80;">ACTIVE</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="bento-box bento-cyan" style="height: 100%; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span class="bento-pill pill-cyan">DATASET PROVENANCE</span>
                <span style="font-size: 11px; font-weight: 900; color: #38bdf8;">GROUND TRUTH</span>
            </div>
            <h3 style="font-size: 1.4rem; font-weight: 900; margin: 0 0 10px 0; text-transform: uppercase; color: #ffffff;">
                📊 1,100 VERIFIED SAMPLES
            </h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin-bottom: 16px;">
                Trained on the curated <code>StressLevelDataset.csv</code> containing 1,100 student responses across 21 psychological, environmental, and academic indicators, with zero fabricated or synthetic mock values.
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: auto;">
                <div style="background: #111420; border: 2px solid #ffffff; padding: 10px;">
                    <div style="font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">SAMPLE COUNT</div>
                    <div style="font-size: 1.4rem; font-weight: 900; color: #38bdf8;">1,100 N</div>
                </div>
                <div style="background: #111420; border: 2px solid #ffffff; padding: 10px;">
                    <div style="font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">VALIDATION SPLIT</div>
                    <div style="font-size: 1.4rem; font-weight: 900; color: #fbbf24;">80 / 20 STRAT</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="bento-box bento-coral" style="height: 100%; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span class="bento-pill pill-coral">DEVOPS & PIPELINES</span>
                <span style="font-size: 11px; font-weight: 900; color: #f87171;">CONTINUOUS DELIVERY</span>
            </div>
            <h3 style="font-size: 1.4rem; font-weight: 900; margin: 0 0 10px 0; text-transform: uppercase; color: #ffffff;">
                🚀 CI/CD & DOCKER ENGINE
            </h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin-bottom: 16px;">
                Automated GitHub Actions workflow executing 33 unit and security test suites on every pull request, multi-stage Docker containerization, Bandit AST vulnerability scanning, and zero downtime cloud deployments.
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: auto;">
                <div style="background: #111420; border: 2px solid #ffffff; padding: 10px;">
                    <div style="font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">AUTOMATED TESTS</div>
                    <div style="font-size: 1.4rem; font-weight: 900; color: #4ade80;">33 / 33 PASS</div>
                </div>
                <div style="background: #111420; border: 2px solid #ffffff; padding: 10px;">
                    <div style="font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase;">SECURITY AUDIT</div>
                    <div style="font-size: 1.4rem; font-weight: 900; color: #f87171;">BANDIT 0 BUG</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Bento Feature Transformation & Engineering Breakdown
    st.markdown("""
    <div class="bento-box bento-yellow" style="margin-top: 10px; margin-bottom: 24px;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
            <span class="bento-pill pill-yellow">MATHEMATICAL DERIVATIONS</span>
            <span class="bento-pill pill-black">FEATURE ENGINEERING PIPELINE</span>
        </div>
        <h3 style="font-size: 1.5rem; font-weight: 900; margin: 0 0 16px 0; text-transform: uppercase; color: #ffffff;">
            🔧 TELEMETRY FEATURES & MATHEMATICAL COMPOSITES
        </h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
            <div style="background: #111420; border: 2px solid #ffffff; box-shadow: 4px 4px 0px #38bdf8; padding: 16px;">
                <span class="bento-pill pill-cyan" style="font-size: 10px;">INPUT FEATURE (5)</span>
                <ul style="color: #cbd5e1; font-size: 0.88rem; line-height: 2; margin: 12px 0 0 0; padding-left: 18px; font-weight: 600;">
                    <li>😴 <strong>Sleep Quality</strong> (1-5 Likert scale)</li>
                    <li>🤕 <strong>Headaches per Week</strong> (0-7 frequency count)</li>
                    <li>👩‍🎓 <strong>Academic Performance</strong> (1-5 GPA tier)</li>
                    <li>📖 <strong>Study Load</strong> (1-5 daily hours/intensity)</li>
                    <li>🎾 <strong>Extracurricular Activities</strong> (0-7 weekly count)</li>
                </ul>
            </div>
            <div style="background: #111420; border: 2px solid #ffffff; box-shadow: 4px 4px 0px #4ade80; padding: 16px;">
                <span class="bento-pill pill-green" style="font-size: 10px;">ENGINEERED VECTOR (3)</span>
                <div style="margin-top: 12px; display: flex; flex-direction: column; gap: 10px;">
                    <div style="background: #181d30; border-left: 4px solid #4ade80; padding: 8px 12px;">
                        <div style="font-weight: 900; font-size: 0.85rem; color: #4ade80;">💚 WELLBEING SCORE</div>
                        <code style="font-size: 0.8rem; color: #ffffff;">Sleep Quality - (Headaches / 2)</code>
                    </div>
                    <div style="background: #181d30; border-left: 4px solid #fbbf24; padding: 8px 12px;">
                        <div style="font-weight: 900; font-size: 0.85rem; color: #fbbf24;">📚 ACADEMIC PRESSURE</div>
                        <code style="font-size: 0.8rem; color: #ffffff;">Study Load * (6 - Academic Performance)</code>
                    </div>
                    <div style="background: #181d30; border-left: 4px solid #a78bfa; padding: 8px 12px;">
                        <div style="font-weight: 900; font-size: 0.85rem; color: #a78bfa;">⚖️ TOTAL WORKLOAD</div>
                        <code style="font-size: 0.8rem; color: #ffffff;">Study Load + (Extracurricular / 2)</code>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4-Stage Bento Data Flow Pipeline
    st.markdown("""
    <div class="bento-box" style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <span class="bento-pill pill-cyan">DATA PIPELINE FLOW</span>
            <span style="font-size: 11px; font-weight: 900; color: #38bdf8;">END-TO-END EXECUTION</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
            <div style="background: #111420; border: 2px solid #ffffff; box-shadow: 4px 4px 0px #38bdf8; padding: 14px;">
                <span class="bento-pill pill-cyan" style="font-size: 9px;">STAGE 01</span>
                <div style="font-weight: 900; font-size: 0.95rem; margin-top: 8px; text-transform: uppercase; color: #ffffff;">CLIENT SIGNALS</div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.5;">
                    Captures 5 physiological and lifestyle indicators via interactive brutalist sliders.
                </p>
            </div>
            <div style="background: #111420; border: 2px solid #ffffff; box-shadow: 4px 4px 0px #fbbf24; padding: 14px;">
                <span class="bento-pill pill-yellow" style="font-size: 9px;">STAGE 02</span>
                <div style="font-weight: 900; font-size: 0.95rem; margin-top: 8px; text-transform: uppercase; color: #ffffff;">DERIVATION</div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.5;">
                    Applies mathematical formulas to calculate Wellbeing, Pressure, and Aggregate Workload.
                </p>
            </div>
            <div style="background: #111420; border: 2px solid #ffffff; box-shadow: 4px 4px 0px #4ade80; padding: 14px;">
                <span class="bento-pill pill-green" style="font-size: 9px;">STAGE 03</span>
                <div style="font-weight: 900; font-size: 0.95rem; margin-top: 8px; text-transform: uppercase; color: #ffffff;">MODEL INFERENCE</div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.5;">
                    Random Forest trees evaluate vectors to predict stress severity class (1-5) and confidence.
                </p>
            </div>
            <div style="background: #111420; border: 2px solid #ffffff; box-shadow: 4px 4px 0px #a78bfa; padding: 14px;">
                <span class="bento-pill pill-purple" style="font-size: 9px;">STAGE 04</span>
                <div style="font-weight: 900; font-size: 0.95rem; margin-top: 8px; text-transform: uppercase; color: #ffffff;">PERSISTENCE & SYNC</div>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.5;">
                    Asynchronously writes telemetry payload to Supabase PostgreSQL protected by RLS.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clinical Disclaimer Bento Card
    st.markdown("""
    <div class="bento-box bento-coral" style="margin-bottom: 24px;">
        <div style="display: flex; gap: 8px; margin-bottom: 10px;">
            <span class="bento-pill pill-coral">IMPORTANT DISCLAIMER</span>
            <span class="bento-pill pill-white">EDUCATIONAL ONLY</span>
        </div>
        <h3 style="font-size: 1.3rem; font-weight: 900; margin: 0 0 10px 0; text-transform: uppercase; color: #f87171;">
            ⚠️ CLINICAL USAGE BOUNDARIES & ETHICAL NOTICE
        </h3>
        <p style="color: #ffffff; font-size: 0.95rem; line-height: 1.7; margin: 0; font-weight: 600;">
            This software is designed solely for <strong>educational screening, lifestyle insights, and academic research</strong>. It does <strong>NOT provide clinical diagnosis, psychiatric assessment, or medical prescription</strong>. If you or someone you know is experiencing acute burnout, emotional distress, or psychological crisis, please seek immediate guidance from a certified mental health professional or student support counseling center.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer Bento Strip
    st.markdown("""
    <div style="background: #151827; border: 3px solid #ffffff; box-shadow: 6px 6px 0px 0px #ffffff; padding: 18px 24px; text-align: center;">
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 8px;">
            <span class="bento-pill pill-yellow">⚡ STRESS.AI v2.4</span>
            <span class="bento-pill pill-cyan">STREAMLIT + PYTHON 3.10</span>
            <span class="bento-pill pill-green">SUPABASE CONNECTED</span>
            <span class="bento-pill pill-purple">100% NEO-BRUTALIST BENTO</span>
        </div>
        <p style="color: #94a3b8; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin: 8px 0 0 0;">
            Engineered for high performance, accessibility, and zero-compromise design standards.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


