# 🚀 Streamlit Cloud Deployment Guide

## 🎯 Deploy Your App to Streamlit Cloud (FREE!)

This guide shows you how to deploy your Student Stress Predictor app to Streamlit Cloud while keeping your API key **100% secure**.

---

## ✨ Why Streamlit Cloud?

- ✅ **Free hosting** for public repos
- ✅ **Built-in secrets management** (secure API keys)
- ✅ **Auto-deploy** on git push
- ✅ **HTTPS** by default
- ✅ **No server management** needed
- ✅ **Share with anyone** via URL

---

## 📋 Prerequisites

Before deploying, make sure you have:

- [x] GitHub account
- [x] This repository pushed to GitHub (without API key in files!)
- [x] Groq API key (from https://console.groq.com)
- [x] Streamlit Cloud account (sign up with GitHub)

---

## 🔒 Step 1: Secure Your Repository

### Make Sure These Files Are in `.gitignore`:

```bash
# Check .gitignore includes:
cat .gitignore | grep -E "(secrets.toml|ai_config.json|.env)"

# Should show:
# .streamlit/secrets.toml
# ai_config.json
# .env
```

### Verify No Secrets in Git:

```bash
# Search for API keys - should find NOTHING
git log --all -p | grep -i "gsk_"

# If found, follow GITHUB_SECURITY_INSTRUCTIONS.md first!
```

---

## 🚀 Step 2: Push to GitHub

```bash
cd /home/omindu/Documents/Python/student_streess_ML

# Check what will be committed (should NOT include secrets)
git status

# Add safe files
git add .
git commit -m "feat: Streamlit Cloud ready with secure secrets management"

# Push to GitHub
git push origin master
```

---

## ☁️ Step 3: Deploy to Streamlit Cloud

### 3.1 Sign Up for Streamlit Cloud

1. Go to: **https://share.streamlit.io**
2. Click **"Sign up with GitHub"**
3. Authorize Streamlit Cloud to access your repos

### 3.2 Create New App

1. Click **"New app"**
2. Select your repository: `OminduD/student_streess_ML`
3. Set branch: `master`
4. Set main file path: `app.py`
5. **DON'T CLICK DEPLOY YET!**

### 3.3 Add Secrets (IMPORTANT!)

1. Click **"Advanced settings"** ⚙️
2. In the **"Secrets"** section, add:

```toml
# Copy and paste this into Secrets section:
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

**Replace** `your_actual_groq_api_key_here` with your real Groq API key!

### 3.4 Deploy!

1. Click **"Deploy!"** 🚀
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://yourusername-student-stress-ml.streamlit.app`

---

## 🔐 How Secrets Work

### On Streamlit Cloud:
```python
# app.py automatically reads from st.secrets
import streamlit as st
api_key = st.secrets["GROQ_API_KEY"]  # Secure, not in code!
```

### Locally:
```bash
# Create .streamlit/secrets.toml (gitignored)
mkdir -p .streamlit
echo 'GROQ_API_KEY = "your_key_here"' > .streamlit/secrets.toml

# Or use environment variable
export GROQ_API_KEY="your_key_here"
```

### Priority Order:
1. ☁️ **Streamlit secrets** (on Streamlit Cloud)
2. 🖥️ **Environment variables** (local/server)
3. 📄 **Config file** (fallback, not recommended)

---

## 📝 Step 4: Configure Your Deployment

### Custom Domain (Optional)

Streamlit Cloud gives you: `https://share.streamlit.io/yourusername/repo-name/main`

You can add a custom domain in settings!

### Auto-Deploy on Push

By default, every `git push` triggers a new deployment:

```bash
# Make changes
git add .
git commit -m "Update UI"
git push origin master

# Streamlit Cloud auto-deploys in 2-3 minutes! 🚀
```

### Resource Limits (Free Tier)

- **RAM**: 1 GB
- **CPU**: Shared
- **Bandwidth**: Unlimited
- **Apps**: Unlimited for public repos

If you need more, upgrade to Streamlit Cloud Teams/Enterprise.

---

## 🧪 Step 5: Test Your Deployment

### 5.1 Check App Loads

Visit your app URL: `https://yourusername-student-stress-ml.streamlit.app`

Should show:
- ✅ Animated gradient background
- ✅ Glassmorphism cards
- ✅ All UI elements

### 5.2 Test AI Recommendations

1. Go to **"Predict"** page
2. Enter test data
3. Click **"Predict My Stress Level"**
4. Should see: **"⚡ Powered by Groq AI (Lightning Fast!)"**
5. AI recommendations should appear

### 5.3 Check Logs

In Streamlit Cloud dashboard:
1. Click **"Manage app"**
2. View **"Logs"** tab
3. Should NOT show "No API key found"
4. Should show successful API calls

---

## ⚙️ Managing Your Deployment

### Update Secrets

1. Go to: https://share.streamlit.io
2. Click your app → **"Settings"** ⚙️
3. Edit **"Secrets"** section
4. Click **"Save"**
5. App auto-restarts with new secrets

### View Logs

```bash
# In Streamlit Cloud dashboard:
Manage app → Logs
```

### Reboot App

```bash
# In Streamlit Cloud dashboard:
Manage app → ⋮ (three dots) → Reboot app
```

### Delete App

```bash
# In Streamlit Cloud dashboard:
Manage app → ⋮ (three dots) → Delete app
```

---

## 🐛 Troubleshooting

### Issue 1: "No API key found"

**Symptoms**: App loads but shows "Using rule-based recommendations"

**Solution**:
1. Check secrets are added in Streamlit Cloud dashboard
2. Make sure key is named exactly: `GROQ_API_KEY`
3. No quotes around the key name (only around value)
4. Reboot app after adding secrets

**Correct format in Secrets:**
```toml
GROQ_API_KEY = "gsk_your_key_here"
```

**Incorrect formats:**
```toml
# ❌ Wrong - has quotes around key name
"GROQ_API_KEY" = "gsk_your_key_here"

# ❌ Wrong - missing value quotes
GROQ_API_KEY = gsk_your_key_here

# ❌ Wrong - wrong variable name
GROQ_KEY = "gsk_your_key_here"
```

---

### Issue 2: App Won't Load

**Symptoms**: Deployment fails or shows errors

**Solution**:

1. **Check requirements.txt exists**:
```bash
ls requirements.txt
```

2. **Check all required files are in repo**:
```bash
git ls-files | grep -E "(app.py|requirements.txt|ai_recommender.py)"
```

3. **Check Streamlit Cloud logs**:
   - Dashboard → Your app → Logs
   - Look for import errors or missing dependencies

4. **Verify Python version** (if specified in `.python-version`):
```bash
python --version  # Should be 3.8+
```

---

### Issue 3: API Key Still in Repo

**Symptoms**: GitHub shows security warning

**Solution**:
1. **DO NOT DEPLOY YET!**
2. Follow `GITHUB_SECURITY_INSTRUCTIONS.md` first
3. Remove key from Git history
4. Then deploy to Streamlit Cloud

---

### Issue 4: Model Files Too Large

**Symptoms**: Deployment times out or fails

**Solution**:

1. **Check model size**:
```bash
ls -lh model/stress_predictor_model.joblib
# If > 100MB, it's too large
```

2. **Use Git LFS** (Large File Storage):
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.joblib"
git add .gitattributes
git commit -m "Add Git LFS for model files"
git push
```

3. **Or retrain with smaller model**:
   - Reduce `max_depth` in training
   - Use fewer trees in Random Forest

---

### Issue 5: Slow Performance

**Symptoms**: App takes too long to load predictions

**Solution**:

1. **Optimize model loading** (cache it):
```python
import streamlit as st

@st.cache_resource
def load_model():
    return joblib.load('model/stress_predictor_model.joblib')

model = load_model()  # Only loads once!
```

2. **Use lighter Groq model**:
   - Change to `llama-3.1-8b-instant` (faster)
   - In Streamlit Cloud secrets:
```toml
GROQ_API_KEY = "your_key"
GROQ_MODEL = "llama-3.1-8b-instant"
```

---

## 📊 Monitor Your App

### Usage Statistics

Streamlit Cloud dashboard shows:
- 📈 **Visitors** over time
- 🌍 **Geographic distribution**
- ⏱️ **Resource usage** (RAM, CPU)
- 🚨 **Error logs**

### Set Up Alerts

1. Dashboard → Your app → Settings
2. Enable email notifications for:
   - Deployment failures
   - High resource usage
   - Errors

---

## 🔄 Local Testing Before Deploy

Always test locally first:

```bash
# Create local secrets (gitignored)
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
GROQ_API_KEY = "your_test_key_here"
EOF

# Run locally
streamlit run app.py

# Test all features:
# ✅ UI loads properly
# ✅ Predictions work
# ✅ AI recommendations appear
# ✅ No console errors

# If all good, push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin master
```

---

## 🎉 Success Checklist

- [ ] Repository on GitHub (no secrets in code)
- [ ] Signed up for Streamlit Cloud
- [ ] Created new app on Streamlit Cloud
- [ ] Added `GROQ_API_KEY` to secrets
- [ ] Deployed successfully
- [ ] App URL is live
- [ ] UI loads with animations
- [ ] Predictions work
- [ ] AI recommendations appear
- [ ] No errors in logs
- [ ] Tested all pages (Predict, Statistics, About)

---

## 🚀 Your App is Live!

### Share Your App

Your app is now live at:
```
https://share.streamlit.io/OminduD/student_streess_ML/master/app.py
```

Share this URL with:
- 🎓 Students for stress predictions
- 👨‍🏫 Teachers for research
- 💼 Employers for portfolio showcase
- 🌐 Social media for engagement

### Next Steps

1. **Custom Domain** (optional): Add in Streamlit Cloud settings
2. **Analytics**: Track usage in dashboard
3. **Updates**: Push to GitHub → auto-deploys
4. **Upgrade** (if needed): Streamlit Cloud Teams for more resources

---

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-cloud
- **Secrets Management**: https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
- **Groq Docs**: https://console.groq.com/docs
- **Git LFS**: https://git-lfs.github.com

---

## 🆘 Need Help?

### Streamlit Support
- Community Forum: https://discuss.streamlit.io
- GitHub Issues: https://github.com/streamlit/streamlit/issues

### Your Project Issues
- Check: `TROUBLESHOOTING.md`
- Security: `GITHUB_SECURITY_INSTRUCTIONS.md`
- Setup: `QUICK_RUN_GUIDE.md`

---

## 🎊 Congratulations!

You've successfully deployed your ML app to the cloud with secure API key management!

**Your app features:**
- ✨ Ultra-modern UI with animations
- 🤖 AI-powered recommendations (Groq)
- 🔒 Secure secrets management
- ☁️ Cloud deployment (free!)
- 🌐 Shareable URL

**Perfect for:**
- 📊 Portfolio projects
- 🎓 Academic presentations  
- 💼 Job applications
- 🌟 Open source contributions

**Enjoy your deployed app! 🚀**
