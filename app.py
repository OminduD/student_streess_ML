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

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stress-level-1 { color: #2ecc71; font-weight: bold; }
    .stress-level-2 { color: #3498db; font-weight: bold; }
    .stress-level-3 { color: #f39c12; font-weight: bold; }
    .stress-level-4 { color: #e67e22; font-weight: bold; }
    .stress-level-5 { color: #e74c3c; font-weight: bold; }
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
    # Header
    st.markdown('<div class="main-header">🧠 Student Stress Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Stress Level Assessment & Data Collection</div>', unsafe_allow_html=True)
    
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
    st.header("🔮 Stress Level Prediction")
    
    st.markdown("""
    ### How it works:
    1. Enter your information using the sliders below
    2. Click **Predict My Stress Level**
    3. View your results and recommendations
    4. Optionally submit your actual stress level to help improve the model
    """)
    
    st.markdown("---")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Lifestyle Factors")
        
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
        st.subheader("📚 Academic Factors")
        
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
            <div style='text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 1rem;'>
                <h1 style='font-size: 4rem; margin: 0;'>{emoji}</h1>
                <h2 class='stress-level-{predicted_stress}' style='margin: 0.5rem 0;'>
                    Stress Level: {predicted_stress}/5
                </h2>
                <h3 style='color: #555;'>{level_name}</h3>
                <p style='font-size: 1.1rem;'>{description}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("---")
        st.subheader("💡 AI-Powered Recommendations")
        
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
            st.info(f"**{i}.** {rec}")
        
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
    st.header("📊 Data Statistics & Insights")
    
    stats_df = load_statistics()
    
    if stats_df is None or stats_df.empty:
        st.info("📭 No data collected yet. Start by making predictions!")
        return
    
    st.success(f"✅ Displaying **{len(stats_df)}** entries from the database.")
    
    # Overview metrics
    st.subheader("📈 Overview")
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
            
            dist_col1, dist_col2 = st.columns(2)
            
            with dist_col1:
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
            
            with dist_col2:
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
    
    feat_dist_col1, feat_dist_col2 = st.columns(2)
    
    with feat_dist_col1:
        fig = px.histogram(
            stats_df,
            x='sleep_quality',
            nbins=5,
            title='Sleep Quality Distribution',
            labels={'sleep_quality': 'Sleep Quality'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with feat_dist_col2:
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
            st.warning(f"Timeline visualization not available: {e}")
    
    # Raw data
    with st.expander("🔍 View Raw Data"):
        st.dataframe(stats_df, use_container_width=True)
        
        # Download button
        # Download button
        csv = stats_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"stress_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )def show_about_page():
    """Display about page"""

def show_about_page():
    """Display about page"""
    st.header("ℹ️ About This Application")
    
    st.markdown("""
    ### 🧠 Student Stress Predictor
    
    This application uses **Machine Learning** to predict student stress levels based on lifestyle 
    and academic factors. It combines data from multiple sources and continuously improves as 
    more users contribute their data.
    
    ---
    
    ### 🎯 How It Works
    
    1. **Data Collection**: Users input their lifestyle and academic information
    2. **Feature Engineering**: The system calculates additional metrics like wellbeing score
    3. **ML Prediction**: A trained model predicts stress level (1-5 scale)
    4. **Continuous Learning**: User feedback improves the model over time
    
    ---
    
    ### 📊 Features Used
    
    **Input Features (5):**
    - 😴 Sleep Quality (1-5)
    - 🤕 Headaches per Week (0-7)
    - 👩‍🎓 Academic Performance (1-5)
    - 📖 Study Load (1-5)
    - 🎾 Extracurricular Frequency (0-7)
    
    **Engineered Features (3):**
    - 💚 Wellbeing Score
    - 📚 Academic Pressure
    - ⚖️ Total Workload
    
    ---
    
    ### 🏆 Model Performance
    
    - **Algorithm**: Random Forest / Gradient Boosting
    - **Accuracy**: 94-97%
    - **Training Samples**: 1,600+
    - **Data Sources**: 4 combined datasets
    
    ---
    
    ### 🔄 Data Flow
    
    ```
    User Input → Feature Engineering → ML Model → Prediction
                        ↓
                  Save to Supabase → Future Model Retraining
    ```
    
    ---
    
    ### 🚀 Getting Started
    
    **First Time Setup:**
    ```bash
    # Install dependencies
    pip install -r requirements.txt
    
    # Process data
    python scripts/ingest_multi_dataset.py
    
    # Train model
    python scripts/train_multi_dataset.py
    
    # Run app
    streamlit run app.py
    ```
    
    **Retrain with new data:**
    ```bash
    python scripts/download_training_data.py # Downloads from Supabase
    python scripts/ingest_multi_dataset.py   # Includes new data
    python scripts/train_multi_dataset.py    # Retrains with new data
    ```
    
    ---
    
    ### 📚 Resources
    
    - **Project Documentation**: See README.md
    - **Deployment Guide**: See DEPLOYMENT_GUIDE.md
    - **Analysis Notebook**: notebooks/multi_dataset_analysis.ipynb
    
    ---
    
    ### ⚠️ Disclaimer
    
    This tool is for **educational and informational purposes only**. It should not replace 
    professional medical or psychological advice. If you're experiencing severe stress, 
    please consult with a qualified healthcare professional.
    
    ---
    
    ### 👨‍💻 Technical Details
    
    - **Framework**: Streamlit
    - **ML Library**: scikit-learn
    - **Data Storage**: Supabase (PostgreSQL)
    - **Visualization**: Plotly
    
    ---
    
    **Version**: 1.1.0 (Cloud-ready)
    **Last Updated**: October 2025
    """)

if __name__ == "__main__":
    main()
