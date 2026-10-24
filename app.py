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
    
    /* Subheaders Styling for Visibility */
    h2, h3 {{
        color: {text_primary} !important;
        font-weight: 700 !important;
    }}
    
    .stMarkdown h2 {{
        color: {text_primary} !important;
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin: 2rem 0 1rem 0 !important;
        padding: 0.5rem 0 !important;
    }}
    
    .stMarkdown h3 {{
        color: {accent_1} !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin: 1.5rem 0 1rem 0 !important;
    }}
    
    /* Sidebar with Ultra Modern Glass Effect */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, 
            rgba(102, 126, 234, 0.15) 0%, 
            rgba(118, 75, 162, 0.15) 50%,
            rgba(77, 182, 172, 0.15) 100%) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-right: 1px solid {card_border} !important;
        box-shadow: 4px 0 24px {shadow_color} !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background: transparent !important;
    }}
    
    /* Sidebar Logo Container */
    section[data-testid="stSidebar"] .stImage {{
        display: flex !important;
        justify-content: center !important;
        margin: 1rem auto !important;
        padding: 1rem !important;
        background: linear-gradient(135deg, {accent_1}20 0%, {accent_2}20 100%) !important;
        border-radius: 20px !important;
        border: 2px solid {card_border} !important;
        box-shadow: 0 8px 16px {shadow_color} !important;
        animation: float 3s ease-in-out infinite !important;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    /* Sidebar Title */
    section[data-testid="stSidebar"] .stMarkdown h1 {{
        color: {text_primary} !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin: 1.5rem 0 !important;
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 50%, {accent_3} 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-shadow: 0 0 20px {glow_color} !important;
        animation: gradientSlide 5s ease infinite !important;
    }}
    
    /* Sidebar Radio Buttons */
    section[data-testid="stSidebar"] .stRadio > div {{
        background: {card_bg} !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        border: 1px solid {card_border} !important;
        box-shadow: 0 4px 12px {shadow_color} !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio label {{
        color: {text_primary} !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
        padding: 0.8rem 1rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio label:hover {{
        background: linear-gradient(135deg, {accent_1}30 0%, {accent_2}30 100%) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 0 15px {glow_color} !important;
    }}
    
    /* Sidebar Metrics */
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {{
        color: {accent_1} !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px {glow_color} !important;
    }}
    
    section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
        color: {text_secondary} !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }}
    
    /* Sidebar Divider */
    section[data-testid="stSidebar"] hr {{
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent 0%, {accent_1} 50%, transparent 100%) !important;
        margin: 1.5rem 0 !important;
        animation: pulse 2s ease-in-out infinite !important;
    }}
    
    /* Sidebar Headers */
    section[data-testid="stSidebar"] h3 {{
        color: {text_primary} !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        margin: 1rem 0 0.5rem 0 !important;
        text-align: center !important;
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
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
        animation: spin 1s linear infinite, pulse 2s ease-in-out infinite !important;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {card_bg};
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 4px 16px {shadow_color};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: {container_bg};
        border-radius: 10px;
        padding: 10px 20px;
        color: {text_primary};
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: linear-gradient(135deg, {accent_1}30 0%, {accent_2}30 100%);
        border-color: {card_border};
        transform: translateY(-2px);
        box-shadow: 0 4px 12px {glow_color};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%);
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 20px {glow_color};
        transform: scale(1.02);
    }}
    
    /* Enhanced Plotly Charts */
    .js-plotly-plot {{
        background: {card_bg} !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        box-shadow: 0 4px 20px {shadow_color} !important;
        border: 1px solid {card_border} !important;
        transition: all 0.3s ease !important;
    }}
    
    .js-plotly-plot:hover {{
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 30px {glow_color} !important;
    }}
    
    /* Data Frame Styling */
    .stDataFrame {{
        background: {card_bg} !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px {shadow_color} !important;
        border: 1px solid {card_border} !important;
    }}
    
    .stDataFrame table {{
        background: transparent !important;
    }}
    
    .stDataFrame th {{
        background: linear-gradient(135deg, {accent_1} 0%, {accent_2} 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border: none !important;
    }}
    
    .stDataFrame td {{
        color: {text_primary} !important;
        padding: 0.8rem 1rem !important;
        border-bottom: 1px solid {card_border} !important;
    }}
    
    .stDataFrame tr:hover {{
        background: rgba(100, 181, 246, 0.1) !important;
    }}
    
    /* Progress Bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {accent_1} 0%, {accent_2} 50%, {accent_3} 100%) !important;
        background-size: 200% 100% !important;
        animation: gradientSlide 2s ease infinite !important;
        box-shadow: 0 2px 10px {glow_color} !important;
    }}
    
    /* Download Button Special Effect */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {accent_2} 0%, {accent_3} 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(77, 182, 172, 0.4) !important;
        transition: all 0.3s ease !important;
    }}
    
    .stDownloadButton > button:hover {{
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(77, 182, 172, 0.6) !important;
    }}
    
    /* Select Box Modern Style */
    .stSelectbox > div > div {{
        background: {card_bg} !important;
        border: 2px solid {card_border} !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stSelectbox > div > div:hover {{
        border-color: {accent_1} !important;
        box-shadow: 0 4px 12px {glow_color} !important;
    }}
    
    /* Text Input Glow Effect */
    .stTextInput > div > div > input {{
        background: {card_bg} !important;
        border: 2px solid {card_border} !important;
        border-radius: 12px !important;
        color: {text_primary} !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {accent_1} !important;
        box-shadow: 0 0 0 3px {glow_color}, 0 4px 12px {glow_color} !important;
        transform: scale(1.02) !important;
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
    
    # Sidebar with Ultra Modern Design
    with st.sidebar:
        # Logo with cool animation
        st.image("https://img.icons8.com/fluency/96/000000/mental-health.png", width=100)
        
        # Animated title with gradient
        st.markdown("""
        <h1 style="text-align: center; margin: 1rem 0;">
            🧠 StressAI
        </h1>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation with cool label
        st.markdown("""
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <span style="color: #64b5f6; font-weight: 600; font-size: 1.1rem; 
                         text-transform: uppercase; letter-spacing: 2px;">
                📍 Navigate
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio("Select Page:", 
                       ["🍱 Bento Analytics", "🔮 Predict Stress", "📊 Statistics", "ℹ️ About"],
                       index=0,
                       label_visibility="collapsed")
        
        st.markdown("---")
        
        # Stats section with modern cards
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <span style="color: #64b5f6; font-weight: 600; font-size: 1.1rem; 
                         text-transform: uppercase; letter-spacing: 2px;">
                📊 Live Stats
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        stats_df = load_statistics()
        if stats_df is not None and not stats_df.empty:
            # Submissions metric
            st.markdown("""
            <div style="background: rgba(100, 181, 246, 0.1); 
                        border-radius: 12px; 
                        padding: 1rem; 
                        margin-bottom: 0.8rem;
                        border: 1px solid rgba(100, 181, 246, 0.2);
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
            """, unsafe_allow_html=True)
            st.metric("📥 Total Submissions", len(stats_df))
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Average stress metric
            if 'stress_level' in stats_df.columns:
                valid_stress = pd.to_numeric(stats_df['stress_level'], errors='coerce').dropna()
                if len(valid_stress) > 0:
                    avg_stress = valid_stress.mean()
                    
                    # Color based on stress level
                    if avg_stress < 2.5:
                        stress_color = "#10b981"
                        stress_emoji = "😊"
                    elif avg_stress < 3.5:
                        stress_color = "#ffb74d"
                        stress_emoji = "😐"
                    else:
                        stress_color = "#ef4444"
                        stress_emoji = "😰"
                    
                    st.markdown(f"""
                    <div style="background: rgba(77, 182, 172, 0.1); 
                                border-radius: 12px; 
                                padding: 1rem;
                                border: 1px solid rgba(77, 182, 172, 0.2);
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
                    """, unsafe_allow_html=True)
                    st.metric(f"{stress_emoji} Avg Stress", f"{avg_stress:.2f}")
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(100, 181, 246, 0.1); 
                        border-radius: 12px; 
                        padding: 1.5rem; 
                        text-align: center;
                        border: 1px solid rgba(100, 181, 246, 0.2);">
                <p style="color: #b8bdc8; margin: 0;">📊 No data yet</p>
                <p style="color: #64b5f6; font-size: 0.85rem; margin: 0.5rem 0 0 0;">
                    Start predicting to see stats!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Footer with version info
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem;">
            <p style="color: #64b5f6; font-size: 0.75rem; margin: 0; font-weight: 600;">
                ⚡ Powered by AI
            </p>
            <p style="color: #b8bdc8; font-size: 0.7rem; margin: 0.3rem 0 0 0;">
                v2.0 • Dark Mode
            </p>
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
    """Display the prediction page"""
    
    # Notice banner to switch to Bento Analytics
    st.markdown("""
    <div style="background: linear-gradient(90deg, rgba(251, 191, 36, 0.12), rgba(99, 102, 241, 0.12));
                border: 2px solid #fbbf24; border-radius: 12px; padding: 14px 20px; margin-bottom: 25px;
                display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <div style="display: flex; align-items: center; gap: 14px;">
            <span style="font-size: 1.6rem;">🍱</span>
            <div>
                <strong style="color: #fbbf24; font-size: 0.95rem; letter-spacing: 0.5px;">LOOKING FOR THE NEW BENTO DASHBOARD?</strong>
                <p style="color: #e4e6eb; margin: 3px 0 0 0; font-size: 0.85rem;">Select <strong>🍱 Bento Analytics</strong> in the left sidebar to explore the real-time Neo-Brutalist telemetry, radar metrics, and dataset distributions.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Beautiful section header
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0 2rem 0;">
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
        
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem 0;">
            <h2 style="background: linear-gradient(135deg, #64b5f6 0%, #10b981 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-weight: 700; font-size: 2.5rem; margin: 0;">
                📊 Your Prediction Results
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
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
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem 0;">
            <h2 style="background: linear-gradient(135deg, #ffb74d 0%, #4db6ac 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-weight: 700; font-size: 2.2rem; margin: 0;">
                💡 AI-Powered Recommendations
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
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
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0 1.5rem 0;">
            <h2 style="background: linear-gradient(135deg, #a855f7 0%, #64b5f6 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-weight: 700; font-size: 2rem; margin: 0;">
                📝 Help Us Improve!
            </h2>
            <p style="color: #b8bdc8; margin-top: 1rem; font-size: 1.05rem;">
                If you know your actual stress level, please share it to help improve our model
            </p>
        </div>
        """, unsafe_allow_html=True)
        
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
    """Display statistics page with ultra-modern design"""
    stats_df = load_statistics()

    # Neo-Brutalist Bento Dashboard (Real Data Driven)
    render_bento_dashboard(stats_df)

    st.markdown("---")
    st.markdown("""
    <div class="glass-card" style="text-align: center; margin-bottom: 2.5rem; animation-delay: 0.1s; 
                 background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
                 border: 2px solid rgba(100, 181, 246, 0.3);
                 box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 40px rgba(100, 181, 246, 0.2);">
        <h1 style="background: linear-gradient(135deg, #64b5f6 0%, #4db6ac 50%, #ffb74d 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-weight: 800; font-size: 2.2rem; margin: 0; text-shadow: 0 0 30px rgba(100, 181, 246, 0.5);">
            📊 Detailed Community Telemetry & Timeline
        </h1>
        <p style="color: #b8bdc8; margin-top: 0.5rem; font-size: 1rem; font-weight: 500;">
            Historic submission trends and deep distributions 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

    if stats_df is None or len(stats_df) == 0:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 4rem; animation-delay: 0.2s;
                     background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);">
            <div style="font-size: 5rem; margin-bottom: 1.5rem; animation: pulse 2s ease-in-out infinite;">📭</div>
            <h3 style="color: #64b5f6; margin-bottom: 1rem; font-size: 2rem; font-weight: 700;">No Data Yet</h3>
            <p style="color: #b8bdc8; font-size: 1.2rem;">Start by making predictions to unlock powerful insights!</p>
            <div style="margin-top: 2rem;">
                <span style="display: inline-block; padding: 0.8rem 2rem; background: linear-gradient(135deg, #64b5f6 0%, #4db6ac 100%);
                             color: white; border-radius: 25px; font-weight: 600; box-shadow: 0 4px 15px rgba(100, 181, 246, 0.4);">
                    👆 Use the sidebar to get started
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Enhanced Total Submissions Card
    st.markdown(f"""
    <style>
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-20px); }}
    }}
    </style>
    <div class="glass-card" style="text-align: center; margin-bottom: 2.5rem; animation-delay: 0.2s;
                 background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(100, 181, 246, 0.15) 100%);
                 border: 2px solid rgba(16, 185, 129, 0.3);
                 box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 40px rgba(16, 185, 129, 0.2);
                 position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50%; right: -50%; width: 200%; height: 200%; 
                    background: radial-gradient(circle, rgba(100, 181, 246, 0.1) 0%, transparent 70%);
                    animation: spin 20s linear infinite;"></div>
        <div style="position: relative; z-index: 1;">
            <div style="font-size: 4rem; margin-bottom: 1rem; animation: bounce 2s ease-in-out infinite;">✅</div>
            <h2 style="color: #10b981; margin: 0; font-size: 3.5rem; font-weight: 800; 
                       text-shadow: 0 0 20px rgba(16, 185, 129, 0.5);">{len(stats_df)}</h2>
            <p style="color: #b8bdc8; margin-top: 0.5rem; font-size: 1.2rem; font-weight: 600; letter-spacing: 1px;">
                TOTAL SUBMISSIONS
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced Overview metrics header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
        <h3 style="background: linear-gradient(135deg, #64b5f6 0%, #4db6ac 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-weight: 700; font-size: 2rem; margin: 0;">
            📈 Key Metrics Overview
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        avg_sleep = stats_df['sleep_quality'].mean()
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; animation-delay: 0.4s;
                     background: linear-gradient(135deg, rgba(100, 181, 246, 0.15) 0%, rgba(147, 51, 234, 0.15) 100%);
                     border: 2px solid rgba(100, 181, 246, 0.3); padding: 1.5rem;
                     box-shadow: 0 4px 20px rgba(100, 181, 246, 0.3);">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">😴</div>
            <h4 style="color: #64b5f6; font-weight: 700; font-size: 2rem; margin: 0.5rem 0;">
                {avg_sleep:.2f}<span style="font-size: 1.2rem; color: #b8bdc8;">/5</span>
            </h4>
            <p style="color: #b8bdc8; font-size: 0.9rem; font-weight: 600; margin: 0;">Sleep Quality</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        avg_headaches = stats_df['headaches_per_week'].mean()
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; animation-delay: 0.5s;
                     background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(255, 183, 77, 0.15) 100%);
                     border: 2px solid rgba(239, 68, 68, 0.3); padding: 1.5rem;
                     box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤕</div>
            <h4 style="color: #ef4444; font-weight: 700; font-size: 2rem; margin: 0.5rem 0;">
                {avg_headaches:.1f}
            </h4>
            <p style="color: #b8bdc8; font-size: 0.9rem; font-weight: 600; margin: 0;">Headaches/Week</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        avg_performance = stats_df['academic_performance'].mean()
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; animation-delay: 0.6s;
                     background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(77, 182, 172, 0.15) 100%);
                     border: 2px solid rgba(16, 185, 129, 0.3); padding: 1.5rem;
                     box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎓</div>
            <h4 style="color: #10b981; font-weight: 700; font-size: 2rem; margin: 0.5rem 0;">
                {avg_performance:.2f}<span style="font-size: 1.2rem; color: #b8bdc8;">/5</span>
            </h4>
            <p style="color: #b8bdc8; font-size: 0.9rem; font-weight: 600; margin: 0;">Academic Performance</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_load = stats_df['study_load'].mean()
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; animation-delay: 0.7s;
                     background: linear-gradient(135deg, rgba(255, 183, 77, 0.15) 0%, rgba(251, 146, 60, 0.15) 100%);
                     border: 2px solid rgba(255, 183, 77, 0.3); padding: 1.5rem;
                     box-shadow: 0 4px 20px rgba(255, 183, 77, 0.3);">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📚</div>
            <h4 style="color: #ffb74d; font-weight: 700; font-size: 2rem; margin: 0.5rem 0;">
                {avg_load:.2f}<span style="font-size: 1.2rem; color: #b8bdc8;">/5</span>
            </h4>
            <p style="color: #b8bdc8; font-size: 0.9rem; font-weight: 600; margin: 0;">Study Load</p>
        </div>
        """, unsafe_allow_html=True)

    # Stress level distribution (if available)
    if 'stress_level' in stats_df.columns:
        valid_stress = stats_df['stress_level'].dropna()

        if len(valid_stress) > 0:
            st.markdown("""
            <div style="text-align: center; margin: 3rem 0 2rem 0;">
                <h2 style="background: linear-gradient(135deg, #64b5f6 0%, #a855f7 100%);
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                           font-weight: 700; font-size: 2.2rem; margin: 0;">
                    🎯 Stress Level Distribution
                </h2>
            </div>
            """, unsafe_allow_html=True)

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
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="background: linear-gradient(135deg, #4db6ac 0%, #ffb74d 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-weight: 700; font-size: 2.2rem; margin: 0;">
            📊 Feature Distributions
        </h2>
    </div>
    """, unsafe_allow_html=True)

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
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem 0;">
            <h2 style="background: linear-gradient(135deg, #10b981 0%, #64b5f6 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-weight: 700; font-size: 2.2rem; margin: 0;">
                📅 Submission Timeline
            </h2>
        </div>
        """, unsafe_allow_html=True)

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
    """Display about page with ultra-modern design"""
    st.markdown("""
    <div class="glass-card" style="text-align: center; margin-bottom: 2.5rem; animation-delay: 0.1s;
                 background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
                 border: 2px solid rgba(100, 181, 246, 0.3);
                 box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 40px rgba(100, 181, 246, 0.2);
                 position: relative; overflow: hidden;">
        <div style="position: absolute; top: -100%; left: -100%; width: 300%; height: 300%; 
                    background: radial-gradient(circle, rgba(100, 181, 246, 0.1) 0%, transparent 50%);
                    animation: spin 30s linear infinite;"></div>
        <div style="position: relative; z-index: 1;">
            <h1 style="background: linear-gradient(135deg, #64b5f6 0%, #4db6ac 50%, #ffb74d 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-weight: 800; font-size: 3.5rem; margin: 0; 
                       text-shadow: 0 0 30px rgba(100, 181, 246, 0.5); animation: pulse 2s ease-in-out infinite;">
                ℹ️ About StressAI
            </h1>
            <p style="color: #b8bdc8; margin-top: 1rem; font-size: 1.2rem; font-weight: 500;">
                Built with ❤️ using Advanced Machine Learning • AI-Powered Predictions
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 0.2s;
                 background: linear-gradient(135deg, rgba(77, 182, 172, 0.1) 0%, rgba(100, 181, 246, 0.1) 100%);
                 border: 2px solid rgba(77, 182, 172, 0.2);
                 box-shadow: 0 4px 20px rgba(77, 182, 172, 0.2);">
        <h3 style="background: linear-gradient(135deg, #64b5f6 0%, #4db6ac 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 1.5rem; font-weight: 700; font-size: 2rem;">
            🧠 Student Stress Predictor
        </h3>
        <p style="color: #e4e6eb; font-size: 1.15rem; line-height: 2; text-align: justify;">
            This application uses <strong style="color: #64b5f6;">Advanced Machine Learning</strong> algorithms to predict 
            student stress levels based on lifestyle and academic factors. It combines data from multiple sources and 
            continuously improves as more users contribute their data, creating a more accurate and personalized 
            stress prediction system.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 0.3s; margin-bottom: 2rem;
                 background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                 border: 2px solid rgba(100, 181, 246, 0.2);">
        <h3 style="background: linear-gradient(135deg, #64b5f6 0%, #ffb74d 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 1.5rem; font-weight: 700; font-size: 2rem; text-align: center;">
            🎯 How It Works
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.4s; 
                     background: linear-gradient(135deg, rgba(100, 181, 246, 0.15) 0%, rgba(147, 51, 234, 0.15) 100%);
                     border: 2px solid rgba(100, 181, 246, 0.3);
                     box-shadow: 0 4px 20px rgba(100, 181, 246, 0.3);
                     transition: all 0.3s ease;"
             onmouseover="this.style.transform='translateY(-10px)'; this.style.boxShadow='0 8px 30px rgba(100, 181, 246, 0.5)'"
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 20px rgba(100, 181, 246, 0.3)'">
            <div style="text-align: center; font-size: 3.5rem; margin-bottom: 1rem; 
                        background: linear-gradient(135deg, #64b5f6 0%, #9333ea 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                1️⃣
            </div>
            <h4 style="color: #64b5f6; text-align: center; margin-bottom: 1rem; font-weight: 700; font-size: 1.3rem;">
                Data Collection
            </h4>
            <p style="color: #b8bdc8; text-align: center; line-height: 1.8; font-size: 1rem;">
                Users input lifestyle & academic information through an intuitive interface
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.6s; margin-top: 1.5rem;
                     background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(77, 182, 172, 0.15) 100%);
                     border: 2px solid rgba(16, 185, 129, 0.3);
                     box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
                     transition: all 0.3s ease;"
             onmouseover="this.style.transform='translateY(-10px)'; this.style.boxShadow='0 8px 30px rgba(16, 185, 129, 0.5)'"
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 20px rgba(16, 185, 129, 0.3)'">
            <div style="text-align: center; font-size: 3.5rem; margin-bottom: 1rem;
                        background: linear-gradient(135deg, #10b981 0%, #4db6ac 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                3️⃣
            </div>
            <h4 style="color: #10b981; text-align: center; margin-bottom: 1rem; font-weight: 700; font-size: 1.3rem;">
                ML Prediction
            </h4>
            <p style="color: #b8bdc8; text-align: center; line-height: 1.8; font-size: 1rem;">
                Trained Random Forest model predicts stress level (1-5 scale)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.5s;
                     background: linear-gradient(135deg, rgba(255, 183, 77, 0.15) 0%, rgba(251, 146, 60, 0.15) 100%);
                     border: 2px solid rgba(255, 183, 77, 0.3);
                     box-shadow: 0 4px 20px rgba(255, 183, 77, 0.3);
                     transition: all 0.3s ease;"
             onmouseover="this.style.transform='translateY(-10px)'; this.style.boxShadow='0 8px 30px rgba(255, 183, 77, 0.5)'"
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 20px rgba(255, 183, 77, 0.3)'">
            <div style="text-align: center; font-size: 3.5rem; margin-bottom: 1rem;
                        background: linear-gradient(135deg, #ffb74d 0%, #fb923c 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                2️⃣
            </div>
            <h4 style="color: #ffb74d; text-align: center; margin-bottom: 1rem; font-weight: 700; font-size: 1.3rem;">
                Feature Engineering
            </h4>
            <p style="color: #b8bdc8; text-align: center; line-height: 1.8; font-size: 1rem;">
                Calculate wellbeing & pressure scores from input data
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card" style="animation-delay: 0.7s; margin-top: 1.5rem;
                     background: linear-gradient(135deg, rgba(147, 51, 234, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
                     border: 2px solid rgba(147, 51, 234, 0.3);
                     box-shadow: 0 4px 20px rgba(147, 51, 234, 0.3);
                     transition: all 0.3s ease;"
             onmouseover="this.style.transform='translateY(-10px)'; this.style.boxShadow='0 8px 30px rgba(147, 51, 234, 0.5)'"
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 20px rgba(147, 51, 234, 0.3)'">
            <div style="text-align: center; font-size: 3.5rem; margin-bottom: 1rem;
                        background: linear-gradient(135deg, #9333ea 0%, #a855f7 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                4️⃣
            </div>
            <h4 style="color: #a855f7; text-align: center; margin-bottom: 1rem; font-weight: 700; font-size: 1.3rem;">
                Continuous Learning
            </h4>
            <p style="color: #b8bdc8; text-align: center; line-height: 1.8; font-size: 1rem;">
                User feedback continuously improves model accuracy
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 0.8s; margin-top: 2rem;
                 background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                 border: 2px solid rgba(100, 181, 246, 0.2);
                 box-shadow: 0 4px 20px rgba(100, 181, 246, 0.2);">
        <h3 style="background: linear-gradient(135deg, #64b5f6 0%, #a855f7 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 2rem; font-weight: 700; font-size: 2rem; text-align: center;">
            📊 Features & Engineering
        </h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
            <div style="background: linear-gradient(135deg, rgba(100, 181, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
                        padding: 2rem; border-radius: 15px; border: 2px solid rgba(100, 181, 246, 0.2);
                        box-shadow: 0 4px 15px rgba(100, 181, 246, 0.2);">
                <h4 style="color: #64b5f6; margin-bottom: 1.5rem; font-weight: 700; font-size: 1.4rem; text-align: center;">
                    📥 Input Features (5)
                </h4>
                <ul style="color: #e4e6eb; line-height: 2.5; font-size: 1.05rem; list-style: none; padding: 0;">
                    <li style="padding: 0.5rem; margin: 0.5rem 0; background: rgba(100, 181, 246, 0.1); border-radius: 8px;
                               border-left: 4px solid #64b5f6;">
                        😴 <strong>Sleep Quality</strong> (1-5)
                    </li>
                    <li style="padding: 0.5rem; margin: 0.5rem 0; background: rgba(239, 68, 68, 0.1); border-radius: 8px;
                               border-left: 4px solid #ef4444;">
                        🤕 <strong>Headaches</strong> per Week (0-7)
                    </li>
                    <li style="padding: 0.5rem; margin: 0.5rem 0; background: rgba(16, 185, 129, 0.1); border-radius: 8px;
                               border-left: 4px solid #10b981;">
                        👩‍🎓 <strong>Academic Performance</strong> (1-5)
                    </li>
                    <li style="padding: 0.5rem; margin: 0.5rem 0; background: rgba(255, 183, 77, 0.1); border-radius: 8px;
                               border-left: 4px solid #ffb74d;">
                        📖 <strong>Study Load</strong> (1-5)
                    </li>
                    <li style="padding: 0.5rem; margin: 0.5rem 0; background: rgba(147, 51, 234, 0.1); border-radius: 8px;
                               border-left: 4px solid #9333ea;">
                        🎾 <strong>Extracurricular</strong> Frequency (0-7)
                    </li>
                </ul>
            </div>
            <div style="background: linear-gradient(135deg, rgba(147, 51, 234, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
                        padding: 2rem; border-radius: 15px; border: 2px solid rgba(147, 51, 234, 0.2);
                        box-shadow: 0 4px 15px rgba(147, 51, 234, 0.2);">
                <h4 style="color: #a855f7; margin-bottom: 1.5rem; font-weight: 700; font-size: 1.4rem; text-align: center;">
                    🔧 Engineered Features (3)
                </h4>
                <ul style="color: #e4e6eb; line-height: 2.5; font-size: 1.05rem; list-style: none; padding: 0;">
                    <li style="padding: 1rem; margin: 0.8rem 0; background: rgba(16, 185, 129, 0.1); border-radius: 8px;
                               border-left: 4px solid #10b981;">
                        💚 <strong>Wellbeing Score</strong><br>
                        <span style="font-size: 0.9rem; color: #b8bdc8;">Sleep quality - headaches</span>
                    </li>
                    <li style="padding: 1rem; margin: 0.8rem 0; background: rgba(255, 183, 77, 0.1); border-radius: 8px;
                               border-left: 4px solid #ffb74d;">
                        📚 <strong>Academic Pressure</strong><br>
                        <span style="font-size: 0.9rem; color: #b8bdc8;">Study load + performance</span>
                    </li>
                    <li style="padding: 1rem; margin: 0.8rem 0; background: rgba(147, 51, 234, 0.1); border-radius: 8px;
                               border-left: 4px solid #9333ea;">
                        ⚖️ <strong>Total Workload</strong><br>
                        <span style="font-size: 0.9rem; color: #b8bdc8;">Academic + extracurricular</span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; animation-delay: 0.9s;
                     background: linear-gradient(135deg, rgba(100, 181, 246, 0.15) 0%, rgba(147, 51, 234, 0.15) 100%);
                     border: 2px solid rgba(100, 181, 246, 0.3);
                     box-shadow: 0 4px 20px rgba(100, 181, 246, 0.3);
                     padding: 2rem 1rem;
                     transition: all 0.3s ease;"
             onmouseover="this.style.transform='scale(1.05) translateY(-5px)'; this.style.boxShadow='0 8px 30px rgba(100, 181, 246, 0.5)'"
             onmouseout="this.style.transform='scale(1) translateY(0)'; this.style.boxShadow='0 4px 20px rgba(100, 181, 246, 0.3)'">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h4 style="color: #64b5f6; margin: 0.8rem 0; font-weight: 700; font-size: 1.1rem;">Algorithm</h4>
            <p style="color: #e4e6eb; font-size: 1rem; font-weight: 600;">Random Forest</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; animation-delay: 1s;
                     background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(77, 182, 172, 0.15) 100%);
                     border: 2px solid rgba(16, 185, 129, 0.3);
                     box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
                     padding: 2rem 1rem;
                     transition: all 0.3s ease;"
             onmouseover="this.style.transform='scale(1.05) translateY(-5px)'; this.style.boxShadow='0 8px 30px rgba(16, 185, 129, 0.5)'"
             onmouseout="this.style.transform='scale(1) translateY(0)'; this.style.boxShadow='0 4px 20px rgba(16, 185, 129, 0.3)'">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h4 style="color: #10b981; margin: 0.8rem 0; font-weight: 700; font-size: 1.1rem;">Accuracy</h4>
            <p style="color: #e4e6eb; font-size: 1rem; font-weight: 600;">94-97%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; animation-delay: 1.1s;
                     background: linear-gradient(135deg, rgba(255, 183, 77, 0.15) 0%, rgba(251, 146, 60, 0.15) 100%);
                     border: 2px solid rgba(255, 183, 77, 0.3);
                     box-shadow: 0 4px 20px rgba(255, 183, 77, 0.3);
                     padding: 2rem 1rem;
                     transition: all 0.3s ease;"
             onmouseover="this.style.transform='scale(1.05) translateY(-5px)'; this.style.boxShadow='0 8px 30px rgba(255, 183, 77, 0.5)'"
             onmouseout="this.style.transform='scale(1) translateY(0)'; this.style.boxShadow='0 4px 20px rgba(255, 183, 77, 0.3)'">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h4 style="color: #ffb74d; margin: 0.8rem 0; font-weight: 700; font-size: 1.1rem;">Samples</h4>
            <p style="color: #e4e6eb; font-size: 1rem; font-weight: 600;">1,600+</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="glass-card" style="text-align: center; animation-delay: 1.2s;
                     background: linear-gradient(135deg, rgba(147, 51, 234, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
                     border: 2px solid rgba(147, 51, 234, 0.3);
                     box-shadow: 0 4px 20px rgba(147, 51, 234, 0.3);
                     padding: 2rem 1rem;
                     transition: all 0.3s ease;"
             onmouseover="this.style.transform='scale(1.05) translateY(-5px)'; this.style.boxShadow='0 8px 30px rgba(147, 51, 234, 0.5)'"
             onmouseout="this.style.transform='scale(1) translateY(0)'; this.style.boxShadow='0 4px 20px rgba(147, 51, 234, 0.3)'">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🗂️</div>
            <h4 style="color: #a855f7; margin: 0.8rem 0; font-weight: 700; font-size: 1.1rem;">Datasets</h4>
            <p style="color: #e4e6eb; font-size: 1rem; font-weight: 600;">4 combined</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 1.3s; margin-top: 2rem;
                 background: linear-gradient(135deg, rgba(77, 182, 172, 0.15) 0%, rgba(100, 181, 246, 0.15) 100%);
                 border: 2px solid rgba(77, 182, 172, 0.3);
                 box-shadow: 0 4px 20px rgba(77, 182, 172, 0.2);">
        <h3 style="background: linear-gradient(135deg, #4db6ac 0%, #64b5f6 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 1.5rem; font-weight: 700; font-size: 2rem; text-align: center;">
            🔄 Data Flow Pipeline
        </h3>
        <div style="text-align: center; background: rgba(77, 182, 172, 0.1); 
                    padding: 2.5rem; border-radius: 20px; margin: 1.5rem 0;
                    border: 2px solid rgba(77, 182, 172, 0.2);
                    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);">
            <p style="color: #e4e6eb; font-size: 1.2rem; line-height: 2.5; font-weight: 600;">
                <span style="color: #64b5f6;">📥 User Input</span> 
                <span style="color: #4db6ac;">→</span> 
                <span style="color: #ffb74d;">🔧 Feature Engineering</span> 
                <span style="color: #4db6ac;">→</span><br>
                <span style="color: #10b981;">🤖 ML Model</span> 
                <span style="color: #4db6ac;">→</span> 
                <span style="color: #a855f7;">🎯 Prediction</span><br>
                <span style="color: #64b5f6; font-size: 2rem;">↓</span><br>
                <span style="color: #4db6ac;">💾 Save to Database</span> 
                <span style="color: #4db6ac;">→</span> 
                <span style="color: #ffb74d;">📈 Future Improvements</span>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="animation-delay: 1.4s; margin-top: 2rem;
                 background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(255, 183, 77, 0.1) 100%);
                 border: 2px solid rgba(239, 68, 68, 0.3);
                 box-shadow: 0 4px 20px rgba(239, 68, 68, 0.2);">
        <h3 style="background: linear-gradient(135deg, #ef4444 0%, #ffb74d 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin-bottom: 1.5rem; font-weight: 700; font-size: 1.8rem; text-align: center;">
            ⚠️ Important Disclaimer
        </h3>
        <p style="color: #e4e6eb; font-size: 1.15rem; line-height: 2; text-align: center; 
                  padding: 1.5rem; background: rgba(239, 68, 68, 0.05); border-radius: 15px;">
            This tool is for <strong style="color: #ffb74d;">educational and informational purposes only</strong>. 
            It should <strong style="color: #ef4444;">NOT replace</strong> professional medical or psychological advice. 
            If you're experiencing <strong style="color: #ef4444;">severe stress</strong> or mental health concerns, 
            please consult with a qualified healthcare professional immediately. 🏥
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; animation-delay: 1.5s;
                background: linear-gradient(135deg, rgba(100, 181, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
                border-radius: 20px; border: 2px solid rgba(100, 181, 246, 0.2);">
        <p style="background: linear-gradient(135deg, #64b5f6 0%, #a855f7 100%);
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                  font-size: 1.1rem; font-weight: 700; margin: 0;">
            ⚡ StressAI v2.0 (Dark Mode) • Built with ❤️ using Advanced ML
        </p>
        <p style="color: #b8bdc8; font-size: 0.9rem; margin-top: 0.8rem; font-weight: 500;">
            Powered by Random Forest • Groq AI Integration • Real-time Analytics
        </p>
        <p style="color: #64b5f6; font-size: 0.85rem; margin-top: 0.5rem;">
            Last Updated: October 2025
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

