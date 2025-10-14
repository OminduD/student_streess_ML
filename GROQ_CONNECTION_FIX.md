# 🔧 GROQ AI NOT CONNECTING - COMPLETE FIX GUIDE

## 🎯 Quick Answer

**Groq doesn't show model names in their dashboard!** You only get an API key.

The models are **not visible** in the Groq console - you need to know their names!

---

## ✅ SOLUTION: Update Your Model Name

Your current config has an **old model name** that may not work. Try the latest:

### Step 1: Edit `ai_config.json`

Change this line:
```json
"model": "llama-3.1-70b-versatile"
```

To this (latest model):
```json
"model": "llama-3.3-70b-versatile"
```

Or this (fastest model):
```json
"model": "llama-3.1-8b-instant"
```

---

## 📋 ALL AVAILABLE GROQ MODELS (October 2024)

Here are the **exact model names** to use:

### ⭐ Recommended Models

1. **`llama-3.3-70b-versatile`** ← **USE THIS!** (Latest & Best)
   - Quality: ⭐⭐⭐⭐⭐
   - Speed: ⚡⚡ Fast
   - Released: October 2024

2. **`llama-3.1-8b-instant`** ← Fast option
   - Quality: ⭐⭐⭐⭐
   - Speed: ⚡⚡⚡ Super Fast
   - Best for: Quick responses

3. **`mixtral-8x7b-32768`** ← Alternative
   - Quality: ⭐⭐⭐⭐
   - Speed: ⚡⚡ Fast
   - Context: 32K tokens

### 🗂️ Complete List

```
llama-3.3-70b-versatile          ← NEWEST! Try this first
llama-3.1-70b-versatile          ← Older version
llama-3.1-8b-instant             ← Fastest
llama3-groq-70b-8192-tool-use-preview
llama3-groq-8b-8192-tool-use-preview
mixtral-8x7b-32768
gemma2-9b-it
gemma-7b-it
```

---

## 🔧 YOUR UPDATED CONFIG

Copy this **exact configuration**:

```json
{
    "enabled": true,
    "provider": "groq",
    "api_key": "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",
    "model": "llama-3.3-70b-versatile",
    "max_tokens": 1000,
    "timeout": 30,

    "_comment_enabled": "Set to true to enable AI recommendations",
    "_comment_provider": "Using Groq AI",
    "_comment_model": "Latest Llama 3.3 model (October 2024)"
}
```

---

## 🧪 TEST YOUR CONNECTION

### Method 1: Use Test Script

```bash
python3 test_models.py
```

This will test all models and tell you which ones work!

### Method 2: Quick Python Test

```bash
python3 << 'END'
import requests, json

with open('ai_config.json') as f:
    config = json.load(f)

api_key = config['api_key']
model = config['model']

print(f"Testing: {model}")

r = requests.post(
    'https://api.groq.com/openai/v1/chat/completions',
    headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
    json={
        'model': model,
        'messages': [{'role': 'user', 'content': 'Say hello in 3 words'}],
        'max_tokens': 20
    }
)

if r.status_code == 200:
    print("✅ SUCCESS!")
    print(f"Response: {r.json()['choices'][0]['message']['content']}")
else:
    print(f"❌ Failed: {r.status_code}")
    print(f"Error: {r.text}")
END
```

### Method 3: Run Your App

```bash
streamlit run app.py
```

Then try making a prediction and see if AI recommendations appear!

---

## ❓ WHY DON'T I SEE MODELS IN GROQ DASHBOARD?

**This is NORMAL!** Groq's website only shows:
- ✅ Your API keys
- ✅ Usage statistics
- ✅ Documentation

They **don't** show a dropdown of available models.

### Where to Find Model Names:

1. **Groq Documentation**: https://console.groq.com/docs/models
2. **This guide** (you're reading it!)
3. **Use the test script**: `python3 test_models.py`

---

## 🔍 COMMON ERROR MESSAGES

### Error: "400 Bad Request"
**Cause**: Wrong model name

**Fix**: 
```json
"model": "llama-3.3-70b-versatile"
```

### Error: "Model not found"
**Cause**: Model name is misspelled or deprecated

**Fix**: Use exact name from list above (copy-paste!)

### Error: "401 Unauthorized"
**Cause**: Invalid API key

**Fix**: 
1. Go to https://console.groq.com/keys
2. Check your key is active
3. Create new key if needed

### Error: "429 Too Many Requests"
**Cause**: Rate limit exceeded

**Fix**: 
- Free tier: 10 requests/minute
- Wait 60 seconds and try again

---

## 📝 STEP-BY-STEP FIX

1. **Open** `ai_config.json` in your editor

2. **Find** this line:
   ```json
   "model": "llama-3.1-70b-versatile",
   ```

3. **Change** it to:
   ```json
   "model": "llama-3.3-70b-versatile",
   ```

4. **Save** the file

5. **Test** it:
   ```bash
   python3 test_models.py
   ```

6. **Run** your app:
   ```bash
   streamlit run app.py
   ```

7. **Try** making a prediction with high stress values

8. **Look for**: "⚡ Powered by Groq AI" badge and personalized recommendations

---

## 💡 ALTERNATIVE MODELS TO TRY

If `llama-3.3-70b-versatile` doesn't work, try these **in order**:

1. `llama-3.1-8b-instant` (fastest)
2. `mixtral-8x7b-32768` (good quality)
3. `llama-3.1-70b-versatile` (older but stable)
4. `gemma2-9b-it` (Google's model)

Just change the `"model"` line in your config!

---

## 🎯 EXPECTED RESULT

When working correctly, you'll see:

```
💡 AI-Powered Recommendations
⚡ Powered by Groq AI (Lightning Fast!)

╔═══════════════════════════════════════╗
║ #1                                     ║
║ 🆘 Given your high stress level...    ║
║ [Detailed personalized advice]        ║
╚═══════════════════════════════════════╝
```

Instead of generic rule-based advice, you'll get:
- ✅ Personalized recommendations
- ✅ Specific numbers and techniques
- ✅ Detailed action steps
- ✅ Context-aware advice

---

## 🆘 STILL NOT WORKING?

### Option 1: Disable AI (Temporary)
```json
{
    "enabled": false
}
```
App will work with rule-based recommendations!

### Option 2: Check API Key
```bash
# Visit Groq console
open https://console.groq.com/keys

# Verify your key is:
# - Active (green status)
# - Not expired
# - Has remaining quota
```

### Option 3: Try Different Provider
Use OpenAI instead:
```json
{
    "enabled": true,
    "provider": "openai",
    "api_key": "sk-...",
    "model": "gpt-3.5-turbo"
}
```

---

## ✅ RECOMMENDED FINAL CONFIG

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

Save this, restart your app, and it should work! 🎉

---

## 📚 Additional Resources

- **Groq Models Docs**: https://console.groq.com/docs/models
- **API Reference**: https://console.groq.com/docs/api-reference
- **Rate Limits**: https://console.groq.com/docs/rate-limits
- **Community**: https://console.groq.com/community

---

**Need more help?** Check `GROQ_FIX.md` for detailed troubleshooting!

**Good luck!** 🚀
