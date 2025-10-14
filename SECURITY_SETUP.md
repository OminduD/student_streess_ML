# 🔐 Quick Security Setup Guide

## ⚠️ IMPORTANT: Never Commit API Keys!

Before pushing to GitHub, make sure you've secured your API keys.

---

## 🚀 Quick Setup (3 Steps)

### 1. Get Your API Key
Visit [Groq Console](https://console.groq.com) and generate a free API key.

### 2. Set Up Locally

**Option A: Environment Variable (Recommended)**
```bash
export GROQ_API_KEY="your_api_key_here"
```

**Option B: Config File**
```bash
cp ai_config.json.template ai_config.json
# Edit ai_config.json and add your API key
```

### 3. Verify Security
```bash
# Make sure these files are in .gitignore
git check-ignore ai_config.json .env
# Should output: ai_config.json and .env
```

---

## 🚨 If GitHub Detects Your Key

1. **Revoke the key immediately** at https://console.groq.com
2. **Generate a new key**
3. **Follow instructions in** `SECURITY_FIX.md`

---

## ✅ What's Already Protected

- ✅ `.gitignore` includes `ai_config.json`
- ✅ `.gitignore` includes `.env`
- ✅ Template files provided without real keys
- ✅ Environment variable support built-in

---

## 📚 Full Details

See `SECURITY_FIX.md` for complete instructions on:
- Removing keys from Git history
- Setting up environment variables
- Best security practices
- Troubleshooting

**Stay secure! 🔒**
