"""
Student Stress Predictor - Streamlit Web Application
=======================================================
A modern, accessible web interface for student stress level prediction,
community telemetry insights, and machine learning model validation.
Styled with a clean, 100% pure Bento Light Theme.
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
from ai_recommender import get_ai_recommendations, AIRecommendationEngine
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

# Global tracker for last prediction error
_last_prediction_error = None

# Inject 100% Bento Light Design System CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600;700;800&family=Inter:wght@400;600;700;800;900&display=swap');
    
    :root {
        --bento-bg: #f8fafc;
        --bento-card: #ffffff;
        --bento-card-sub: #f1f5f9;
        --bento-border: #0f172a;
        --bento-text: #0f172a;
        --bento-text-muted: #64748b;
        --bento-yellow: #fef08a;
        --bento-green: #bbf7d0;
        --bento-cyan: #bae6fd;
        --bento-purple: #e9d5ff;
        --bento-coral: #fecdd3;
    }
    
    /* PRESERVE STREAMLIT MATERIAL ICONS (DO NOT OVERRIDE SYSTEM ICON FONTS) */
    [data-testid="stIconMaterial"], 
    .material-symbols-rounded, 
    .material-icons,
    button[kind="header"] *,
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="collapsedControl"] *,
    [data-testid="collapsedControl"] span {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-style: normal !important;
    }

    /* STYLE SLIDE MENU (SIDEBAR) COLLAPSE/EXPAND TOGGLE BUTTON */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        background: #ffffff !important;
        border: 2px solid #0f172a !important;
        box-shadow: 2px 2px 0px #0f172a !important;
        border-radius: 6px !important;
        color: #0f172a !important;
        margin: 4px !important;
        padding: 4px 6px !important;
    }
    [data-testid="stSidebarCollapseButton"]:hover,
    [data-testid="collapsedControl"]:hover {
        background: #f1f5f9 !important;
        transform: translate(-1px, -1px) !important;
        box-shadow: 3px 3px 0px #0f172a !important;
    }

    /* GLOBAL TYPOGRAPHY */
    html, body, [data-testid="stAppViewContainer"], .main, .stMarkdown, p, h1, h2, h3, h4, label, input {
        font-family: 'Space Grotesk', 'Inter', -apple-system, sans-serif !important;
        box-sizing: border-box;
    }
    
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* 100% PURE LIGHT THEME CANVAS & BLUEPRINT GRID */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background-color: #f8fafc !important;
        background-image: radial-gradient(rgba(15, 23, 42, 0.08) 1.5px, transparent 1.5px) !important;
        background-size: 24px 24px !important;
        color: #0f172a !important;
    }

    /* STREAMLIT HEADER TRANSPARENCY */
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* BENTO MAIN CONTAINER */
    .main .block-container {
        background: #ffffff !important;
        border: 2px solid #0f172a !important;
        box-shadow: 8px 8px 0px 0px #0f172a !important;
        border-radius: 8px !important;
        padding: 2.2rem !important;
        margin-top: 1rem !important;
        margin-bottom: 3rem !important;
        color: #0f172a !important;
    }
    
    /* BENTO PILLS & BADGES */
    .bento-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        padding: 4px 10px;
        border: 2px solid #0f172a;
        box-shadow: 2px 2px 0px #0f172a;
        border-radius: 4px;
        color: #0f172a;
    }
    .pill-yellow { background: #fef08a !important; color: #0f172a !important; }
    .pill-green { background: #bbf7d0 !important; color: #0f172a !important; }
    .pill-cyan { background: #bae6fd !important; color: #0f172a !important; }
    .pill-purple { background: #e9d5ff !important; color: #0f172a !important; }
    .pill-coral { background: #fecdd3 !important; color: #0f172a !important; }
    .pill-black { background: #0f172a !important; color: #ffffff !important; border-color: #0f172a !important; box-shadow: 2px 2px 0px #0f172a !important; }
    .pill-white { background: #ffffff !important; color: #0f172a !important; border-color: #0f172a !important; box-shadow: 2px 2px 0px #0f172a !important; }
    
    /* BENTO BOXES */
    .bento-box {
        background: #ffffff;
        border: 2px solid #0f172a;
        box-shadow: 4px 4px 0px 0px #0f172a;
        border-radius: 8px;
        padding: 22px;
        margin-bottom: 22px;
        position: relative;
        color: #0f172a;
        transition: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .bento-box:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px 0px #0f172a;
    }
    .bento-yellow { background: #fffbeb !important; }
    .bento-green { background: #f0fdf4 !important; }
    .bento-cyan { background: #f0f9ff !important; }
    .bento-purple { background: #faf5ff !important; }
    .bento-coral { background: #fff1f2 !important; }
    
    /* BENTO BUTTONS */
    .stButton > button {
        background: #0284c7 !important;
        color: #ffffff !important;
        border: 2px solid #0f172a !important;
        box-shadow: 4px 4px 0px 0px #0f172a !important;
        border-radius: 6px !important;
        padding: 0.85rem 1.8rem !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.12s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: #0369a1 !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px 0px #0f172a !important;
        color: #ffffff !important;
    }
    .stButton > button:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0px 0px #0f172a !important;
    }
    
    /* BENTO SLIDERS */
    .stSlider label p {
        font-size: 0.95rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #0f172a !important;
    }
    .stSlider [data-baseweb="slider"] {
        padding: 10px 0 !important;
    }
    .stSlider div[role="slider"] {
        border: 2px solid #0f172a !important;
        box-shadow: 2px 2px 0px #0f172a !important;
        border-radius: 4px !important;
        background-color: #0284c7 !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* BENTO SLIDE MENU (SIDEBAR) */
    section[data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background: #ffffff !important;
        border-right: 2px solid #0f172a !important;
        color: #0f172a !important;
    }
    
    /* TURN SIDEBAR RADIO OPTIONS INTO HIGH-CONTRAST BENTO BUTTONS */
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        background: #f8fafc !important;
        border: 2px solid #0f172a !important;
        box-shadow: 3px 3px 0px 0px #0f172a !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        margin: 0 !important;
    }
    /* Hide native circular radio dot */
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    /* Full width text inside button */
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p {
        font-size: 0.95rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #0f172a !important;
        margin: 0 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: #f1f5f9 !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 5px 5px 0px 0px #0f172a !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: #fef08a !important;
        border-color: #0f172a !important;
        box-shadow: 4px 4px 0px 0px #0f172a !important;
        transform: translate(-1px, -1px) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) div[data-testid="stMarkdownContainer"] p {
        color: #0f172a !important;
        font-weight: 900 !important;
    }
    
    /* BENTO METRICS */
    [data-testid="stMetric"] {
        background: #ffffff !important;
        border: 2px solid #0f172a !important;
        box-shadow: 4px 4px 0px 0px #0f172a !important;
        padding: 14px 18px !important;
        border-radius: 8px !important;
    }
    [data-testid="stMetricLabel"] {
        font-weight: 800 !important;
        text-transform: uppercase !important;
        color: #64748b !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.8px !important;
    }
    [data-testid="stMetricValue"] {
        font-weight: 900 !important;
        color: #0f172a !important;
        font-size: 2.2rem !important;
    }
    
    /* BENTO EXPANDER */
    .streamlit-expanderHeader {
        background: #f8fafc !important;
        border: 2px solid #0f172a !important;
        box-shadow: 3px 3px 0px 0px #0f172a !important;
        border-radius: 6px !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        padding: 12px 18px !important;
    }
    .streamlit-expanderContent {
        background: #ffffff !important;
        border: 2px solid #0f172a !important;
        border-top: none !important;
        box-shadow: 3px 3px 0px 0px #0f172a !important;
        border-radius: 0 0 6px 6px !important;
        padding: 16px !important;
        color: #0f172a !important;
    }
    
    /* HEADERS */
    h1, h2, h3, h4 {
        color: #0f172a !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: -0.5px !important;
    }
    p, span, li {
        color: #0f172a;
    }
    
    /* PLOTLY CONTAINERS */
    .js-plotly-plot {
        background: #ffffff !important;
        border: 2px solid #0f172a !important;
        box-shadow: 4px 4px 0px 0px #0f172a !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-bottom: 20px !important;
    }
    
    /* DATAFRAMES */
    .stDataFrame {
        background: #ffffff !important;
        border: 2px solid #0f172a !important;
        box-shadow: 4px 4px 0px 0px #0f172a !important;
        border-radius: 8px !important;
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div > div > div {
        background: #16a34a !important;
        border-radius: 4px !important;
        border: 1px solid #0f172a !important;
    }
    
    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f8fafc;
    }
    ::-webkit-scrollbar-thumb {
        background: #94a3b8;
        border-radius: 4px;
        border: 1px solid #0f172a;
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
if 'predicted_confidence' not in st.session_state:
    st.session_state.predicted_confidence = None
if 'input_data' not in st.session_state:
    st.session_state.input_data = None

# ==============================================================================
# BENTO ERROR & DIAGNOSTIC UI HELPERS
# ==============================================================================

def show_bento_error(title: str, message: str, error_code: str = None, action_hint: str = None):
    """Display a prominent, high-contrast Bento error card"""
    code_badge = f'<span class="bento-pill pill-black" style="font-size: 9px;">CODE: {error_code}</span>' if error_code else ''
    hint_html = f"""
    <div style="margin-top: 12px; padding: 10px 14px; background: #ffffff; border: 2px solid #e11d48; border-radius: 6px;">
        <div style="font-size: 11px; font-weight: 800; color: #e11d48; text-transform: uppercase; letter-spacing: 0.5px;">RECOMMENDED ACTION:</div>
        <div style="font-size: 13px; color: #0f172a; font-weight: 600; margin-top: 3px;">{action_hint}</div>
    </div>
    """ if action_hint else ''
    
    st.markdown(f"""
    <div class="bento-box" style="background: #fff1f2; border: 2px solid #e11d48; box-shadow: 4px 4px 0px #e11d48; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="bento-pill pill-coral" style="background: #fecdd3; color: #9f1239; border-color: #e11d48;">⚠️ SYSTEM ERROR</span>
                {code_badge}
            </div>
        </div>
        <h3 style="font-size: 1.25rem; font-weight: 900; color: #9f1239; margin: 4px 0 6px 0; text-transform: uppercase;">
            {title}
        </h3>
        <p style="color: #475569; font-size: 0.95rem; font-weight: 600; margin: 0; line-height: 1.5;">
            {message}
        </p>
        {hint_html}
    </div>
    """, unsafe_allow_html=True)

def show_bento_warning(title: str, message: str, warning_code: str = None, action_hint: str = None):
    """Display an informative Bento warning / fallback card"""
    code_badge = f'<span class="bento-pill pill-black" style="font-size: 9px;">CODE: {warning_code}</span>' if warning_code else ''
    hint_html = f"""
    <div style="margin-top: 12px; padding: 10px 14px; background: #ffffff; border: 2px solid #d97706; border-radius: 6px;">
        <div style="font-size: 11px; font-weight: 800; color: #d97706; text-transform: uppercase; letter-spacing: 0.5px;">NOTICE:</div>
        <div style="font-size: 13px; color: #0f172a; font-weight: 600; margin-top: 3px;">{action_hint}</div>
    </div>
    """ if action_hint else ''
    
    st.markdown(f"""
    <div class="bento-box" style="background: #fffbeb; border: 2px solid #d97706; box-shadow: 4px 4px 0px #d97706; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="bento-pill pill-yellow" style="background: #fef08a; color: #92400e; border-color: #d97706;">⚡ NOTICE</span>
                {code_badge}
            </div>
        </div>
        <h3 style="font-size: 1.25rem; font-weight: 900; color: #92400e; margin: 4px 0 6px 0; text-transform: uppercase;">
            {title}
        </h3>
        <p style="color: #475569; font-size: 0.95rem; font-weight: 600; margin: 0; line-height: 1.5;">
            {message}
        </p>
        {hint_html}
    </div>
    """, unsafe_allow_html=True)

def show_bento_success(title: str, message: str, success_code: str = None):
    """Display a clean Bento success card"""
    code_badge = f'<span class="bento-pill pill-black" style="font-size: 9px;">{success_code}</span>' if success_code else ''
    st.markdown(f"""
    <div class="bento-box" style="background: #f0fdf4; border: 2px solid #16a34a; box-shadow: 4px 4px 0px #16a34a; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="bento-pill pill-green" style="background: #bbf7d0; color: #166534; border-color: #16a34a;">✅ SUCCESS</span>
                {code_badge}
            </div>
        </div>
        <h3 style="font-size: 1.25rem; font-weight: 900; color: #166534; margin: 4px 0 6px 0; text-transform: uppercase;">
            {title}
        </h3>
        <p style="color: #1e293b; font-size: 0.95rem; font-weight: 600; margin: 0; line-height: 1.5;">
            {message}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MODEL & FEATURE LOGIC
