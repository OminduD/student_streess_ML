#!/usr/bin/env python3
"""
Detailed Groq API Test - Find Available Models and Test Connection
"""

import os
import requests
import json

def test_groq_connection():
    """Test Groq API with detailed error messages"""
    
    print("=" * 70)
    print("🧪 Groq API Detailed Test")
    print("=" * 70)
    
    # Load config
    with open('ai_config.json', 'r') as f:
        config = json.load(f)
    
    api_key = config.get('api_key') or os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("\n❌ No API key found!")
        return False
    
    print(f"\n✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    
    # Test 1: List available models
    print("\n" + "─" * 70)
    print("📋 Step 1: Fetching Available Models from Groq")
    print("─" * 70)
    
    try:
        models_url = "https://api.groq.com/openai/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(models_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get('data', [])
            
            print(f"\n✅ Found {len(models)} available models:\n")
            
            for i, model in enumerate(models, 1):
                model_id = model.get('id', 'unknown')
                print(f"  {i}. {model_id}")
            
            # Recommended models
            print("\n💡 Recommended Models:")
            recommended = [
                'llama-3.3-70b-versatile',
                'llama-3.1-70b-versatile', 
                'llama-3.1-8b-instant',
                'mixtral-8x7b-32768',
                'gemma2-9b-it'
            ]
            
            available_recommended = [m for m in recommended if any(m in model.get('id', '') for model in models)]
            
            for model in available_recommended:
                print(f"  ⭐ {model}")
            
        else:
            print(f"\n⚠️  Could not fetch models: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n⚠️  Error fetching models: {e}")
    
    # Test 2: Test different model names
    print("\n" + "─" * 70)
    print("🧪 Step 2: Testing AI Completion")
    print("─" * 70)
    
    test_models = [
        'llama-3.3-70b-versatile',
        'llama-3.1-70b-versatile',
        'llama-3.1-8b-instant',
        'mixtral-8x7b-32768'
    ]
    
    for model_name in test_models:
        print(f"\n🔍 Testing model: {model_name}")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        data = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": "Say 'Hello, I am working!' in exactly 5 words."
                }
            ],
            "max_tokens": 50,
            "temperature": 0.5
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"  ✅ SUCCESS! Response: {content}")
                print(f"\n🎉 Working model found: {model_name}")
                print(f"\n💡 Update your ai_config.json to use: \"{model_name}\"")
                return True
                
            else:
                print(f"  ❌ Failed: {response.status_code}")
                if response.status_code == 400:
                    error_data = response.json()
                    print(f"  Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
                    
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "─" * 70)
    print("❌ No working model found")
    print("─" * 70)
    
    return False

if __name__ == "__main__":
    test_groq_connection()
