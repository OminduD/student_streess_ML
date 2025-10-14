# 🔍 Theme Toggle Debug Guide

## Quick Test Steps

### 1. Run the App Locally
```bash
streamlit run app.py
```

### 2. Look for Debug Indicators

At the top of the page, you should see:
- **🎨 Theme: LIGHT** (or DARK)
- **Three colored squares** showing the accent colors
  - Light mode: Blue (#4a90e2), Green (#50c878), Orange (#e67e22)
  - Dark mode: Light Blue (#64b5f6), Teal (#4db6ac), Amber (#ffb74d)

### 3. Click the Theme Button
- Look for 🌙 (moon) or ☀️ (sun) button in top-right
- Click it
- Watch the debug info change
- Watch the color squares change
- Background should animate and change colors

---

## What You Should See

### ✅ LIGHT MODE Active:
```
🎨 Theme: LIGHT
[Blue square] [Green square] [Orange square]
Background: Soft blues & warm creams
Button shows: 🌙 (moon icon)
```

### ✅ DARK MODE Active:
```
🎨 Theme: DARK
[Light Blue square] [Teal square] [Amber square]
Background: Deep purples & dark blues
Button shows: ☀️ (sun icon)
```

---

## 🚨 Troubleshooting

### Problem 1: Only One Theme Shows

**Symptom**: Colors don't change when clicking button

**Check:**
1. Look at debug text - does it say "LIGHT" or "DARK"?
2. Do the color squares change when you click?
3. Does the button icon change (🌙 ↔ ☀️)?

**If debug text changes but colors don't:**
```python
# This means theme state is updating but CSS isn't re-rendering
# Solution: Clear browser cache (Ctrl+F5)
```

**If debug text doesn't change:**
```python
# This means button click isn't working
# Check browser console for errors (F12)
```

### Problem 2: Button Not Visible

**Check:**
```bash
# Look in terminal for errors when running:
streamlit run app.py

# Common error: Missing package
pip install streamlit --upgrade
```

### Problem 3: Colors Look the Same

**Test:**
1. Open browser DevTools (F12)
2. Click "Elements" tab
3. Find `<div class="stApp">`
4. Check `background` property
5. Should show gradient with different colors for each theme

**Expected:**
- Light: `#e8f4f8, #fef5e7, #fdeef4, #e8f8f5`
- Dark: `#1a1d29, #2d1b2e, #1e2837, #252134`

---

## 🧪 Manual Testing

### Test 1: Session State
Add to your app temporarily:
```python
st.sidebar.write("### Debug Info")
st.sidebar.write(f"session_state.theme: {st.session_state.theme}")
st.sidebar.write(f"current_theme: {current_theme}")
st.sidebar.write(f"query_params: {st.query_params}")
```

### Test 2: Color Variables
Add after theme colors are set:
```python
st.sidebar.write("### Theme Colors")
st.sidebar.write(f"bg_gradient: {bg_gradient[:50]}...")
st.sidebar.write(f"text_primary: {text_primary}")
st.sidebar.write(f"accent_1: {accent_1}")
```

### Test 3: CSS Injection
Check if CSS is being applied:
```python
st.sidebar.markdown(f"""
<div style="padding: 20px; background: {container_bg}; border: 2px solid {card_border}; border-radius: 10px;">
    <p style="color: {text_primary}; margin: 0;">Container BG Test</p>
    <p style="color: {text_secondary}; margin: 5px 0;">Secondary Text Test</p>
    <div style="background: {accent_1}; padding: 10px; border-radius: 5px; color: white; margin-top: 10px;">
        Accent 1 Test
    </div>
</div>
""", unsafe_allow_html=True)
```

---

## 🔧 Common Fixes

### Fix 1: Clear Streamlit Cache
```bash
# Stop the app (Ctrl+C)
# Clear cache
rm -rf ~/.streamlit/cache

# Restart
streamlit run app.py
```

### Fix 2: Force Theme on Startup
Edit `app.py` line 30:
```python
# Change from:
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# To force dark:
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Start with dark mode
```

### Fix 3: Check Browser Cache
```
1. Open app in incognito/private window
2. Press Ctrl+Shift+Delete
3. Clear cache and reload
4. Or hard refresh: Ctrl+F5
```

### Fix 4: Verify Theme Logic
Check that this code is at the TOP of your file (before CSS):
```python
# Should be around line 30-50
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

query_params = st.query_params
if 'theme' in query_params:
    st.session_state.theme = query_params['theme']

current_theme = st.session_state.theme

# Then colors...
if current_theme == 'light':
    # light colors
else:
    # dark colors

# THEN CSS injection
st.markdown(f"""<style>...""")
```

---

## 📊 Expected vs Actual

### What SHOULD Happen:

1. **App starts** → Default theme: LIGHT
2. **Debug shows**: "Theme: LIGHT" + light colored squares
3. **Background**: Soft blues and creams
4. **Click 🌙 button**
5. **Debug changes to**: "Theme: DARK" + darker colored squares
6. **Background**: Deep purples and blues
7. **URL updates**: `?theme=dark` appears
8. **Refresh page** → Theme stays DARK

### What SHOULDN'T Happen:

❌ Colors stay the same after clicking
❌ Debug text doesn't update
❌ Button doesn't respond
❌ Theme resets to light on refresh
❌ Both themes look identical

---

## 🎯 Diagnostic Checklist

Run through this list:

- [ ] App starts without errors
- [ ] Debug text shows "Theme: LIGHT" on first load
- [ ] Three colored squares are visible
- [ ] Button shows 🌙 (moon) icon
- [ ] Clicking button triggers page reload
- [ ] After click, debug text changes to "Theme: DARK"
- [ ] Color squares change to different colors
- [ ] Background gradient changes colors
- [ ] Button icon changes to ☀️ (sun)
- [ ] URL includes `?theme=dark`
- [ ] Refreshing page keeps dark theme
- [ ] Clicking again switches back to light

**If all checked**: Theme system working! ✅
**If some unchecked**: See which step fails

---

## 🆘 Still Not Working?

### Share This Info:

1. **Streamlit version**: 
   ```bash
   streamlit --version
   ```

2. **Python version**: 
   ```bash
   python --version
   ```

3. **Debug output**: What does the debug text show?

4. **Browser console**: Any errors? (F12 → Console tab)

5. **Button behavior**: Does it rerun the app?

6. **Color values**: Run this and share output:
   ```python
   st.write(f"current_theme = {current_theme}")
   st.write(f"accent_1 = {accent_1}")
   st.write(f"accent_2 = {accent_2}")
   st.write(f"bg_gradient = {bg_gradient}")
   ```

---

## 🎨 Visual Comparison

### Light Mode Should Look Like:
- **Background**: Light pastel colors (pink, blue, yellow tints)
- **Text**: Dark gray (easy to read)
- **Cards**: White with subtle shadows
- **Buttons**: Blue/green gradient
- **Overall feel**: Bright, airy, daytime

### Dark Mode Should Look Like:
- **Background**: Deep purple/blue (almost black)
- **Text**: Light gray/white (easy to read)
- **Cards**: Dark gray with blue tint
- **Buttons**: Lighter blue/teal gradient
- **Overall feel**: Dark, moody, nighttime

---

## ✅ Remove Debug Info

Once working, remove the debug code:

Find this in `app.py` (around line 558):
```python
with col1:
    # Debug info with visual indicators (remove after testing)
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="color: {text_primary};">🎨 Theme: <strong>{current_theme.upper()}</strong></span>
            ...
        </div>
    """, unsafe_allow_html=True)
```

Replace with:
```python
with col1:
    st.write("")  # Just a spacer
```

---

**Last Updated**: October 14, 2025
**Status**: Debugging Active
**Next Step**: Run app and check debug output
