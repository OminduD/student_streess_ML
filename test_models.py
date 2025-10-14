#!/usr/bin/env python3
"""
Simple Groq API Tester - Tests multiple models to find working one
"""

import requests
import json
import sys

# Load API key
try:
    with open('ai_config.json', 'r') as f:
        config = json.load(f)
    api_key = config.get('api_key')
except Exception as e:
    print(f"❌ Error loading config: {e}")
    sys.exit(1)

if not api_key:
    print("❌ No API key found in ai_config.json")
    sys.exit(1)

print("=" * 70)
print("🧪 Testing Groq API Models")
print("=" * 70)
print(f"\n🔑 API Key: {api_key[:15]}...{api_key[-10:]}\n")

# Models to test
models = [
    'llama-3.3-70b-versatile',
    'llama-3.1-70b-versatile',
    'llama-3.1-8b-instant',
    'mixtral-8x7b-32768',
    'gemma2-9b-it'
]

url = 'https://api.groq.com/openai/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

working_models = []

for model in models:
    print(f"Testing: {model}")
    
    data = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': 'Respond with exactly these 4 words: "API is working correctly"'
            }
        ],
        'max_tokens': 50,
        'temperature': 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            print(f"  ✅ SUCCESS!")
            print(f"  Response: {content}\n")
            working_models.append(model)
            
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"  ❌ Failed (400): {error_msg}\n")
            
        elif response.status_code == 401:
            print(f"  ❌ Failed (401): Invalid API key\n")
            break
            
        elif response.status_code == 429:
            print(f"  ❌ Rate limit exceeded. Wait a minute.\n")
            break
            
        else:
            print(f"  ❌ Failed ({response.status_code}): {response.text[:100]}\n")
            
    except requests.exceptions.Timeout:
        print(f"  ⏱️  Timeout (model might be loading)\n")
        
    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {e}\n")

print("=" * 70)

if working_models:
    print(f"\n✅ {len(working_models)} working model(s) found:")
    for model in working_models:
        print(f"   • {model}")
    
    print(f"\n💡 Recommended: Use '{working_models[0]}' in your ai_config.json")
    print(f"\n📝 Update your config:")
    print(f'   "model": "{working_models[0]}"')
    
else:
    print("\n❌ No working models found!")
    print("\n🔍 Troubleshooting:")
    print("   1. Check if your API key is valid at https://console.groq.com/keys")
    print("   2. Verify you have an active Groq account")
    print("   3. Check rate limits (10/min, 14,400/day free tier)")
    print("   4. Try again in a few minutes")
    print("\n💡 Meanwhile, app will use rule-based recommendations")

print("\n" + "=" * 70)
