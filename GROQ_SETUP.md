# 🚀 Groq AI Setup Guide

## Why Groq?

Groq provides **SUPER FAST** AI inference (10x faster than traditional APIs) with a **generous FREE tier**! Perfect for getting instant AI-powered stress management recommendations.

### ⚡ Key Benefits:
- **Lightning Fast**: Responses in milliseconds
- **Free Tier**: 14,400 requests/day (10/min)
- **High Quality**: Uses powerful models like Llama 3.1 70B
- **Easy Setup**: Just need an API key!

---

## 📋 Step-by-Step Setup

### 1️⃣ Get Your Free Groq API Key

1. Visit **[https://console.groq.com](https://console.groq.com)**
2. Sign up for a free account (GitHub or email)
3. Go to **API Keys** section
4. Click **"Create API Key"**
5. Copy your API key (starts with `gsk_...`)

### 2️⃣ Configure the App

You have **two options** to add your API key:

#### Option A: Environment Variable (Recommended)

**For Linux/Mac:**
```bash
# Temporary (for current session)
export GROQ_API_KEY="your_groq_api_key_here"

# Permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export GROQ_API_KEY="your_groq_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

**For Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
```

#### Option B: Configuration File

Edit `ai_config.json` and add your API key:

```json
{
    "enabled": true,
    "provider": "groq",
    "api_key": "your_groq_api_key_here",
    "model": "llama-3.1-70b-versatile",
    "max_tokens": 1000,
    "timeout": 30
}
```

### 3️⃣ Run the App

```bash
streamlit run app.py
```

---

## 🎯 Available Groq Models

Choose the best model for your needs in `ai_config.json`:

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `llama-3.1-8b-instant` | ⚡⚡⚡ Fastest | Good | Quick responses |
| `llama-3.1-70b-versatile` | ⚡⚡ Fast | ⭐⭐⭐ Excellent | **Recommended** - Best balance |
| `mixtral-8x7b-32768` | ⚡⚡ Fast | ⭐⭐ Great | Long context |

**Default**: `llama-3.1-70b-versatile` (best quality)

---

## 🔧 Troubleshooting

### "No API key found"
- Make sure you set `GROQ_API_KEY` environment variable OR added it to `ai_config.json`
- Restart the terminal/app after setting the environment variable

### "Rate limit exceeded"
- Free tier: 10 requests/minute, 14,400/day
- Wait 1 minute or upgrade to paid tier

### "Invalid API key"
- Check your API key in console.groq.com
- Make sure it starts with `gsk_`
- No extra spaces or quotes in the key

### Fallback Mode
If Groq is not configured, the app automatically uses **rule-based recommendations** - no AI needed!

---

## 💰 Pricing (as of 2024)

### Free Tier (Perfect for this app!)
- **14,400 requests per day**
- **10 requests per minute**
- Access to all models
- No credit card required

### Paid Tier (if you need more)
- $0.10 - $0.90 per million tokens
- Much cheaper than OpenAI!

---

## 🌟 Example Usage

```python
# In the app, once configured, you'll see:
# ⚡ Powered by Groq AI (Lightning Fast!)

# Recommendations will be generated using:
# - Model: llama-3.1-70b-versatile
# - Response time: < 1 second
# - Personalized based on your stress profile
```

---

## 🔄 Switching Providers

Want to use a different AI provider? Edit `ai_config.json`:

**OpenAI:**
```json
{
    "enabled": true,
    "provider": "openai",
    "api_key": "sk-...",
    "model": "gpt-3.5-turbo"
}
```

**Anthropic (Claude):**
```json
{
    "enabled": true,
    "provider": "anthropic",
    "api_key": "sk-ant-...",
    "model": "claude-3-sonnet-20240229"
}
```

**Disable AI (use rule-based):**
```json
{
    "enabled": false
}
```

---

## 📚 Resources

- **Groq Console**: https://console.groq.com
- **Groq Documentation**: https://console.groq.com/docs
- **API Playground**: https://console.groq.com/playground
- **Rate Limits**: https://console.groq.com/docs/rate-limits

---

## 🎉 You're All Set!

Once configured, your app will generate **personalized, AI-powered stress management recommendations** in milliseconds! 🚀

Try different stress profiles and see how Groq adapts its advice based on:
- Sleep quality
- Academic performance  
- Study load
- Stress levels
- And more!

---

**Need Help?** Check the troubleshooting section above or visit [Groq Community](https://console.groq.com/community)
