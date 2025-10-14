"""
Minimal Theme Toggle Test
Run this to test if theme switching works
"""
import streamlit as st

st.set_page_config(page_title="Theme Test", page_icon="🎨", layout="wide")

# Initialize theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Check query params
query_params = st.query_params
if 'theme' in query_params:
    st.session_state.theme = query_params['theme']

def toggle_theme():
    new_theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.session_state.theme = new_theme
    st.query_params['theme'] = new_theme

current_theme = st.session_state.theme

# Set theme colors
if current_theme == 'light':
    bg_color = "#e8f4f8"
    text_color = "#2c3e50"
    accent = "#4a90e2"
    card_bg = "rgba(255, 255, 255, 0.9)"
else:
    bg_color = "#1a1d29"
    text_color = "#e4e6eb"
    accent = "#64b5f6"
    card_bg = "rgba(30, 35, 45, 0.9)"

# Apply CSS with theme colors
st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color} !important;
        transition: all 0.3s ease;
    }}
    
    .main .block-container {{
        background: {card_bg} !important;
        border-radius: 20px;
        padding: 2rem;
    }}
    
    h1, h2, h3, p {{
        color: {text_color} !important;
    }}
    
    .test-box {{
        background: {accent};
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# Header with theme info
st.title("🎨 Theme Toggle Test")
st.write(f"**Current Theme:** {current_theme.upper()}")
st.write(f"**Background Color:** {bg_color}")
st.write(f"**Text Color:** {text_color}")
st.write(f"**Accent Color:** {accent}")

# Toggle button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    theme_icon = "🌙 Switch to Dark" if current_theme == "light" else "☀️ Switch to Light"
    if st.button(theme_icon, key=f"toggle_{current_theme}", use_container_width=True):
        toggle_theme()
        st.rerun()

# Visual test boxes
st.markdown(f"""
<div class="test-box">
    This box uses the accent color: {accent}
</div>
""", unsafe_allow_html=True)

st.write("---")

# Show detailed info
with st.expander("🔍 Debug Information"):
    st.json({
        "session_state.theme": st.session_state.theme,
        "current_theme": current_theme,
        "query_params": dict(st.query_params),
        "bg_color": bg_color,
        "text_color": text_color,
        "accent_color": accent
    })

st.write("---")
st.success("✅ If colors change when you click the button, theme toggle is working!")
st.info("💡 Check the URL - it should include `?theme=light` or `?theme=dark`")
