# 🔧 Groq AI Connection Fix Guide

## ❓ Understanding Groq Models

**Important**: When you sign up at Groq, you only get an **API key**. They don't show model names because the models are standardized!

### ✅ Available Groq Models (as of October 2024)

Groq provides these models through their API:

| Model Name | Speed | Quality | Context | Best For |
|------------|-------|---------|---------|----------|
| `llama-3.3-70b-versatile` | ⚡⚡ Fast | ⭐⭐⭐ Best | 128K | **Recommended!** Latest & best |
| `llama-3.1-70b-versatile` | ⚡⚡ Fast | ⭐⭐⭐ Excellent | 128K | High quality |
| `llama-3.1-8b-instant` | ⚡⚡⚡ Fastest | ⭐⭐ Good | 128K | Quick responses |
| `mixtral-8x7b-32768` | ⚡⚡ Fast | ⭐⭐ Good | 32K | Long context |
| `gemma2-9b-it` | ⚡⚡ Fast | ⭐⭐ Good | 8K | Google's model |

**Note**: Model names may change. Groq recently upgraded from Llama 3.1 to Llama 3.3!

---

## 🔧 Fix Your Configuration

### Option 1: Try Latest Model (Recommended)

Edit your `ai_config.json`:

```json
{
    "enabled": true,
    "provider": "groq",
    "api_key": "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",
    "model": "llama-3.3-70b-versatile",
    "max_tokens": 1000,
    "timeout": 30
}
```

### Option 2: Use Faster Model

If you want faster responses:

```json
{
    "enabled": true,
    "provider": "groq",
    "api_key": "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",
    "model": "llama-3.1-8b-instant",
    "max_tokens": 1000,
    "timeout": 30
}
```

### Option 3: Try Different Model

```json
{
    "enabled": true,
    "provider": "groq",
    "api_key": "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",
    "model": "mixtral-8x7b-32768",
    "max_tokens": 1000,
    "timeout": 30
}
```

---

## 🧪 Test Each Model

Run this command to test all models:

```bash
python3 << 'EOF'
import requests
import json

with open('ai_config.json') as f:
    config = json.load(f)
api_key = config['api_key']

models_to_test = [
    'llama-3.3-70b-versatile',
    'llama-3.1-70b-versatile',
    'llama-3.1-8b-instant',
    'mixtral-8x7b-32768',
    'gemma2-9b-it'
]

print("Testing Groq Models...")
print("=" * 60)

for model in models_to_test:
    print(f"\nTesting: {model}")
    
    url = 'https://api.groq.com/openai/v1/chat/completions'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': 'Say hello in 3 words'}],
        'max_tokens': 20
    }
    
    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        if r.status_code == 200:
            result = r.json()['choices'][0]['message']['content']
            print(f"  ✅ SUCCESS: {result}")
        else:
            print(f"  ❌ Failed: {r.status_code}")
            if r.status_code == 400:
                print(f"     Error: {r.json().get('error', {}).get('message', 'Unknown')}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 60)
EOF
```

---

## 🔍 Common Issues & Solutions

### Issue 1: "400 Bad Request"

**Cause**: Model name might be outdated or wrong

**Solution**: 
1. Try `llama-3.3-70b-versatile` (latest)
2. If that fails, try `llama-3.1-8b-instant`
3. Run the test script above to find working models

### Issue 2: "401 Unauthorized"

**Cause**: Invalid API key

**Solution**:
1. Go to https://console.groq.com/keys
2. Check if your key is still active
3. Create a new key if needed
4. Update `api_config.json`

### Issue 3: "429 Rate Limit"

**Cause**: Too many requests

**Solution**:
- Free tier: 10 requests/minute, 14,400/day
- Wait 1 minute and try again
- Or upgrade your account

### Issue 4: "Model not found"

**Cause**: Model name changed or deprecated

**Solution**:
1. Check Groq's documentation: https://console.groq.com/docs/models
2. Use the test script above to find current models
3. Update your config with working model name

---

## 📝 Quick Fix Steps

1. **Update model name** in `ai_config.json` to `llama-3.3-70b-versatile`

2. **Test it**:
   ```bash
   python test_groq.py
   ```

3. **If still failing**, try each model:
   - `llama-3.3-70b-versatile`
   - `llama-3.1-8b-instant`
   - `mixtral-8x7b-32768`

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Where to Find Model Information

**Groq doesn't show models in the dashboard!** They only give you API keys.

To see available models:

1. **Official Documentation**: https://console.groq.com/docs/models
2. **API Endpoint**: GET `https://api.groq.com/openai/v1/models`
3. **Use the test script** in this guide

---

## 💡 Pro Tips

1. **Use `llama-3.3-70b-versatile`** - It's the latest and best!
2. **Use `llama-3.1-8b-instant`** - For fastest responses
3. **Check for updates** - Groq frequently adds new models
4. **Read docs** - https://console.groq.com/docs/models

---

## ✅ Recommended Configuration

Based on current Groq API (October 2024):

```json
{
    "enabled": true,
    "provider": "groq",
    "api_key": "your_api_key_here",
    "model": "llama-3.3-70b-versatile",
    "max_tokens": 1000,
    "timeout": 30
}
```

---

## 🆘 Still Not Working?

1. **Verify API key** is correct at https://console.groq.com/keys
2. **Check rate limits** - wait a few minutes
3. **Try different model** from the list above
4. **Disable AI temporarily**:
   ```json
   {
       "enabled": false
   }
   ```
   App will use rule-based recommendations

5. **Contact Groq Support**: https://console.groq.com/community

---

**Good luck!** 🚀
