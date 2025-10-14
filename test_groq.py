#!/usr/bin/env python3
"""
Quick test script for Groq AI integration
Run this to test if your Groq API key is working correctly.
"""

import os
import sys
from ai_recommender import get_ai_recommendations

def test_groq_integration():
    """Test Groq AI recommendations"""
    
    print("=" * 60)
    print("🧪 Testing Groq AI Integration")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv('GROQ_API_KEY') or os.getenv('AI_API_KEY')
    
    if not api_key:
        print("\n❌ No API key found!")
        print("\nPlease set your Groq API key:")
        print("  export GROQ_API_KEY='your_key_here'")
        print("\nOr add it to ai_config.json")
        print("\n💡 Get a free key at: https://console.groq.com")
        return False
    
    print(f"\n✅ API key found: {api_key[:10]}...{api_key[-5:]}")
    
    # Test with sample data
    print("\n📊 Test Profile:")
    print("  - Stress Level: 4 (High)")
    print("  - Sleep Quality: 2 (Poor)")
    print("  - Headaches: 4 per week")
    print("  - Academic Performance: 3")
    print("  - Study Load: 5 (Very Heavy)")
    print("  - Extracurricular: 2 per week")
    
    print("\n🤖 Generating AI recommendations...")
    print("-" * 60)
    
    try:
        recommendations = get_ai_recommendations(
            stress_level=4,
            sleep_quality=2,
            headaches_per_week=4,
            academic_performance=3,
            study_load=5,
            extracurricular_frequency=2
        )
        
        print("\n💡 Recommendations:\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}\n")
        
        print("-" * 60)
        print(f"✅ Success! Generated {len(recommendations)} recommendations")
        print("\n🎉 Groq AI is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔍 Troubleshooting:")
        print("  1. Check your API key is valid")
        print("  2. Ensure you have internet connection")
        print("  3. Check rate limits (10/min, 14,400/day)")
        print("  4. Review GROQ_SETUP.md for detailed help")
        return False

if __name__ == "__main__":
    success = test_groq_integration()
    sys.exit(0 if success else 1)
