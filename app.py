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

# Page configuration
st.set_page_config(
    page_title="Student Stress Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the storage connection once and cache it
storage = get_storage()

# DARK MODE ONLY - No theme toggle needed
# Using eye-comfortable dark colors with reduced blue light
bg_gradient = "linear-gradient(-45deg, #1a1d29, #2d1b2e, #1e2837, #252134)"
container_bg = "rgba(30, 35, 45, 0.9)"
text_primary = "#e4e6eb"
text_secondary = "#b8bdc8"
card_bg = "rgba(40, 45, 60, 0.85)"
card_border = "rgba(255, 255, 255, 0.1)"
accent_1 = "#64b5f6"  # Softer blue
accent_2 = "#4db6ac"  # Teal
accent_3 = "#ffb74d"  # Warm amber
shadow_color = "rgba(0, 0, 0, 0.3)"
glow_color = "rgba(100, 181, 246, 0.2)"

# Custom CSS for ULTRA MODERN styling with advanced animations (Dark Mode Only)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Inter:wght@300;400;600;700&display=swap');
    
    /* Root variables for theme */
    :root {{
        --bg-gradient: {bg_gradient};
        --container-bg: {container_bg};
        --text-primary: {text_primary};
        --text-secondary: {text_secondary};
        --card-bg: {card_bg};
        --card-border: {card_border};
        --accent-1: {accent_1};
        --accent-2: {accent_2};
        --accent-3: {accent_3};
        --shadow: {shadow_color};
        --glow: {glow_color};
    }}
    
    /* Smooth theme transitions */
    * {{
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
    }}
    
    /* Animated Background Gradient */
    .stApp {{
        background: {bg_gradient};
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Glassmorphism container */
    .main .block-container {{
        background: {container_bg};
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-radius: 30px;
        border: 1px solid {card_border};
        box-shadow: 0 8px 32px {shadow_color}, 0 0 0 1px {card_border};
        padding: 2rem;
        animation: fadeInScale 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    * {{
        font-family: 'Poppins', 'Inter', sans-serif;
    }}
    
    /* Animated Header with Glow */
    .main-header {{
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 50%, {accent_3} 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out, gradientSlide 4s ease infinite;
        filter: drop-shadow(0 0 20px {glow_color});
        letter-spacing: -1px;
    }}
    
    @keyframes gradientSlide {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    
    /* Floating Animation */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        33% {{ transform: translateY(-15px) rotate(2deg); }}
        66% {{ transform: translateY(-5px) rotate(-2deg); }}
    }}
    
    .sub-header {{
        font-size: 1.3rem;
        color: {text_secondary};
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        animation: fadeIn 1s ease-out 0.3s both;
        text-shadow: 0 2px 4px {shadow_color};
    }}
    
    /* Glassmorphism Cards */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid {card_border};
        padding: 2rem;
        box-shadow: 0 8px 32px {shadow_color};
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: slideInUp 0.6s ease-out;
    }}
    
    .glass-card:hover {{
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 40px {glow_color};
        border-color: {accent_1};
    }}
    
    /* Neon Glow Effect for Stress Levels */
    .stress-level-1 {{ 
        color: #10b981; 
        font-weight: bold; 
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.8),
                     0 0 40px rgba(16, 185, 129, 0.5);
        animation: neonGlow 2s ease-in-out infinite;
    }}
    .stress-level-2 {{ 
        color: #3b82f6; 
        font-weight: bold; 
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.8),
                     0 0 40px rgba(59, 130, 246, 0.5);
        animation: neonGlow 2s ease-in-out infinite;
    }}
    .stress-level-3 {{ 
        color: #f59e0b; 
        font-weight: bold; 
        text-shadow: 0 0 20px rgba(245, 158, 11, 0.8),
                     0 0 40px rgba(245, 158, 11, 0.5);
        animation: neonGlow 2s ease-in-out infinite;
    }}
    .stress-level-4 {{ 
        color: #f97316; 
        font-weight: bold; 
        text-shadow: 0 0 20px rgba(249, 115, 22, 0.8),
                     0 0 40px rgba(249, 115, 22, 0.5);
        animation: neonGlow 2s ease-in-out infinite;
    }}
    .stress-level-5 {{ 
        color: #ef4444; 
        font-weight: bold; 
        text-shadow: 0 0 20px rgba(239, 68, 68, 0.8),
                     0 0 40px rgba(239, 68, 68, 0.5);
        animation: neonGlow 2s ease-in-out infinite;
    }}
    
    @keyframes neonGlow {{
        0%, 100% {{ filter: brightness(1); }}
        50% {{ filter: brightness(1.3); }}
    }}
    
    /* Epic Prediction Card with 3D Effect */
    .prediction-card {{
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 50%, {accent_3} 100%);
        background-size: 200% 200%;
        padding: 3.5rem;
        border-radius: 25px;
        box-shadow: 0 20px 60px {glow_color}, 0 0 80px {glow_color};
        text-align: center;
        color: white;
        animation: scaleIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275),
                   gradientShift 8s ease infinite;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }}
    
    .prediction-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%) rotate(45deg); }}
        100% {{ transform: translateX(100%) rotate(45deg); }}
    }}
    
    /* Glassmorphism Recommendation Cards */
    .recommendation-card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        padding: 1.8rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px {shadow_color};
        margin: 1.2rem 0;
        border-left: 6px solid transparent;
        border-image: linear-gradient(135deg, {accent_1}, {accent_2}) 1;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: slideInLeft 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }}
    
    .recommendation-card::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 6px;
        background: linear-gradient(135deg, {accent_1}, {accent_2});
        transition: width 0.3s ease;
    }}
    
    .recommendation-card:hover {{
        transform: translateX(15px) scale(1.02);
        box-shadow: 0 12px 30px {glow_color};
    }}
    
    .recommendation-card:hover::before {{
        width: 100%;
        opacity: 0.1;
    }}
    
    /* Animated AI Badge with Pulse */
    .ai-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px {glow_color};
        animation: pulse 2s infinite, float 3s ease-in-out infinite;
        position: relative;
    }}
    
    .ai-badge::after {{
        content: '⚡';
        margin-left: 0.5rem;
        animation: sparkle 1.5s infinite;
    }}
    
    @keyframes sparkle {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.5; transform: scale(1.2); }}
    }}
    
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes fadeInScale {{
        from {{
            opacity: 0;
            transform: scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    @keyframes scaleIn {{
        from {{
            opacity: 0;
            transform: scale(0.9);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes slideInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* Epic Button with Gradient and Effects */
    .stButton>button {{
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%) !important;
        background-size: 200% 200% !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        box-shadow: 0 10px 30px {glow_color} !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        position: relative !important;
        overflow: hidden !important;
        letter-spacing: 0.5px !important;
    }}
    
    .stButton>button::before {{
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-radius: 50% !important;
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.6s, height 0.6s !important;
    }}
    
    .stButton>button:hover {{
        box-shadow: 0 15px 40px {glow_color} !important;
        transform: translateY(-5px) scale(1.05) !important;
        background-position: 100% 50% !important;
    }}
    
    .stButton>button:hover::before {{
        width: 300px !important;
        height: 300px !important;
    }}
    
    .stButton>button:active {{
        transform: translateY(-2px) scale(1.02) !important;
    }}
    
    /* Sidebar with Glass Effect */
    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, {accent_1}f2 0%, {accent_2}f2 100%) !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    /* Animated Metrics */
    div[data-testid="stMetricValue"] {{
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%);
        background-size: 200% 200%;
        animation: gradientSlide 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    /* Slider Styling */
    .stSlider > div > div > div > div {{
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%) !important;
    }}
    
    /* Info/Success/Warning Message Styling */
    .element-container:has(> .stAlert) {{
        animation: slideInLeft 0.5s ease-out;
    }}
    
    div[data-testid="stInfo"],
    div[data-testid="stSuccess"],
    div[data-testid="stWarning"] {{
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border-left-width: 5px;
        animation: slideInUp 0.5s ease-out;
    }}
    
    /* Expander Styling */
    .streamlit-expanderHeader {{
        background: {card_bg} !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: {card_bg} !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 12px {glow_color} !important;
    }}
    
    /* Loading Spinner */
    .stSpinner > div {{
        border-color: {accent_1} transparent transparent transparent !important;
    }}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {card_bg};
        padding: 10px;
        border-radius: 15px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: {container_bg};
        border-radius: 10px;
        padding: 10px 20px;
        color: {text_primary};
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%);
        color: white;
    }}
    
    /* Particle Effect Background */
    @keyframes particles {{
        0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
        100% {{ transform: translateY(-100vh) rotate(360deg); opacity: 0; }}
    }}
    
    /* Smooth Scroll */
    html {{
        scroll-behavior: smooth;
    }}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {card_bg};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, {accent_2} 0%, {accent_1} 100%);
    }}
    
    /* Theme Toggle Button Specific Styling */
    button[key*="theme_toggle"] {{
        background: {card_bg} !important;
        border: 2px solid {card_border} !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        font-size: 1.5rem !important;
        padding: 0 !important;
        box-shadow: 0 4px 15px {shadow_color} !important;
        transition: all 0.3s ease !important;
    }}
    
    button[key*="theme_toggle"]:hover {{
        transform: rotate(180deg) scale(1.1) !important;
        box-shadow: 0 6px 20px {glow_color} !important;
        border-color: {accent_1} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Add animated particles background (dark theme)
particle_color_1 = glow_color
particle_color_2 = f"{accent_1}33"  # 30% opacity for dark mode

st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1; overflow: hidden;">
        <div style="position: absolute; width: 20px; height: 20px; background: {particle_color_1}; border-radius: 50%; 
                    animation: particles 15s linear infinite; left: 10%; animation-delay: 0s;"></div>
        <div style="position: absolute; width: 15px; height: 15px; background: {particle_color_2}; border-radius: 50%; 
                    animation: particles 20s linear infinite; left: 20%; animation-delay: 2s;"></div>
        <div style="position: absolute; width: 25px; height: 25px; background: {particle_color_1}; border-radius: 50%; 
                    animation: particles 18s linear infinite; left: 30%; animation-delay: 4s;"></div>
        <div style="position: absolute; width: 18px; height: 18px; background: {particle_color_2}; border-radius: 50%; 
                    animation: particles 22s linear infinite; left: 40%; animation-delay: 1s;"></div>
        <div style="position: absolute; width: 22px; height: 22px; background: {particle_color_1}; border-radius: 50%; 
                    animation: particles 17s linear infinite; left: 50%; animation-delay: 3s;"></div>
        <div style="position: absolute; width: 16px; height: 16px; background: {particle_color_2}; border-radius: 50%; 
                    animation: particles 21s linear infinite; left: 60%; animation-delay: 5s;"></div>
        <div style="position: absolute; width: 24px; height: 24px; background: {particle_color_1}; border-radius: 50%; 
                    animation: particles 19s linear infinite; left: 70%; animation-delay: 2.5s;"></div>
        <div style="position: absolute; width: 19px; height: 19px; background: {particle_color_2}; border-radius: 50%; 
                    animation: particles 16s linear infinite; left: 80%; animation-delay: 4.5s;"></div>
        <div style="position: absolute; width: 21px; height: 21px; background: {particle_color_1}; border-radius: 50%; 
                    animation: particles 23s linear infinite; left: 90%; animation-delay: 1.5s;"></div>
    </div>
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
    # Epic Animated Header with Icons
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div class="main-header" style="margin-bottom: 0.5rem;">
            <span style="display: inline-block; animation: float 3s ease-in-out infinite;">🧠</span>
            Student Stress Predictor
            <span style="display: inline-block; animation: float 3s ease-in-out infinite; animation-delay: 1.5s;">✨</span>
        </div>
        <div class="sub-header">
            <span style="display: inline-block; animation: pulse 2s infinite; margin-right: 0.5rem;">⚡</span>
            AI-Powered Stress Level Assessment & Data Collection
            <span style="display: inline-block; animation: pulse 2s infinite; animation-delay: 1s; margin-left: 0.5rem;">🚀</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    model, error = load_model()
    
    if error:
        st.error(f"⚠️ {error}")
        st.info("Please run: `python scripts/train_multi_dataset.py`")
        return
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/mental-health.png", width=100)
        st.title("Navigation")
        page = st.radio("Select Page:", 
                       ["🔮 Predict Stress", "📊 Statistics", "ℹ️ About"])
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        stats_df = load_statistics()
        if stats_df is not None and not stats_df.empty:
            st.metric("Total Submissions", len(stats_df))
            if 'stress_level' in stats_df.columns:
                valid_stress = pd.to_numeric(stats_df['stress_level'], errors='coerce').dropna()
                if len(valid_stress) > 0:
                    avg_stress = valid_stress.mean()
                    st.metric("Avg Stress Level", f"{avg_stress:.2f}")
        else:
            st.info("No data collected yet")
    
    # Main content based on page selection
    if page == "🔮 Predict Stress":
        show_prediction_page(model)
    elif page == "📊 Statistics":
        show_statistics_page()
    else:
        show_about_page()

def show_prediction_page(model):
    """Display the prediction page"""
    
    # Beautiful section header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 700; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 1rem; animation: fadeInDown 0.6s ease-out;">
            🔮 Stress Level Prediction
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Glass card with instructions
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 2rem; animation-delay: 0.2s;">
        <h3 style="color: #667eea; margin-bottom: 1rem; font-weight: 600;">✨ How it works:</h3>
        <div style="display: grid; gap: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                             width: 32px; height: 32px; border-radius: 50%; display: flex; 
                             align-items: center; justify-content: center; font-weight: bold;">1</span>
                <span style="color: #4b5563;">Enter your information using the sliders below</span>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                             width: 32px; height: 32px; border-radius: 50%; display: flex; 
                             align-items: center; justify-content: center; font-weight: bold;">2</span>
                <span style="color: #4b5563;">Click the <strong>Predict My Stress Level</strong> button</span>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                             width: 32px; height: 32px; border-radius: 50%; display: flex; 
                             align-items: center; justify-content: center; font-weight: bold;">3</span>
                <span style="color: #4b5563;">View your personalized results and AI-powered recommendations</span>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                             width: 32px; height: 32px; border-radius: 50%; display: flex; 
                             align-items: center; justify-content: center; font-weight: bold;">4</span>
                <span style="color: #4b5563;">Share your actual stress level to help improve our AI</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.4s;">
            <h3 style="color: #667eea; margin-bottom: 1.5rem; font-weight: 600;">📋 Lifestyle Factors</h3>
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
        <div class="glass-card" style="animation-delay: 0.5s;">
            <h3 style="color: #764ba2; margin-bottom: 1.5rem; font-weight: 600;">📚 Academic Factors</h3>
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
    
    st.markdown("---")
    
    # Display calculated features
    with st.expander("🔍 View Calculated Features (Advanced)"):
        wellbeing, pressure, workload = calculate_engineered_features(
            sleep_quality, headaches_per_week, academic_performance,
            study_load, extracurricular_frequency
        )
        
        col1_feat, col2_feat, col3_feat = st.columns(3)
        col1_feat.metric("Wellbeing Score", f"{wellbeing:.2f}")
        col2_feat.metric("Academic Pressure", f"{pressure:.2f}")
        col3_feat.metric("Total Workload", f"{workload:.2f}")
    
    # Predict button
    if st.button("🎯 Predict My Stress Level", type="primary", use_container_width=True):
        # Prepare features with engineered features
        wellbeing, pressure, workload = calculate_engineered_features(
            sleep_quality, headaches_per_week, academic_performance,
            study_load, extracurricular_frequency
        )
        
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
        
        # Make prediction
        predicted_stress, confidence = predict_stress(model, features)
        
        if predicted_stress:
            st.session_state.prediction_made = True
            st.session_state.predicted_stress = predicted_stress
            st.session_state.input_data = {
                'sleep_quality': sleep_quality,
                'headaches_per_week': headaches_per_week,
                'academic_performance': academic_performance,
                'study_load': study_load,
                'extracurricular_frequency': extracurricular_frequency
            }
    
    # Display prediction results
    if st.session_state.prediction_made:
        predicted_stress = st.session_state.predicted_stress
        level_name, emoji, description = get_stress_description(predicted_stress)
        
        st.markdown("---")
        st.subheader("📊 Your Results")
        
        # Create result display
        res_col1, res_col2, res_col3 = st.columns([1, 2, 1])
        
        with res_col2:
            st.markdown(f"""
            <div class='prediction-card'>
                <h1 style='font-size: 5rem; margin: 0; animation: pulse 2s infinite;'>{emoji}</h1>
                <h2 style='margin: 1rem 0 0.5rem 0; font-size: 2rem;'>
                    Stress Level: {predicted_stress}/5
                </h2>
                <h3 style='color: rgba(255,255,255,0.9); font-weight: 300; font-size: 1.5rem;'>{level_name}</h3>
                <p style='font-size: 1.1rem; color: rgba(255,255,255,0.95); margin-top: 1rem;'>{description}</p>
            </div>
            <style>
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
            }}
            </style>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("---")
        st.subheader("💡 AI-Powered Recommendations")
        
        # Check if AI is enabled
        from ai_recommender import AIRecommendationEngine
        engine = AIRecommendationEngine()
        
        if engine.enabled and engine.api_key:
            if engine.provider == 'groq':
                st.markdown('<div class="ai-badge">⚡ Powered by Groq AI (Lightning Fast!)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-badge">🤖 Powered by {engine.provider.upper()} AI</div>', unsafe_allow_html=True)
        else:
            st.info("💡 **Tip**: Enable Groq AI for personalized recommendations! Add your API key to `ai_config.json` or set `GROQ_API_KEY` environment variable. Get a free key at: https://console.groq.com")
        
        with st.spinner("🤖 Generating personalized recommendations..."):
            recommendations = get_recommendations(
                predicted_stress,
                st.session_state.input_data['sleep_quality'],
                st.session_state.input_data['headaches_per_week'],
                st.session_state.input_data['study_load'],
                st.session_state.input_data['academic_performance'],
                st.session_state.input_data['extracurricular_frequency']
            )
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="recommendation-card">
                <strong style="color: #667eea; font-size: 1.1rem;">#{i}</strong>
                <p style="margin: 0.5rem 0 0 0; font-size: 1rem; color: #374151;">{rec}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feedback section
        st.markdown("---")
        st.subheader("📝 Help Us Improve!")
        st.markdown("If you know your actual stress level, please share it to help improve our model:")
        
        feedback_col1, feedback_col2 = st.columns([3, 1])
        
        with feedback_col1:
            actual_stress = st.slider(
                "What is your actual stress level?",
                min_value=1, max_value=5, value=predicted_stress,
                help="Your honest assessment helps improve predictions"
            )
        
        with feedback_col2:
            if st.button("📤 Submit", type="primary", use_container_width=True):
                data = st.session_state.input_data.copy()
                data['actual_stress'] = actual_stress
                
                if save_user_input(data, include_stress=True):
                    # Success/error messages are now handled by the database module
                    st.balloons()
                else:
                    # Let the database module show the error
                    pass

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
    """Display statistics page"""
    st.markdown("""
    <div class="glass-card" style="text-align: center; margin-bottom: 2rem; animation-delay: 0.1s;">
        <h1 style="color: #667eea; font-weight: 700; font-size: 2.5rem; margin: 0;">
            📊 Data Statistics & Insights
        </h1>
        <p style="color: #6b7280; margin-top: 0.5rem;">Real-time analytics from our student community</p>
    </div>
    """, unsafe_allow_html=True)

    stats_df = load_statistics()

    if stats_df is None or len(stats_df) == 0:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem; animation-delay: 0.2s;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
            <h3 style="color: #667eea; margin-bottom: 0.5rem;">No Data Yet</h3>
            <p style="color: #6b7280;">Start by making predictions to see insights!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div class="glass-card" style="text-align: center; margin-bottom: 2rem; animation-delay: 0.2s;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">✅</div>
        <h2 style="color: #10b981; margin: 0;">{len(stats_df)}</h2>
        <p style="color: #6b7280; margin-top: 0.3rem;">Total Submissions</p>
    </div>
    """, unsafe_allow_html=True)

    # Overview metrics
    st.markdown("""
    <div class="glass-card" style="animation-delay: 0.3s; margin-bottom: 1.5rem;">
        <h3 style="color: #667eea; margin-bottom: 1.5rem; font-weight: 600;">📈 Overview Metrics</h3>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_sleep = stats_df['sleep_quality'].mean()
        st.metric("Avg Sleep Quality", f"{avg_sleep:.2f}/5")

    with col2:
        avg_headaches = stats_df['headaches_per_week'].mean()
        st.metric("Avg Headaches/Week", f"{avg_headaches:.1f}")

    with col3:
        avg_performance = stats_df['academic_performance'].mean()
        st.metric("Avg Academic Perf.", f"{avg_performance:.2f}/5")

    with col4:
        avg_load = stats_df['study_load'].mean()
        st.metric("Avg Study Load", f"{avg_load:.2f}/5")

    # Stress level distribution (if available)
    if 'stress_level' in stats_df.columns:
        valid_stress = stats_df['stress_level'].dropna()

        if len(valid_stress) > 0:
            st.markdown("---")
            st.subheader("🎯 Stress Level Distribution")

            col1, col2 = st.columns(2)

            with col1:
                # Bar chart
                stress_counts = valid_stress.value_counts().sort_index()
                fig = px.bar(
                    x=stress_counts.index,
                    y=stress_counts.values,
                    labels={'x': 'Stress Level', 'y': 'Count'},
                    title='Stress Level Distribution',
                    color=stress_counts.index,
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Pie chart
                fig = px.pie(
                    values=stress_counts.values,
                    names=stress_counts.index,
                    title='Stress Level Proportions',
                    color_discrete_sequence=px.colors.sequential.RdBu_r
                )
                st.plotly_chart(fig, use_container_width=True)

    # Feature distributions
    st.markdown("---")
    st.subheader("📊 Feature Distributions")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            stats_df,
            x='sleep_quality',
            nbins=5,
            title='Sleep Quality Distribution',
            labels={'sleep_quality': 'Sleep Quality'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            stats_df,
            x='study_load',
            nbins=5,
            title='Study Load Distribution',
            labels={'study_load': 'Study Load'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Timeline
    if 'timestamp' in stats_df.columns:
        st.markdown("---")
        st.subheader("📅 Submission Timeline")

        try:
            stats_df['timestamp'] = pd.to_datetime(stats_df['timestamp'])
            stats_df['date'] = stats_df['timestamp'].dt.date
            daily_counts = stats_df.groupby('date').size().reset_index(name='count')

            fig = px.line(
                daily_counts,
                x='date',
                y='count',
                title='Daily Submissions',
                labels={'date': 'Date', 'count': 'Number of Submissions'}
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.info(f"Timeline visualization not available: {e}")

    # Raw data
    with st.expander("🔍 View Raw Data"):
        st.dataframe(stats_df, use_container_width=True)

        # Download button
        csv = stats_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"stress_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def show_about_page():
    """Display about page"""
    st.markdown("""
    <div class="glass-card" style="text-align: center; margin-bottom: 2rem; animation-delay: 0.1s;">
        <h1 style="color: #667eea; font-weight: 700; font-size: 2.5rem; margin: 0;">
            ℹ️ About This Application
        </h1>
        <p style="color: #6b7280; margin-top: 0.5rem;">Built with ❤️ using Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 0.2s;">
        <h3 style="color: #667eea; margin-bottom: 1rem; font-weight: 600;">🧠 Student Stress Predictor</h3>
        <p style="color: #4b5563; font-size: 1.05rem; line-height: 1.8;">
            This application uses <strong>Machine Learning</strong> to predict student stress levels based on lifestyle 
            and academic factors. It combines data from multiple sources and continuously improves as 
            more users contribute their data.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 0.3s;">
        <h3 style="color: #667eea; margin-bottom: 1rem; font-weight: 600;">🎯 How It Works</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.4s;">
            <div style="text-align: center; font-size: 2.5rem; margin-bottom: 1rem;">1️⃣</div>
            <h4 style="color: #667eea; text-align: center; margin-bottom: 0.5rem;">Data Collection</h4>
            <p style="color: #6b7280; text-align: center;">Users input lifestyle & academic info</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.6s;">
            <div style="text-align: center; font-size: 2.5rem; margin-bottom: 1rem;">3️⃣</div>
            <h4 style="color: #667eea; text-align: center; margin-bottom: 0.5rem;">ML Prediction</h4>
            <p style="color: #6b7280; text-align: center;">Trained model predicts stress (1-5)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.5s;">
            <div style="text-align: center; font-size: 2.5rem; margin-bottom: 1rem;">2️⃣</div>
            <h4 style="color: #764ba2; text-align: center; margin-bottom: 0.5rem;">Feature Engineering</h4>
            <p style="color: #6b7280; text-align: center;">Calculate wellbeing & pressure scores</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.7s;">
            <div style="text-align: center; font-size: 2.5rem; margin-bottom: 1rem;">4️⃣</div>
            <h4 style="color: #764ba2; text-align: center; margin-bottom: 0.5rem;">Continuous Learning</h4>
            <p style="color: #6b7280; text-align: center;">User feedback improves the model</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 0.8s;">
        <h3 style="color: #667eea; margin-bottom: 1.5rem; font-weight: 600;">📊 Features Used</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
            <div>
                <h4 style="color: #667eea; margin-bottom: 1rem;">Input Features (5):</h4>
                <ul style="color: #4b5563; line-height: 2;">
                    <li>😴 Sleep Quality (1-5)</li>
                    <li>🤕 Headaches per Week (0-7)</li>
                    <li>👩‍🎓 Academic Performance (1-5)</li>
                    <li>📖 Study Load (1-5)</li>
                    <li>🎾 Extracurricular Frequency (0-7)</li>
                </ul>
            </div>
            <div>
                <h4 style="color: #764ba2; margin-bottom: 1rem;">Engineered Features (3):</h4>
                <ul style="color: #4b5563; line-height: 2;">
                    <li>💚 Wellbeing Score</li>
                    <li>📚 Academic Pressure</li>
                    <li>⚖️ Total Workload</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; animation-delay: 0.9s;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
            <h4 style="color: #667eea; margin: 0.5rem 0;">Algorithm</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Random Forest</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; animation-delay: 1s;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
            <h4 style="color: #10b981; margin: 0.5rem 0;">Accuracy</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">94-97%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; animation-delay: 1.1s;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <h4 style="color: #667eea; margin: 0.5rem 0;">Samples</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">1,600+</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="glass-card" style="text-align: center; animation-delay: 1.2s;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🗂️</div>
            <h4 style="color: #764ba2; margin: 0.5rem 0;">Datasets</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">4 combined</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 1.3s;">
        <h3 style="color: #667eea; margin-bottom: 1rem; font-weight: 600;">🔄 Data Flow</h3>
        <div style="text-align: center; background: rgba(102, 126, 234, 0.1); padding: 2rem; border-radius: 15px; margin: 1.5rem 0;">
            <p style="color: #e4e6eb; font-size: 1.1rem; line-height: 2; font-weight: 500;">
                User Input → Feature Engineering → ML Model → Prediction<br>
                <span style="color: #64b5f6;">↓</span><br>
                Save to Database → Future Model Improvements
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 1.4s;">
        <h3 style="color: #667eea; margin-bottom: 1rem; font-weight: 600;">⚠️ Disclaimer</h3>
        <p style="color: #b8bdc8; font-size: 1.05rem; line-height: 1.8; text-align: center; padding: 1rem;">
            This tool is for <strong style="color: #e4e6eb;">educational and informational purposes only</strong>. 
            It should not replace professional medical or psychological advice. If you're experiencing severe stress, 
            please consult with a qualified healthcare professional.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; animation-delay: 1.5s;">
        <p style="color: #64b5f6; font-size: 0.95rem; font-weight: 500;">
            Version 2.0 (Dark Mode) • Built with ❤️ using Machine Learning
        </p>
        <p style="color: #b8bdc8; font-size: 0.85rem; margin-top: 0.5rem;">
            Last Updated: October 2025
        </p>
    </div>
    """)

if __name__ == "__main__":
    main()