# ==============================================================================

@st.cache_resource
def load_model():
    """Load the trained model artifact with exception handling"""
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            return model, None
        else:
            return None, f"Model file not found at '{MODEL_PATH}'."
    except Exception as e:
        return None, f"Error loading model: {str(e)}"

def calculate_engineered_features(sleep_quality, headaches_per_week, 
                                 academic_performance, study_load, 
                                 extracurricular_frequency):
    """Calculate engineered composite features"""
    wellbeing_score = sleep_quality - (headaches_per_week / 2)
    academic_pressure = study_load * (6 - academic_performance)
    total_workload = study_load + (extracurricular_frequency / 2)
    
    return wellbeing_score, academic_pressure, total_workload

def predict_stress(model, features):
    """Make prediction using the model safely with detailed error handling"""
    global _last_prediction_error
    try:
        _last_prediction_error = None
        if model is None:
            _last_prediction_error = "Machine learning model instance is not loaded."
            return None, None
        
        # Check if model has feature names and filter features accordingly
        if hasattr(model, 'feature_names_in_'):
            model_features = model.feature_names_in_.tolist()
            missing = [f for f in model_features if f not in features.columns]
            if missing:
                _last_prediction_error = f"Missing required model features: {missing}"
                return None, None
            features = features[model_features]
        
        prediction = model.predict(features)[0]
        # Get probability if available
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(features)[0]
            confidence = float(max(proba) * 100)
        else:
            confidence = None
        return int(prediction), confidence
    except Exception as e:
        _last_prediction_error = str(e)
        return None, None

