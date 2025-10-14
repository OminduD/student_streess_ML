# ⚡ Quick Start Guide - Deploy in 15 Minutes

Follow these steps to get your app deployed with persistent storage and auto-retraining.

---

## 🎯 What You'll Get

- ✅ App deployed online (free)
- ✅ User data saved permanently in cloud database
- ✅ Model automatically retrained every hour
- ✅ No server management needed

---

## 📋 Prerequisites

- GitHub account
- 15 minutes of your time
- Your project pushed to GitHub

---

## 🚀 Step-by-Step Setup

### 1️⃣ Setup Supabase (5 minutes)

```bash
# 1. Go to https://supabase.com
# 2. Click "Start your project" → Sign up with GitHub
# 3. Create new project:
#    - Name: student-stress-predictor
#    - Password: [create strong password]
#    - Region: [closest to you]
# 4. Wait 2 minutes for project creation
```

**Create database table:**
- Go to SQL Editor
- Paste and run this:

```sql
CREATE TABLE user_inputs (
    id BIGSERIAL PRIMARY KEY,
    sleep_quality INTEGER NOT NULL,
    headaches_per_week INTEGER NOT NULL,
    academic_performance INTEGER NOT NULL,
    study_load INTEGER NOT NULL,
    extracurricular_frequency INTEGER NOT NULL,
    stress_level INTEGER,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    source TEXT DEFAULT 'streamlit_app'
);

ALTER TABLE user_inputs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable insert for anon" ON user_inputs
    FOR INSERT TO anon
    WITH CHECK (true);

CREATE POLICY "Enable select for anon" ON user_inputs
    FOR SELECT TO anon
    USING (true);
```

**Get your credentials:**
- Settings → API
- Copy: **Project URL** and **service_role key**

---

### 2️⃣ Update Your Code (3 minutes)

```bash
# Install new dependency
pip install supabase==2.0.3

# Update requirements.txt
echo "supabase==2.0.3" >> requirements.txt

# The database.py file is already created!
# The GitHub Actions workflow is already created!
```

**Update app.py** - Find and replace these functions:

```python
# REPLACE the save_to_csv function with:
from database import get_storage

def save_to_csv(data, include_stress=False):
    """Save user input to database"""
    storage = get_storage()
    return storage.save_user_input(data, include_stress)

# REPLACE the load_statistics function with:
def load_statistics():
    """Load statistics from database"""
    storage = get_storage()
    return storage.get_all_data()
```

---

### 3️⃣ Push to GitHub (2 minutes)

```bash
git add .
git commit -m "Add cloud database and auto-retraining"
git push origin master
```

---

### 4️⃣ Add GitHub Secrets (2 minutes)

1. Go to your GitHub repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Click "New repository secret"
4. Add two secrets:

| Name | Value |
|------|-------|
| `SUPABASE_URL` | `https://jujcyoomunwqyftyfezf.supabase.co` (your URL) |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1amN5b29tdW53cXlmdHlmZXpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI1OTI1NSwiZXhwIjoyMDc1ODM1MjU1fQ.r2dIrJYv-pRMTdQhqPwPvbGWn68ti7RTrTj49J7Z7xg` (your service_role key) |

---

### 5️⃣ Deploy to Streamlit Cloud (3 minutes)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repo: `student_streess_ML`
5. Main file: `app.py`
6. Click "Advanced settings" → "Secrets"
7. Add:

```toml
SUPABASE_URL = "https://jujcyoomunwqyftyfezf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1amN5b29tdW53cXlmdHlmZXpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI1OTI1NSwiZXhwIjoyMDc1ODM1MjU1fQ.r2dIrJYv-pRMTdQhqPwPvbGWn68ti7RTrTj49J7Z7xg"
```

8. Click "Deploy"
9. Wait 2-3 minutes

---

## 🎉 Done! Test Your App

### Test 1: Check Data Persistence

1. Open your deployed app
2. Submit a prediction with actual stress level
3. Go to Supabase → Table Editor → user_inputs
4. ✅ You should see your data!

### Test 2: Check Auto-Retraining

1. Go to your GitHub repo
2. **Actions** tab
3. Click "Automated Model Retraining"
4. Click "Run workflow" → "Run workflow"
5. Wait 2-3 minutes
6. ✅ Should complete successfully!

---

## 📊 How to Monitor

### Check if data is saving:
```
Supabase Dashboard → Table Editor → user_inputs
```

### Check retraining status:
```
GitHub → Actions → Recent workflow runs
```

### Check model performance:
```
Your repo → model/metrics.json
```

---

## 🔄 What Happens Automatically

**Every hour (or when manually triggered):**

```
1. GitHub Actions wakes up
2. Downloads new data from Supabase
3. Checks if ≥10 new labeled samples exist
4. If yes:
   - Processes data
   - Retrains model
   - Updates model/metrics.json
   - Commits to GitHub
   - Streamlit Cloud auto-redeploys
5. Your app now uses the improved model!
```

---

## 💡 Tips

1. **Test locally first:**
   ```bash
   export SUPABASE_URL="https://jujcyoomunwqyftyfezf.supabase.co"
   export SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1amN5b29tdW53cXlmdHlmZXpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI1OTI1NSwiZXhwIjoyMDc1ODM1MjU1fQ.r2dIrJYv-pRMTdQhqPwPvbGWn68ti7RTrTj49J7Z7xg"
   streamlit run app.py
   ```

2. **Change retraining frequency:**
   Edit `.github/workflows/retrain_model.yml`:
   ```yaml
   schedule:
     - cron: '0 */3 * * *'  # Every 3 hours
   ```

3. **View logs:**
   - Streamlit: Click "Manage app" → "Logs"
   - GitHub Actions: Actions tab → Click workflow run

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Data not saving | Check Supabase credentials in Streamlit secrets |
| GitHub Actions failing | Verify GitHub secrets are set correctly |
| Import error | Make sure `supabase==2.0.3` is in requirements.txt |
| Table not found | Run the SQL script in Supabase SQL Editor |

---

## 📚 Next Steps

- Read full [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for details
- Monitor your Supabase usage (free tier = 500MB)
- Check GitHub Actions minutes (free tier = 2000 min/month)
- Share your app URL! 🎉

---

**Your app is now production-ready with persistent storage and automatic improvements!** 🚀
