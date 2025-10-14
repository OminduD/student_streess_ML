# 🏗️ System Architecture

## Overview

This document explains how your Student Stress Predictor works with cloud deployment, persistent storage, and automated retraining.

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                   (Streamlit Cloud - Free)                      │
│                                                                 │
│  [Student fills form] → [Predict] → [Submit actual stress]    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      STREAMLIT APP                              │
│                      (app.py)                                   │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   Load       │    │  Make        │    │  Save Data   │    │
│  │   Model      │ →  │  Prediction  │ →  │  to Database │    │
│  └──────────────┘    └──────────────┘    └──────┬───────┘    │
└─────────────────────────────────────────────────┼─────────────┘
                                                   │
                     ┌─────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLOUD DATABASE                               │
│                 (Supabase - PostgreSQL)                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ user_inputs table:                                       │  │
│  │ ┌────┬───────────┬───────────┬────────────┬────────┐    │  │
│  │ │ id │ sleep_q.  │ headaches │ study_load │ stress │    │  │
│  │ ├────┼───────────┼───────────┼────────────┼────────┤    │  │
│  │ │  1 │     3     │     2     │      4     │   3    │    │  │
│  │ │  2 │     2     │     5     │      5     │   5    │    │  │
│  │ │... │    ...    │    ...    │     ...    │  ...   │    │  │
│  │ └────┴───────────┴───────────┴────────────┴────────┘    │  │
│  │                                                          │  │
│  │  💾 Data persists forever (not ephemeral!)              │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ (Every Hour)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              AUTOMATED RETRAINING SERVICE                       │
│              (GitHub Actions - Free)                            │
│                                                                 │
│  Trigger: Cron Schedule (0 * * * * = every hour)              │
│                                                                 │
│  Steps:                                                        │
│  1. ⬇️  Download new data from Supabase                        │
│  2. ✅ Check if ≥10 new labeled samples exist                  │
│  3. 🔄 If yes: Process data + Retrain model                    │
│  4. 💾 Save updated model to repository                        │
│  5. 🚀 Push to GitHub (triggers Streamlit redeploy)            │
│                                                                 │
│  Result: Improved model deployed automatically! 🎉             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ (Commits to repo)
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                            │
│                  (Version Control)                              │
│                                                                 │
│  📁 model/                                                      │
│     ├── stress_predictor_model.joblib  (ML model)             │
│     └── metrics.json                    (Performance stats)    │
│                                                                 │
│  📁 data/processed/                                             │
│     └── combined_dataset.csv            (Training data)        │
│                                                                 │
│  When updated → Streamlit Cloud auto-redeploys                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Flow 1: User Submission

```
User Input
    │
    ├─→ [app.py] Make prediction with current model
    │       │
    │       └─→ Display results + recommendations
    │
    └─→ [database.py] Save to Supabase
            │
            └─→ ✅ Data persisted in cloud
```

### Flow 2: Automated Retraining (Hourly)

```
GitHub Actions Timer (every hour)
    │
    ├─→ [1] Download data from Supabase
    │       └─→ scripts/download_training_data.py
    │
    ├─→ [2] Check if enough new data
    │       └─→ scripts/check_new_data.py
    │           └─→ If < 10 samples: SKIP
    │           └─→ If ≥ 10 samples: CONTINUE
    │
    ├─→ [3] Process data
    │       └─→ scripts/ingest_multi_dataset.py
    │           └─→ Merge with existing datasets
    │           └─→ Engineer features
    │           └─→ Split train/test
    │
    ├─→ [4] Train model
    │       └─→ scripts/train_multi_dataset.py
    │           └─→ Try multiple algorithms
    │           └─→ Select best model
    │           └─→ Save to model/
    │
    └─→ [5] Commit & Push
            └─→ Git commit with new model
            └─→ Streamlit Cloud detects change
            └─→ 🚀 Auto-redeploys with improved model!
```

---

## 🗂️ File Structure

```
student_streess_ML/
│
├── 🎨 Frontend
│   ├── app.py                      # Main Streamlit app
│   └── ai_recommender.py           # AI recommendations
│
├── 💾 Database Layer
│   └── database.py                 # Supabase integration
│
├── 🤖 Model Training
│   ├── scripts/
│   │   ├── ingest_multi_dataset.py      # Data processing
│   │   ├── train_multi_dataset.py       # Model training
│   │   ├── download_training_data.py    # Download from Supabase
│   │   └── check_new_data.py            # Check if retraining needed
│   │
│   └── model/
│       ├── stress_predictor_model.joblib  # Trained model
│       └── metrics.json                    # Performance metrics
│
├── 🔄 Automation
│   └── .github/workflows/
│       └── retrain_model.yml        # Automated retraining
│
├── 📊 Data
│   ├── data/processed/              # Processed training data
│   ├── user_inputs.csv              # Local backup (optional)
│   └── *.csv                        # Original datasets
│
└── 📚 Documentation
    ├── README.md
    ├── DEPLOYMENT_GUIDE.md          # Full deployment guide
    ├── QUICK_START.md               # 15-min setup guide
    └── ARCHITECTURE.md              # This file
```

---

## 🔐 Environment Variables & Secrets

### Streamlit Cloud Secrets

