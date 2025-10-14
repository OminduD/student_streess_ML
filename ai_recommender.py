"""
AI Recommendation Engine
==========================
Module for generating AI-powered stress management recommendations.
Supports multiple AI providers with fallback to rule-based recommendations.
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime


class AIRecommendationEngine:
    """
    AI-powered recommendation engine with multiple provider support.
    """
    
    def __init__(self, config_path: str = 'ai_config.json'):
        """
        Initialize the AI recommendation engine.
        
        Args:
            config_path: Path to AI configuration file
        """
        self.config = self._load_config(config_path)
        self.provider = self.config.get('provider', 'openai')
        # Support both AI_API_KEY and GROQ_API_KEY environment variables
        self.api_key = self.config.get('api_key') or os.getenv('GROQ_API_KEY') or os.getenv('AI_API_KEY')
        self.api_url = self.config.get('api_url', '')
        self.model = self.config.get('model', 'gpt-3.5-turbo')
        self.enabled = self.config.get('enabled', False)
        self.timeout = self.config.get('timeout', 10)
        self.max_tokens = self.config.get('max_tokens', 500)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file."""
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load AI config: {e}")
        return {}
    
    def generate_recommendations(
        self,
        stress_level: int,
        sleep_quality: int,
        headaches_per_week: int,
        academic_performance: int,
        study_load: int,
        extracurricular_frequency: int
    ) -> List[str]:
        """
        Generate personalized recommendations using AI.
        
        Args:
            stress_level: Predicted stress level (1-5)
            sleep_quality: Sleep quality rating (1-5)
            headaches_per_week: Number of headaches per week (0-7)
            academic_performance: Academic performance rating (1-5)
            study_load: Study load rating (1-5)
            extracurricular_frequency: Extracurricular activities frequency (1-7)
            
        Returns:
            List of personalized recommendations
        """
        # If AI is not enabled or configured, use rule-based fallback
        if not self.enabled:
            print("ℹ️  AI recommendations disabled in config. Using rule-based recommendations.")
            return self._fallback_recommendations(
                stress_level, sleep_quality, headaches_per_week, study_load
            )
        
        if not self.api_key:
            print("⚠️  No API key found. Set AI_API_KEY environment variable or add to config.")
            print("   Using rule-based recommendations as fallback.")
            return self._fallback_recommendations(
                stress_level, sleep_quality, headaches_per_week, study_load
            )
        
        try:
            # Generate AI recommendations based on provider
            if self.provider == 'openai':
                return self._get_openai_recommendations(
                    stress_level, sleep_quality, headaches_per_week,
                    academic_performance, study_load, extracurricular_frequency
                )
            elif self.provider == 'anthropic':
                return self._get_anthropic_recommendations(
                    stress_level, sleep_quality, headaches_per_week,
                    academic_performance, study_load, extracurricular_frequency
                )
            elif self.provider == 'groq':
                return self._get_groq_recommendations(
                    stress_level, sleep_quality, headaches_per_week,
                    academic_performance, study_load, extracurricular_frequency
                )
            elif self.provider == 'huggingface':
                return self._get_huggingface_recommendations(
                    stress_level, sleep_quality, headaches_per_week,
                    academic_performance, study_load, extracurricular_frequency
                )
            elif self.provider == 'custom':
                return self._get_custom_api_recommendations(
                    stress_level, sleep_quality, headaches_per_week,
                    academic_performance, study_load, extracurricular_frequency
                )
            else:
                print(f"⚠️  Unknown provider: {self.provider}")
                return self._fallback_recommendations(
                    stress_level, sleep_quality, headaches_per_week, study_load
                )
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            if "429" in error_msg:
                print("⚠️  Rate limit exceeded or quota exhausted. Check your API key and billing.")
            elif "401" in error_msg:
                print("⚠️  Invalid API key. Please check your credentials.")
            elif "403" in error_msg:
                print("⚠️  Access forbidden. Check API key permissions.")
            else:
                print(f"⚠️  API error: {e}")
            print("   Using rule-based recommendations as fallback.")
            return self._fallback_recommendations(
                stress_level, sleep_quality, headaches_per_week, study_load
            )
        except Exception as e:
            print(f"⚠️  Unexpected error: {type(e).__name__}: {e}")
            print("   Using rule-based recommendations as fallback.")
            return self._fallback_recommendations(
                stress_level, sleep_quality, headaches_per_week, study_load
            )
    
    def _create_prompt(
        self,
        stress_level: int,
        sleep_quality: int,
        headaches: int,
        academic_perf: int,
        study_load: int,
        extracurricular: int
    ) -> str:
        """Create a detailed prompt for the AI model."""
        
        stress_descriptions = {
            1: "very low stress",
            2: "low stress",
            3: "moderate stress",
            4: "high stress",
            5: "very high stress"
        }
        
        prompt = f"""You are a compassionate student wellness advisor. Based on the following student profile, provide 3-5 personalized, actionable recommendations to help reduce stress and improve wellbeing.

Student Profile:
- Stress Level: {stress_level}/5 ({stress_descriptions.get(stress_level, 'moderate')})
- Sleep Quality: {sleep_quality}/5 ({'poor' if sleep_quality <= 2 else 'moderate' if sleep_quality == 3 else 'good'})
- Headaches per Week: {headaches}
- Academic Performance: {academic_perf}/5
- Study Load: {study_load}/5 ({'light' if study_load <= 2 else 'moderate' if study_load == 3 else 'heavy'})
- Extracurricular Activities: {extracurricular}/7 days per week

Guidelines:
1. Provide specific, actionable advice (not generic platitudes)
2. Address the most critical issues first
3. Be empathetic and supportive
4. Include practical techniques and resources
5. Keep each recommendation to 1-2 sentences
6. Use emojis to make recommendations engaging
7. For high stress (4-5), prioritize professional help

Format each recommendation on a new line starting with an emoji."""

        return prompt
    
    def _get_openai_recommendations(
        self, stress_level, sleep_quality, headaches,
        academic_perf, study_load, extracurricular
    ) -> List[str]:
        """Get recommendations from OpenAI API."""
        
        url = self.api_url or "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful student wellness advisor specializing in stress management."
                },
                {
                    "role": "user",
                    "content": self._create_prompt(
                        stress_level, sleep_quality, headaches,
                        academic_perf, study_load, extracurricular
                    )
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Parse recommendations (split by lines, filter empty)
        recommendations = [
            line.strip() 
            for line in content.split('\n') 
            if line.strip() and len(line.strip()) > 10
        ]
        
        return recommendations[:5]  # Max 5 recommendations
    
    def _get_groq_recommendations(
        self, stress_level, sleep_quality, headaches,
        academic_perf, study_load, extracurricular
    ) -> List[str]:
        """
        Get recommendations from Groq API (SUPER FAST and FREE!).
        Groq provides incredibly fast inference with generous free tier.
        Sign up at: https://console.groq.com
        """
        
        url = self.api_url or "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Groq supports models like llama-3.1-70b-versatile (best quality)
        # or llama-3.1-8b-instant (fastest)
        model = self.model or "llama-3.1-70b-versatile"
        
        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an empathetic student wellness advisor specializing in stress management and mental health support. Provide practical, actionable advice."
                },
                {
                    "role": "user",
                    "content": self._create_prompt(
                        stress_level, sleep_quality, headaches,
                        academic_perf, study_load, extracurricular
                    )
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "stream": False
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Parse recommendations (split by lines, filter empty)
        recommendations = [
            line.strip() 
            for line in content.split('\n') 
            if line.strip() and len(line.strip()) > 10
        ]
        
        # Remove common prefixes
        recommendations = [
            rec.lstrip('0123456789.-) ') 
            for rec in recommendations
        ]
        
        return recommendations[:5]  # Max 5 recommendations
    
    def _get_anthropic_recommendations(
        self, stress_level, sleep_quality, headaches,
        academic_perf, study_load, extracurricular
    ) -> List[str]:
        """Get recommendations from Anthropic (Claude) API."""
        
        url = self.api_url or "https://api.anthropic.com/v1/messages"
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model or "claude-3-sonnet-20240229",
            "max_tokens": self.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": self._create_prompt(
                        stress_level, sleep_quality, headaches,
                        academic_perf, study_load, extracurricular
                    )
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
        response.raise_for_status()
        
        result = response.json()
        content = result['content'][0]['text']
        
        recommendations = [
            line.strip() 
            for line in content.split('\n') 
            if line.strip() and len(line.strip()) > 10
        ]
        
        return recommendations[:5]
    
    def _get_huggingface_recommendations(
        self, stress_level, sleep_quality, headaches,
        academic_perf, study_load, extracurricular
    ) -> List[str]:
        """Get recommendations from Hugging Face Inference API (FREE tier available!)."""
        
        # Default to a good open-source model if not specified
        model = self.model or "mistralai/Mistral-7B-Instruct-v0.2"
        
        # Hugging Face Inference API endpoint
        url = self.api_url or f"https://api-inference.huggingface.co/models/{model}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Create the prompt
        prompt = self._create_prompt(
            stress_level, sleep_quality, headaches,
            academic_perf, study_load, extracurricular
        )
        
        # Hugging Face expects different formats depending on the model
        # For instruction-tuned models, we format as a chat
        data = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": self.max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        # Hugging Face models can take time to load (cold start)
        # Increase timeout for first request
        timeout = max(self.timeout, 30)
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and 'generated_text' in result[0]:
                    content = result[0]['generated_text']
                else:
                    content = str(result[0])
            elif isinstance(result, dict):
                content = result.get('generated_text', str(result))
            else:
                content = str(result)
            
            # Parse recommendations
            recommendations = [
                line.strip() 
                for line in content.split('\n') 
                if line.strip() and len(line.strip()) > 10
            ]
            
            # Filter out common artifacts
            recommendations = [
                rec for rec in recommendations 
                if not rec.startswith(('```', 'Sure', 'Here are', 'I recommend'))
            ]
            
            return recommendations[:5] if recommendations else self._fallback_recommendations(
                stress_level, sleep_quality, headaches, study_load
            )
            
        except requests.exceptions.Timeout:
            print("⚠️  Hugging Face model is loading (cold start). This can take 20-30 seconds.")
            print("   Please try again in a moment, or use a different provider.")
            return self._fallback_recommendations(
                stress_level, sleep_quality, headaches, study_load
            )
        except requests.exceptions.HTTPError as e:
            if "503" in str(e):
                print("⚠️  Model is currently loading. Please wait 20-30 seconds and try again.")
            else:
                raise
            return self._fallback_recommendations(
                stress_level, sleep_quality, headaches, study_load
            )
    
    def _get_custom_api_recommendations(
        self, stress_level, sleep_quality, headaches,
        academic_perf, study_load, extracurricular
    ) -> List[str]:
        """Get recommendations from a custom API endpoint."""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Custom API payload format
        data = {
            "stress_level": stress_level,
            "sleep_quality": sleep_quality,
            "headaches_per_week": headaches,
            "academic_performance": academic_perf,
            "study_load": study_load,
            "extracurricular_frequency": extracurricular,
            "prompt": self._create_prompt(
                stress_level, sleep_quality, headaches,
                academic_perf, study_load, extracurricular
            )
        }
        
        # Add any custom headers from config
        custom_headers = self.config.get('custom_headers', {})
        headers.update(custom_headers)
        
        response = requests.post(
            self.api_url, 
            headers=headers, 
            json=data, 
            timeout=self.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        
        # Try to extract recommendations from various response formats
        if isinstance(result, list):
            return result[:5]
        elif isinstance(result, dict):
            recommendations = (
                result.get('recommendations') or
                result.get('advice') or
                result.get('suggestions') or
                result.get('response') or
                []
            )
            if isinstance(recommendations, str):
                recommendations = [
                    line.strip() 
                    for line in recommendations.split('\n') 
                    if line.strip() and len(line.strip()) > 10
                ]
            return recommendations[:5]
        
        return self._fallback_recommendations(
            stress_level, sleep_quality, headaches, study_load
        )
    
    def _fallback_recommendations(
        self,
        stress_level: int,
        sleep_quality: int,
        headaches: int,
        study_load: int
    ) -> List[str]:
        """
        Generate rule-based recommendations as fallback.
        Used when AI is disabled or encounters errors.
        """
        recommendations = []
        
        if stress_level >= 4:
            recommendations.append(
                "🆘 **Urgent**: Consider speaking with a counselor or mental health professional. "
                "Your stress level indicates you may need professional support."
            )
        
        if sleep_quality <= 2:
            recommendations.append(
                "😴 **Sleep Improvement**: Aim for 7-9 hours of quality sleep. "
                "Try maintaining a consistent sleep schedule and creating a relaxing bedtime routine."
            )
        
        if headaches >= 3:
            recommendations.append(
                "💊 **Health Check**: Frequent headaches may indicate stress or dehydration. "
                "Stay hydrated (8 glasses of water daily), take regular breaks from screens, and consider consulting a doctor."
            )
        
        if study_load >= 4:
            recommendations.append(
                "📚 **Workload Management**: Break large tasks into smaller, manageable chunks. "
                "Use the Pomodoro technique (25min work, 5min break) and prioritize tasks by importance."
            )
        
        if stress_level >= 3:
            recommendations.append(
                "🧘 **Stress Relief**: Practice daily stress-reduction techniques like meditation (try Headspace or Calm apps), "
                "deep breathing exercises, light exercise, or yoga for 15-20 minutes."
            )
            recommendations.append(
                "👥 **Social Support**: Stay connected with friends, family, or join student support groups. "
                "Talking about your concerns can significantly reduce stress."
            )
        
        if stress_level <= 2 and sleep_quality >= 4:
            recommendations.append(
                "✨ **Great Job!** You're managing stress well! "
                "Continue maintaining your healthy habits, balanced lifestyle, and positive routines."
            )
        
        if len(recommendations) == 0:
            recommendations.append(
                "💪 **Keep Going!** Your stress levels are manageable. "
                "Continue your current healthy practices and stay mindful of self-care."
            )
        
        return recommendations


# Convenience function for easy import
def get_ai_recommendations(
    stress_level: int,
    sleep_quality: int,
    headaches_per_week: int,
    academic_performance: int,
    study_load: int,
    extracurricular_frequency: int,
    config_path: str = 'ai_config.json'
) -> List[str]:
    """
    Get AI-powered recommendations for stress management.
    
    Returns:
        List of personalized recommendations
    """
    engine = AIRecommendationEngine(config_path)
    return engine.generate_recommendations(
        stress_level, sleep_quality, headaches_per_week,
        academic_performance, study_load, extracurricular_frequency
    )
