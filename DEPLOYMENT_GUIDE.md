# 🚀 Deployment Guide - Student Stress Predictor

This guide covers deploying your Streamlit app with **persistent data storage** and **automated model retraining**.

---

## 📋 Overview

**Problem**: When deploying on Streamlit Cloud, file writes don't persist (ephemeral filesystem).

**Solution**: 
- Use **Supabase** (cloud database) for persistent data storage
- Use **GitHub Actions** for automated hourly model retraining

---

## 🗄️ Part 1: Setting Up Supabase (Cloud Database)

### Step 1: Create Supabase Account

1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub (recommended)

### Step 2: Create a New Project

1. Click "New Project"
2. Choose organization (or create new)
3. Set project name: `student-stress-predictor`
4. Set database password (save this!)
5. Choose region (closest to your users)
6. Click "Create new project"
7. Wait 2-3 minutes for setup

### Step 3: Create Database Table

1. Go to **SQL Editor** in left sidebar
2. Click "New Query"
3. Paste this SQL:

```sql
-- Create user_inputs table
CREATE TABLE user_inputs (
    id BIGSERIAL PRIMARY KEY,
    sleep_quality INTEGER NOT NULL,
    headaches_per_week INTEGER NOT NULL,
    academic_performance INTEGER NOT NULL,
    study_load INTEGER NOT NULL,
    extracurricular_frequency INTEGER NOT NULL,
    stress_level INTEGER,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    source TEXT DEFAULT 'streamlit_app',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX idx_timestamp ON user_inputs(timestamp DESC);
CREATE INDEX idx_stress_level ON user_inputs(stress_level) WHERE stress_level IS NOT NULL;

-- Enable Row Level Security (RLS)
ALTER TABLE user_inputs ENABLE ROW LEVEL SECURITY;

-- Create policy to allow insert/select with service key
CREATE POLICY "Enable insert for anon" ON user_inputs
    FOR INSERT TO anon
    WITH CHECK (true);

CREATE POLICY "Enable select for anon" ON user_inputs
    FOR SELECT TO anon
    USING (true);
```

4. Click "Run" (F5)
5. You should see: "Success. No rows returned"

### Step 4: Get API Credentials

1. Go to **Settings** → **API**
2. Copy these values:
   - **Project URL**: `https://jujcyoomunwqyftyfezf.supabase.co`
   - **Project API Key** (service_role): `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1amN5b29tdW53cXlmdHlmZXpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI1OTI1NSwiZXhwIjoyMDc1ODM1MjU1fQ.r2dIrJYv-pRMTdQhqPwPvbGWn68ti7RTrTj49J7Z7xg`
   
⚠️ **Important**: Use the `service_role` key, NOT the `anon` key!

---

## 🔧 Part 2: Update Your Application

### Step 1: Install Supabase Package

Add to `requirements.txt`:

```txt
supabase==2.0.3
```

### Step 2: Update app.py

Replace the `save_to_csv` function calls with the new database module:

```python
from database import get_storage

# At the top of app.py, replace the save_to_csv function with:
def save_user_input(data, include_stress=False):
    """Save user input using database module"""
    storage = get_storage()
    return storage.save_user_input(data, include_stress)

# Replace load_statistics function with:
def load_statistics():
    """Load statistics from database"""
    storage = get_storage()
    return storage.get_all_data()
```

---

## ☁️ Part 3: Deploy to Streamlit Cloud

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Add Supabase integration and automated retraining"
git push origin master
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `student_streess_ML`
5. Set main file path: `app.py`
6. Click "Advanced settings"

### Step 3: Add Environment Variables (Secrets)

In "Advanced settings" → "Secrets", add:

```toml
# Supabase Configuration
SUPABASE_URL = "https://jujcyoomunwqyftyfezf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1amN5b29tdW53cXlmdHlmZXpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI1OTI1NSwiZXhwIjoyMDc1ODM1MjU1fQ.r2dIrJYv-pRMTdQhqPwPvbGWn68ti7RTrTj49J7Z7xg"
```

Replace with YOUR actual Supabase credentials!

7. Click "Deploy"
8. Wait 2-3 minutes

---

## 🤖 Part 4: Setup Automated Retraining (GitHub Actions)

### Step 1: Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click "New repository secret"
4. Add these secrets:

| Name | Value |
|------|-------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase service_role key |