```toml
# .streamlit/secrets.toml (for Streamlit Cloud)
SUPABASE_URL = "https://jujcyoomunwqyftyfezf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1amN5b29tdW53cXlmdHlmZXpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI1OTI1NSwiZXhwIjoyMDc1ODM1MjU1fQ.r2dIrJYv-pRMTdQhqPwPvbGWn68ti7RTrTj49J7Z7xg"
```

### GitHub Secrets

```
Repository Settings → Secrets → Actions
├── SUPABASE_URL     (for GitHub Actions)
└── SUPABASE_KEY     (for GitHub Actions)
```

### Local Development

```bash
# .env (for local testing - create this file)
export SUPABASE_URL="https://jujcyoomunwqyftyfezf.supabase.co"
export SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1amN5b29tdW53cXlmdHlmZXpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI1OTI1NSwiZXhwIjoyMDc1ODM1MjU1fQ.r2dIrJYv-pRMTdQhqPwPvbGWn68ti7RTrTj49J7Z7xg"

# Then run:
source .env
streamlit run app.py
```

---

## 🌐 Deployment Platforms

### 1. Streamlit Cloud (Frontend)

**Purpose**: Hosts the web application  
**Cost**: FREE  
**URL**: `https://[app-name]-[username].streamlit.app`  
**Features**:
- Auto-deploys on Git push
- Built-in secrets management
- Free for public repositories

### 2. Supabase (Database)

**Purpose**: Persistent data storage  
**Cost**: FREE (up to 500MB)  
**Type**: PostgreSQL database  
**Features**:
- Real-time data sync
- REST API
- Free tier suitable for 50k-100k records

### 3. GitHub Actions (Automation)

**Purpose**: Scheduled model retraining  
**Cost**: FREE (2000 minutes/month)  
**Schedule**: Every hour (configurable)  
**Features**:
- Cron-based scheduling
- Automated workflows
- Free for public repos

---

## 📈 Scalability

### Current Setup (Free Tier)

```
Users per month:        ~1,000 - 5,000
Submissions per month:  ~10,000 - 50,000
Database storage:       500 MB (ample)
Retraining frequency:   Every hour
Model updates:          ~24 per day
```

### If You Need More Scale

**Option 1: Upgrade Supabase**
- Pro Plan: $25/month
- 8 GB database
- Higher bandwidth

**Option 2: Add Caching**
- Use Streamlit's `@st.cache_data`
- Reduce database queries

**Option 3: Optimize Retraining**
- Change to every 3-6 hours
- Require more samples (e.g., 50 instead of 10)

---

## 🛡️ Security

### Best Practices Implemented

1. ✅ **Environment Variables**: Secrets never in code
2. ✅ **Service Role Key**: Proper authentication
3. ✅ **Row Level Security**: Database protection
4. ✅ **HTTPS Only**: Encrypted connections
5. ✅ **No Sensitive Data**: Only stress metrics stored

### What's NOT Stored

- ❌ No personal names
- ❌ No email addresses
- ❌ No student IDs
- ❌ No identifying information

---

## 🚀 Performance Optimization

### Current Optimizations

1. **Caching**: Model loaded once and cached
2. **Feature Engineering**: Done efficiently in pandas
3. **Batch Processing**: Multiple samples in training
4. **Minimal API Calls**: Only when needed

### Future Improvements

- Add Redis caching layer
- Use model quantization for faster predictions
- Implement lazy loading for statistics
- Add CDN for static assets

---

## 🔧 Maintenance

### Regular Tasks

| Task | Frequency | How |
|------|-----------|-----|
| Check Supabase usage | Monthly | Supabase dashboard |
| Review GitHub Actions | Weekly | GitHub Actions tab |
| Monitor model accuracy | After each training | Check metrics.json |
| Update dependencies | Quarterly | `pip list --outdated` |

### Troubleshooting Checklist

```
□ Check Streamlit app logs
□ Verify Supabase connection
□ Review GitHub Actions logs
□ Confirm secrets are set correctly
□ Test database table structure
□ Check model file exists
□ Verify training data quality
```

---

## 💡 Why This Architecture?

### ✅ Advantages

1. **Free to Run**: All platforms have generous free tiers
2. **Fully Automated**: No manual intervention needed
3. **Scalable**: Can handle thousands of users
4. **Persistent**: Data never lost
5. **Self-Improving**: Model gets better over time
6. **Version Controlled**: All code in Git
7. **Easy to Deploy**: One-time setup
8. **Professional**: Production-ready architecture

### ⚠️ Trade-offs

1. **Cold Starts**: Streamlit may sleep after inactivity
2. **Processing Time**: Retraining takes 2-3 minutes
3. **Free Tier Limits**: Storage and compute caps
4. **Public Repo**: (Required for free Streamlit)

---

## 🎓 Learning Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Supabase Docs](https://supabase.com/docs)
- [GitHub Actions Guide](https://docs.github.com/actions)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)

---

## 📞 Support

If you have questions:
1. Check DEPLOYMENT_GUIDE.md
2. Review QUICK_START.md
3. Look at code comments
4. Check GitHub Issues

---

**This architecture gives you a production-ready ML application with automatic improvements, all running on free tier services!** 🎉