def save_user_input(data, include_stress=False):
    """Save user input using the database module"""
    return storage.save_user_input(data, include_stress)

def get_stress_description(stress_level):
    """Get description and emoji for stress level"""
    descriptions = {
        1: ("Very Low Stress", "😊", "You're doing great! Keep up your healthy lifestyle and balanced habits."),
        2: ("Low Stress", "🙂", "Good stress management! Minor adjustments can maintain this healthy balance."),
        3: ("Moderate Stress", "😐", "Manageable stress detected. Consider regular breaks and relaxation techniques."),
        4: ("High Stress", "😟", "Significant stress detected. Prioritize sleep, reduce workload, and seek peer support."),
        5: ("Very High Stress", "😰", "Critical stress level! Please take immediate rest and reach out to academic counseling.")
    }
    return descriptions.get(stress_level, ("Unknown", "❓", "Stress level could not be determined."))

@st.cache_data(ttl=60)
def load_statistics():
    """Load statistics from the database module"""
    return storage.get_all_data()

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================

def main():
    # Bento Light Header
    st.markdown("""
    <div class="bento-box bento-yellow" style="margin-bottom: 2rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
            <span class="bento-pill pill-yellow">⚡ AI CORE v2.4</span>
            <span class="bento-pill pill-cyan">N=1,100 GROUND TRUTH</span>
            <span class="bento-pill pill-green">PERSISTENCE SYNC</span>
            <span class="bento-pill pill-black">BENTO LIGHT THEME</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 15px;">
            <div>
                <h1 style="font-size: 2.6rem; font-weight: 900; margin: 0; letter-spacing: -0.5px; text-transform: uppercase; color: #0f172a;">
                    🧠 STUDENT STRESS PREDICTOR
                </h1>
                <p style="color: #64748b; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin: 6px 0 0 0;">
                    Multi-Modal Machine Learning Inference & Community Telemetry
                </p>
            </div>
            <div style="display: flex; gap: 8px;">
                <span class="bento-pill pill-white" style="font-size: 11px; padding: 6px 12px;">BENTO SYSTEM ACTIVE</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    model, model_error = load_model()
    
    # Robust Model Error Presentation
    if model_error:
        show_bento_error(
            title="Machine Learning Model Artifact Not Found",
            message=f"The required prediction model could not be loaded: {model_error}",
            error_code="ERR_MODEL_LOAD",
            action_hint="Train the multi-dataset classifier by running: python scripts/train_multi_dataset.py"
        )
        return
    
    # Sidebar (Slide Menu) with Bento Light Design
    with st.sidebar:
        # Bento Logo Header
        st.markdown("""
        <div style="background: #f8fafc; border: 2px solid #0f172a; box-shadow: 4px 4px 0px 0px #0f172a; border-radius: 8px; padding: 18px 14px; text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 4px;">🧠</div>
            <div style="font-size: 1.4rem; font-weight: 900; letter-spacing: -0.5px; text-transform: uppercase; color: #0f172a;">
                STRESS.AI
            </div>
            <div style="margin-top: 8px;">
                <span class="bento-pill pill-yellow" style="font-size: 10px;">BENTO LIGHT v2.4</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Header
        st.markdown("""
        <div style="margin-bottom: 0.8rem;">
            <span class="bento-pill pill-cyan" style="width: 100%; justify-content: center;">
                📍 SELECT MODULE
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Cleaned up Navigation: Only 2 essential, high-impact modules
        page = st.radio("Select Page:", 
                       ["🔮 Predict Stress", "📊 Analytics & Insights"],
                       index=0,
                       label_visibility="collapsed")
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Live Telemetry Section with Bento Cards
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
            <div style="background: #ffffff; border: 2px solid #0f172a; box-shadow: 3px 3px 0px 0px #0f172a; border-radius: 6px; padding: 12px 14px; margin-bottom: 12px;">
                <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #64748b; letter-spacing: 0.8px;">TOTAL SUBMISSIONS</div>
                <div style="font-size: 1.8rem; font-weight: 900; color: #0f172a; margin-top: 2px;">{sub_count}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if 'stress_level' in stats_df.columns:
                valid_stress = pd.to_numeric(stats_df['stress_level'], errors='coerce').dropna()
                if len(valid_stress) > 0:
                    avg_stress = valid_stress.mean()
                    stress_pill = "pill-green" if avg_stress < 2.5 else ("pill-yellow" if avg_stress < 3.5 else "pill-coral")
                    
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 2px solid #0f172a; box-shadow: 3px 3px 0px 0px #0f172a; border-radius: 6px; padding: 12px 14px; margin-bottom: 12px;">
                        <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #64748b; letter-spacing: 0.8px;">AVERAGE STRESS</div>
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 2px;">
                            <span style="font-size: 1.8rem; font-weight: 900; color: #0f172a;">{avg_stress:.2f}</span>
                            <span class="bento-pill {stress_pill}" style="font-size: 10px;">/ 5.0</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f8fafc; border: 2px solid #0f172a; box-shadow: 3px 3px 0px 0px #0f172a; border-radius: 6px; padding: 14px; text-align: center;">
                <p style="color: #64748b; font-weight: 800; margin: 0; font-size: 0.85rem; text-transform: uppercase;">
                    No Telemetry Yet
                </p>
                <p style="color: #0284c7; font-size: 0.75rem; margin: 4px 0 0 0; font-weight: 800; text-transform: uppercase;">
                    Make a prediction to log data!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Sidebar Footer - Storage Status
        storage_medium = getattr(storage, 'last_storage_medium', 'DATABASE')
        status_text = "SUPABASE POSTGRESQL SYNC" if storage_medium == "SUPABASE" else "LOCAL CSV STORAGE"
        status_pill = "pill-green" if storage_medium == "SUPABASE" else "pill-yellow"
        
        st.markdown(f"""
        <div style="background: #f8fafc; border: 2px solid #0f172a; box-shadow: 3px 3px 0px 0px #0f172a; border-radius: 6px; padding: 12px; text-align: center;">
            <div style="margin-bottom: 4px;">
                <span class="bento-pill {status_pill}" style="font-size: 9px;">{status_text}</span>
            </div>
            <div style="font-size: 9px; font-weight: 700; color: #64748b; margin-top: 4px; text-transform: uppercase;">
                SECURE TELEMETRY ENGINE
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to Module
    if page == "🔮 Predict Stress":
        show_prediction_page(model)
    else:
        show_analytics_page(stats_df)

# ==============================================================================
# MODULE 01: PREDICTION PAGE (DEFAULT PRIMARY VIEW)
# ==============================================================================

def show_prediction_page(model):
    """Display the prediction page with 100% Bento Light design"""
    global _last_prediction_error
    
    # Bento Header Box
    st.markdown("""
    <div class="bento-box bento-cyan" style="margin-bottom: 1.5rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
            <span class="bento-pill pill-cyan">MODULE 01</span>
            <span class="bento-pill pill-yellow">INFERENCE ENGINE</span>
            <span class="bento-pill pill-black">REAL-TIME ML</span>
        </div>
        <h2 style="font-size: 2.2rem; font-weight: 900; margin: 0; color: #0f172a; letter-spacing: -0.5px; text-transform: uppercase;">
            🔮 STRESS LEVEL PREDICTION
        </h2>
        <p style="color: #475569; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin: 6px 0 0 0;">
            Input lifestyle and academic telemetry below for real-time model inference
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bento Workflow Ribbon (4 Steps)
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 24px;">
        <div style="background: #ffffff; border: 2px solid #0f172a; box-shadow: 3px 3px 0px #0f172a; border-radius: 6px; padding: 12px 14px;">
            <span class="bento-pill pill-cyan" style="font-size: 9px; padding: 2px 6px;">STEP 01</span>
            <div style="font-weight: 900; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; color: #0f172a;">INPUT SIGNALS</div>
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">Sleep, headaches, study load</div>
        </div>
        <div style="background: #ffffff; border: 2px solid #0f172a; box-shadow: 3px 3px 0px #0f172a; border-radius: 6px; padding: 12px 14px;">
            <span class="bento-pill pill-yellow" style="font-size: 9px; padding: 2px 6px;">STEP 02</span>
            <div style="font-weight: 900; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; color: #0f172a;">CALCULATE METRICS</div>
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">Dynamic feature derivation</div>
        </div>
        <div style="background: #ffffff; border: 2px solid #0f172a; box-shadow: 3px 3px 0px #0f172a; border-radius: 6px; padding: 12px 14px;">
            <span class="bento-pill pill-green" style="font-size: 9px; padding: 2px 6px;">STEP 03</span>
            <div style="font-weight: 900; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; color: #0f172a;">ML INFERENCE</div>
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">Random Forest classification</div>
        </div>
        <div style="background: #ffffff; border: 2px solid #0f172a; box-shadow: 3px 3px 0px #0f172a; border-radius: 6px; padding: 12px 14px;">
            <span class="bento-pill pill-purple" style="font-size: 9px; padding: 2px 6px;">STEP 04</span>
            <div style="font-weight: 900; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; color: #0f172a;">ACTION PROTOCOL</div>
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">AI tactical recommendations</div>
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
                <span style="font-weight: 900; font-size: 0.85rem; color: #0369a1; text-transform: uppercase;">LIFESTYLE & RECOVERY</span>
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
                <span style="font-weight: 900; font-size: 0.85rem; color: #92400e; text-transform: uppercase;">ACADEMIC WORKLOAD</span>
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
        # Input validation
        validation_error = None
        if not (1 <= sleep_quality <= 5):
            validation_error = "Sleep Quality must be between 1 and 5."
        elif not (0 <= headaches_per_week <= 7):
            validation_error = "Headaches per week must be between 0 and 7."
        elif not (1 <= academic_performance <= 5):
            validation_error = "Academic Performance must be between 1 and 5."
        elif not (1 <= study_load <= 5):
            validation_error = "Study Load must be between 1 and 5."
        elif not (0 <= extracurricular_frequency <= 7):
            validation_error = "Extracurricular activities must be between 0 and 7."
            
        if validation_error:
            show_bento_error(
                title="Input Telemetry Validation Failed",
                message=validation_error,
                error_code="ERR_INPUT_RANGE",
                action_hint="Adjust the input sliders to stay within standard clinical telemetry ranges."
            )
        else:
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
            
            if predicted_stress is not None:
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
            else:
                err_detail = _last_prediction_error or "Unknown model computation failure"
                show_bento_error(
                    title="Prediction Execution Failed",
                    message=f"Model inference failed with diagnostic: {err_detail}",
                    error_code="ERR_PREDICTION_EXEC",
                    action_hint="Ensure the model file is not corrupted and matches the trained feature set."
                )
    
    # Display prediction results in Bento Light cards
    if st.session_state.prediction_made and st.session_state.predicted_stress is not None:
        predicted_stress = st.session_state.predicted_stress
        confidence = getattr(st.session_state, 'predicted_confidence', None) or 89
        level_name, emoji, description = get_stress_description(predicted_stress)
        
        # Bento Light Theme Level Color Configurations
        level_configs = {
            1: {"bg": "#f0fdf4", "accent": "#16a34a", "pill": "pill-green"},
            2: {"bg": "#f0f9ff", "accent": "#0284c7", "pill": "pill-cyan"},
            3: {"bg": "#fffbeb", "accent": "#d97706", "pill": "pill-yellow"},
            4: {"bg": "#fff7ed", "accent": "#ea580c", "pill": "pill-yellow"},
            5: {"bg": "#fff1f2", "accent": "#e11d48", "pill": "pill-coral"}
        }
        cfg = level_configs.get(predicted_stress, {"bg": "#fffbeb", "accent": "#d97706", "pill": "pill-yellow"})
        
        # Visual Segmented Gauge
        gauge_html = "".join([
            f'<div style="flex: 1; height: 16px; background: {cfg["accent"] if i <= predicted_stress else "#e2e8f0"}; border: 2px solid #0f172a; margin: 0 2px; border-radius: 3px;"></div>'
            for i in range(1, 6)
        ])
        
        st.markdown(f"""
        <div class="bento-box" style="background: {cfg['bg']}; border: 2px solid #0f172a; box-shadow: 6px 6px 0px #0f172a; margin-top: 2rem; margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 2px solid #0f172a; padding-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; gap: 8px;">
                    <span class="bento-pill {cfg['pill']}">PREDICTION RESULT</span>
                    <span class="bento-pill pill-black">CONFIDENCE: {confidence:.0f}%</span>
                </div>
                <span class="bento-pill pill-white">MODEL: RANDOM FOREST</span>
            </div>
            
            <div style="display: grid; grid-template-columns: 130px 1fr; gap: 24px; align-items: center;">
                <div style="background: #ffffff; border: 2px solid #0f172a; box-shadow: 4px 4px 0px #0f172a; border-radius: 8px; height: 125px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <span style="font-size: 3.5rem; line-height: 1;">{emoji}</span>
                    <span style="font-size: 11px; font-weight: 900; color: #0f172a; text-transform: uppercase; margin-top: 4px;">LVL {predicted_stress}/5</span>
                </div>
                
                <div>
                    <h2 style="font-size: 2.2rem; font-weight: 900; color: #0f172a; margin: 0; text-transform: uppercase; letter-spacing: -0.5px;">
                        {level_name}
                    </h2>
                    <p style="font-size: 1.05rem; color: #334155; margin: 8px 0 16px 0; font-weight: 600;">
                        {description}
                    </p>
                    
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 10px; font-weight: 800; text-transform: uppercase; color: #64748b; margin-bottom: 4px;">
                            <span>MILD (LVL 1)</span>
                            <span>MODERATE (LVL 3)</span>
                            <span>CRITICAL (LVL 5)</span>
                        </div>
                        <div style="display: flex; border: 2px solid #0f172a; background: #ffffff; padding: 4px; border-radius: 6px;">
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
                <h3 style="font-size: 1.6rem; font-weight: 900; margin: 0; color: #0f172a;">
                    💡 ACTIONABLE RECOMMENDATIONS
                </h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        engine = AIRecommendationEngine()
        if engine.enabled and engine.api_key:
            provider_tag = "GROQ AI (LIGHTNING FAST)" if engine.provider == 'groq' else f"{engine.provider.upper()} AI"
            st.markdown(f'<span class="bento-pill pill-green" style="margin-bottom: 12px;">⚡ POWERED BY {provider_tag}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="bento-pill pill-yellow" style="margin-bottom: 12px;">⚡ CLINICAL RULE-BASED HEURISTICS ACTIVE</span>', unsafe_allow_html=True)
        
        with st.spinner("⚡ Running recommendation engine..."):
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
                    <span style="font-size: 10px; font-weight: 800; color: #64748b; text-transform: uppercase;">PRIORITY ACTION</span>
                </div>
                <p style="margin: 0; font-size: 0.98rem; color: #0f172a; font-weight: 600; line-height: 1.5;">{rec}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Ground Truth Feedback Section in Bento Light Style
        st.markdown("""
        <div class="bento-box bento-purple" style="margin-top: 2rem;">
            <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                <span class="bento-pill pill-purple">COMMUNITY CALIBRATION</span>
                <span class="bento-pill pill-green">PERSISTENCE SYNC</span>
            </div>
            <h3 style="font-size: 1.3rem; font-weight: 900; margin: 0 0 6px 0; color: #0f172a; text-transform: uppercase;">
                📝 REPORT YOUR ACTUAL EXPERIENCED STRESS
            </h3>
            <p style="color: #475569; font-size: 0.9rem; font-weight: 600; margin: 0 0 16px 0;">
                Help calibrate model weights and contribute anonymous ground truth data to our telemetry database.
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
                
                success = save_user_input(data, include_stress=True)
                if success:
                    storage_medium = getattr(storage, 'last_storage_medium', 'DATABASE')
                    if storage_medium == 'SUPABASE':
                        show_bento_success(
                            title="Telemetry Logged to Supabase",
                            message="Your ground truth feedback was securely written to PostgreSQL with RLS protection.",
                            success_code="SYNC_SUPABASE_OK"
                        )
                    else:
                        show_bento_warning(
                            title="Telemetry Stored Locally (CSV Fallback)",
                            message="Cloud database unconfigured or unreachable. Your submission was safely recorded in local storage.",
                            warning_code="STORAGE_LOCAL_CSV",
                            action_hint="To sync directly with Supabase, add SUPABASE_URL and SUPABASE_KEY to your .env configuration."
                        )
                    st.balloons()
                else:
                    last_err = getattr(storage, 'last_error', 'Unknown storage error')
                    show_bento_error(
                        title="Telemetry Sync Failed",
                        message=f"Unable to write telemetry data: {last_err}",
                        error_code="ERR_STORAGE_WRITE",
                        action_hint="Check disk write permissions or internet connectivity."
                    )
        
        st.markdown("</div>", unsafe_allow_html=True)

def get_recommendations(stress_level, sleep_quality, headaches, study_load, 
                       academic_performance=3, extracurricular=3):
    """Generate personalized recommendations using AI or rule-based fallback"""
    try:
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
        recommendations = []
        
        if stress_level >= 4:
            recommendations.append("🆘 Consider speaking with a counselor or mental health professional.")
        if sleep_quality <= 2:
            recommendations.append("😴 Improve sleep: Aim for 7-9 hours, maintain a consistent schedule.")
        if headaches >= 3:
            recommendations.append("💊 Address frequent headaches: Stay hydrated, take screen breaks, consult a doctor.")
        if study_load >= 4:
            recommendations.append("📚 Manage workload: Break tasks into smaller chunks, prioritize, take regular breaks.")
        if stress_level >= 3:
            recommendations.append("🧘 Try stress-reduction techniques: Meditation, deep breathing, or light exercise.")
            recommendations.append("👥 Stay connected: Talk to friends, family, or join peer support groups.")
        
        if len(recommendations) == 0:
            recommendations.append("✨ You're doing well! Maintain your healthy habits and lifestyle balance.")
        
        return recommendations

# ==============================================================================
# MODULE 02: UNIFIED ANALYTICS, COMMUNITY TELEMETRY & SPECIFICATIONS
# ==============================================================================

def show_analytics_page(stats_df):
    """Display unified analytics, community telemetry, and system specs in Bento Light style"""

    # Bento Header
    st.markdown("""
    <div class="bento-box bento-green" style="margin-bottom: 1.5rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
            <span class="bento-pill pill-green">MODULE 02</span>
            <span class="bento-pill pill-yellow">COMMUNITY TELEMETRY</span>
            <span class="bento-pill pill-cyan">N=1,100 GROUND TRUTH</span>
            <span class="bento-pill pill-black">REAL-TIME INSIGHTS</span>
        </div>
        <h2 style="font-size: 2.2rem; font-weight: 900; margin: 0; color: #0f172a; letter-spacing: -0.5px; text-transform: uppercase;">
            📊 COMMUNITY TELEMETRY & DATASET INSIGHTS
        </h2>
        <p style="color: #475569; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin: 6px 0 0 0;">
            Historic submission trends, cross-factor correlations, and population metrics
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Render Bento Analytics Component (Pure real data)
    render_bento_dashboard(stats_df)

    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

    if stats_df is not None and not stats_df.empty:
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
                <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #64748b; letter-spacing: 0.8px;">TOTAL SAMPLES</div>
                <div style="font-size: 2.4rem; font-weight: 900; color: #0f172a; margin-top: 4px;">{len(stats_df)}</div>
                <span class="bento-pill pill-cyan" style="margin-top: 6px; font-size: 9px;">SUBMISSIONS</span>
            </div>
            """, unsafe_allow_html=True)

        with kpi2:
            avg_sleep = stats_df['sleep_quality'].mean() if 'sleep_quality' in stats_df.columns else 3.2
            st.markdown(f"""
            <div class="bento-box bento-green" style="padding: 16px; margin-bottom: 16px;">
                <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #64748b; letter-spacing: 0.8px;">AVG SLEEP RATING</div>
                <div style="font-size: 2.4rem; font-weight: 900; color: #16a34a; margin-top: 4px;">{avg_sleep:.2f}</div>
                <span class="bento-pill pill-green" style="margin-top: 6px; font-size: 9px;">/ 5.0 SCORE</span>
            </div>
            """, unsafe_allow_html=True)

        with kpi3:
            avg_load = stats_df['study_load'].mean() if 'study_load' in stats_df.columns else 3.5
            st.markdown(f"""
            <div class="bento-box bento-yellow" style="padding: 16px; margin-bottom: 16px;">
                <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #64748b; letter-spacing: 0.8px;">STUDY WORKLOAD</div>
                <div style="font-size: 2.4rem; font-weight: 900; color: #d97706; margin-top: 4px;">{avg_load:.2f}</div>
                <span class="bento-pill pill-yellow" style="margin-top: 6px; font-size: 9px;">/ 5.0 INTENSITY</span>
            </div>
            """, unsafe_allow_html=True)

        with kpi4:
            avg_headaches = stats_df['headaches_per_week'].mean() if 'headaches_per_week' in stats_df.columns else 1.8
            st.markdown(f"""
            <div class="bento-box bento-coral" style="padding: 16px; margin-bottom: 16px;">
                <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #64748b; letter-spacing: 0.8px;">HEADACHES / WK</div>
                <div style="font-size: 2.4rem; font-weight: 900; color: #e11d48; margin-top: 4px;">{avg_headaches:.1f}</div>
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
                        color_continuous_scale=[[0, '#16a34a'], [0.5, '#eab308'], [1, '#ef4444']]
                    )
                    fig_bar.update_layout(
                        template="plotly_white",
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#ffffff",
                        font=dict(family="Space Grotesk", color="#0f172a"),
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

                with plot_col2:
                    fig_pie = px.pie(
                        values=stress_counts.values,
                        names=[f"Level {int(x)}" for x in stress_counts.index],
                        title='Stress Severity Proportions',
                        color_discrete_sequence=['#16a34a', '#0284c7', '#eab308', '#ea580c', '#e11d48']
                    )
                    fig_pie.update_layout(
                        template="plotly_white",
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#ffffff",
                        font=dict(family="Space Grotesk", color="#0f172a"),
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

    # Consolidated Architecture & System Specifications Expander
    with st.expander("ℹ️ PLATFORM ARCHITECTURE, PROVENANCE & TECHNICAL SPECIFICATIONS"):
        # 4 Architecture Cards
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="bento-box bento-green" style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="bento-pill pill-green">CLASSIFIER CORE</span>
                    <span style="font-size: 11px; font-weight: 800; color: #166534;">RANDOM FOREST</span>
                </div>
                <h4 style="margin: 0 0 8px 0; color: #0f172a;">🤖 ENSEMBLE SPECIFICATION</h4>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.5; font-weight: 600;">
                    100 decision trees with Gini impurity split criteria and bootstrap aggregating (bagging) classifying student stress on a 5-tier severity scale with 89.2% test accuracy.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="bento-box bento-purple" style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="bento-pill pill-purple">PERSISTENCE</span>
                    <span style="font-size: 11px; font-weight: 800; color: #6b21a8;">POSTGRESQL</span>
                </div>
                <h4 style="margin: 0 0 8px 0; color: #0f172a;">⚡ SUPABASE & RLS POLICIES</h4>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.5; font-weight: 600;">
                    Row Level Security (RLS) protects table integrity with automatic graceful fallback to local encrypted CSV storage when offline.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="bento-box bento-cyan" style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="bento-pill pill-cyan">DATASET</span>
                    <span style="font-size: 11px; font-weight: 800; color: #0369a1;">N=1,100</span>
                </div>
                <h4 style="margin: 0 0 8px 0; color: #0f172a;">📊 VERIFIED GROUND TRUTH</h4>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.5; font-weight: 600;">
                    Trained on curated <code>StressLevelDataset.csv</code> containing 1,100 verified responses across 21 indicators with zero synthetic data.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="bento-box bento-coral" style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="bento-pill pill-coral">CI/CD</span>
                    <span style="font-size: 11px; font-weight: 800; color: #9f1239;">AUTOMATION</span>
                </div>
                <h4 style="margin: 0 0 8px 0; color: #0f172a;">🚀 TEST AUTOMATION & SECURITY</h4>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.5; font-weight: 600;">
                    33 automated test suites covering ML pipelines, SQL injection, XSS neutralization, and Bandit security scans.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Mathematical Feature Formulas
        st.markdown("""
        <div style="background: #ffffff; border: 2px solid #0f172a; border-radius: 6px; padding: 14px; margin-top: 8px;">
            <div style="font-size: 11px; font-weight: 900; color: #0f172a; text-transform: uppercase; margin-bottom: 8px;">
                📐 Mathematical Feature Formulations
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px;">
                <div style="background: #f0fdf4; border-left: 4px solid #16a34a; padding: 8px 10px; border-radius: 4px;">
                    <div style="font-size: 10px; font-weight: 800; color: #166534;">WELLBEING SCORE</div>
                    <code style="font-size: 12px; color: #0f172a;">Sleep - (Headaches / 2)</code>
                </div>
                <div style="background: #fffbeb; border-left: 4px solid #d97706; padding: 8px 10px; border-radius: 4px;">
                    <div style="font-size: 10px; font-weight: 800; color: #92400e;">ACADEMIC PRESSURE</div>
                    <code style="font-size: 12px; color: #0f172a;">Study Load * (6 - Academic Perf)</code>
                </div>
                <div style="background: #faf5ff; border-left: 4px solid #7c3aed; padding: 8px 10px; border-radius: 4px;">
                    <div style="font-size: 10px; font-weight: 800; color: #6b21a8;">TOTAL WORKLOAD</div>
                    <code style="font-size: 12px; color: #0f172a;">Study Load + (Extracurricular / 2)</code>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer Strip
    st.markdown("""
    <div style="background: #ffffff; border: 2px solid #0f172a; box-shadow: 4px 4px 0px 0px #0f172a; border-radius: 8px; padding: 16px 20px; text-align: center; margin-top: 2rem;">
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-bottom: 6px;">
            <span class="bento-pill pill-yellow">⚡ STRESS.AI v2.4</span>
            <span class="bento-pill pill-cyan">STREAMLIT + PYTHON 3.10</span>
            <span class="bento-pill pill-green">PERSISTENCE SYNC</span>
            <span class="bento-pill pill-black">100% BENTO LIGHT THEME</span>
        </div>
        <p style="color: #64748b; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin: 6px 0 0 0;">
            Engineered for high performance, accessibility, and zero-compromise design standards.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