### Step 2: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. The workflow is already created in `.github/workflows/retrain_model.yml`

### Step 3: Test the Workflow

1. Go to **Actions** tab
2. Click "Automated Model Retraining" in the left sidebar
3. Click "Run workflow" → "Run workflow"
4. Wait for it to complete (2-5 minutes)

---

## 📊 How It Works

### Data Flow:

```
User fills form → Data saved to Supabase (cloud database)
                ↓
Every hour, GitHub Actions:
    1. Downloads new data from Supabase
    2. Checks if enough new data (min 10 samples)
    3. If yes: Retrains model
    4. Commits updated model to GitHub
    5. Streamlit Cloud auto-redeploys with new model
```

### Automatic Updates:

- **Data**: Instantly saved to Supabase ✓
- **Model**: Retrained every hour if enough new data ✓
- **App**: Auto-redeploys when model updates ✓

---

## 🔍 Monitoring & Verification

### Check if data is saving:

1. Go to Supabase dashboard
2. Click **Table Editor** → **user_inputs**
3. You should see rows appearing after users submit data

### Check automated retraining:

1. Go to GitHub repository
2. Click **Actions** tab
3. View recent workflow runs
4. Check logs for success/failure

### View model metrics:

After retraining, check `model/metrics.json` in your repository for updated accuracy.

---

## ⚙️ Configuration Options

### Change Retraining Frequency

Edit `.github/workflows/retrain_model.yml`:

```yaml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours
  - cron: '0 0 * * *'    # Daily at midnight
  - cron: '0 */6 * * *'  # Every 6 hours
```

### Change Minimum Data Required

Edit `scripts/check_new_data.py`:

```python
def check_new_data(min_new_samples=20):  # Require 20 samples instead of 10
```

---

## 🛠️ Troubleshooting

### Issue: Data not saving to Supabase

**Solution**:
1. Check Supabase credentials in Streamlit secrets
2. Verify table was created correctly
3. Check RLS policies are set
4. Look at Streamlit logs for error messages

### Issue: GitHub Actions failing

**Solution**:
1. Check GitHub Actions secrets are set correctly
2. Verify `requirements.txt` includes `supabase==2.0.3`
3. Check Actions logs for specific error
4. Ensure repository has write permissions

### Issue: Model not updating

**Solution**:
1. Verify GitHub Actions completed successfully
2. Check if enough new data was collected
3. Look at workflow logs
4. Manually trigger workflow to test

---

## 💰 Cost Considerations

### Free Tier Limits:

**Supabase Free Tier:**
- 500 MB database storage
- 1 GB file storage
- 2 GB bandwidth per month
- Suitable for ~50,000-100,000 user inputs

**GitHub Actions Free Tier:**
- 2,000 minutes/month for private repos
- Unlimited for public repos
- Each training run: ~2-3 minutes
- Easily supports hourly retraining

**Streamlit Cloud Free Tier:**
- 1 app
- Public repositories only
- Limited resources
- Perfect for this project

---

## 🚀 Advanced: Alternative Solutions

### Option 2: Google Sheets (Simpler)

If you prefer not to use Supabase:

```python
# Use gspread library
import gspread
from google.oauth2.service_account import Credentials

# Saves to Google Sheets instead
# Simpler but slower for large datasets
```

### Option 3: MongoDB Atlas

Similar to Supabase, different database type:

```python
# Use pymongo library
from pymongo import MongoClient

# Good for document-style data
```

---

## 📚 Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## ✅ Deployment Checklist

- [ ] Supabase account created
- [ ] Database table created
- [ ] API credentials copied
- [ ] `database.py` module added to project
- [ ] `app.py` updated to use database module
- [ ] `supabase` added to requirements.txt
- [ ] Code pushed to GitHub
- [ ] GitHub secrets added (SUPABASE_URL, SUPABASE_KEY)
- [ ] Streamlit app deployed
- [ ] Streamlit secrets configured
- [ ] GitHub Actions enabled
- [ ] Test submission made
- [ ] Data verified in Supabase
- [ ] Manual workflow run tested

---

## 🎉 You're Done!

Your app now has:
- ✅ Persistent data storage (Supabase)
- ✅ Automated hourly retraining (GitHub Actions)
- ✅ Cloud deployment (Streamlit Cloud)
- ✅ Scalable architecture

Users can submit data → It saves forever → Model improves automatically!
