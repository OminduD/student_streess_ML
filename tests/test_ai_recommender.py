"""
Unit tests for AI Recommendation Engine and Fallback Heuristics
"""

import pytest
from ai_recommender import AIRecommendationEngine, get_ai_recommendations

class TestAIRecommendations:
    def test_engine_initialization_defaults(self):
        """Test engine initializes cleanly even without an API key"""
        engine = AIRecommendationEngine()
        assert engine is not None
        assert hasattr(engine, "_fallback_recommendations")

    def test_fallback_recommendations_high_stress(self):
        """Test rule-based fallback flags urgent counselor support on high stress"""
        engine = AIRecommendationEngine()
        recs = engine._fallback_recommendations(
            stress_level=5,
            sleep_quality=3,
            headaches=1,
            study_load=3
        )
        assert len(recs) > 0
        assert any("counselor" in r.lower() or "mental health" in r.lower() for r in recs)

    def test_fallback_recommendations_poor_sleep(self):
        """Test rule-based fallback suggests sleep routine on low sleep rating"""
        engine = AIRecommendationEngine()
        recs = engine._fallback_recommendations(
            stress_level=2,
            sleep_quality=1,
            headaches=0,
            study_load=2
        )
        assert any("sleep" in r.lower() for r in recs)

    def test_fallback_recommendations_frequent_headaches(self):
        """Test rule-based fallback catches frequent headaches (>= 3 per week)"""
        engine = AIRecommendationEngine()
        recs = engine._fallback_recommendations(
            stress_level=2,
            sleep_quality=4,
            headaches=5,
            study_load=2
        )
        assert any("headache" in r.lower() or "hydrat" in r.lower() for r in recs)

    def test_fallback_recommendations_healthy_profile(self):
        """Test healthy profile receives positive reinforcement advice"""
        engine = AIRecommendationEngine()
        recs = engine._fallback_recommendations(
            stress_level=1,
            sleep_quality=5,
            headaches=0,
            study_load=2
        )
        assert len(recs) > 0
        assert any("maintain" in r.lower() or "doing well" in r.lower() or "routine" in r.lower() for r in recs)

    def test_get_ai_recommendations_returns_list(self):
        """Test public convenience function get_ai_recommendations always returns non-empty list of strings"""
        recs = get_ai_recommendations(
            stress_level=3,
            sleep_quality=3,
            headaches_per_week=2,
            academic_performance=4,
            study_load=3,
            extracurricular_frequency=2
        )
        assert isinstance(recs, list)
        assert len(recs) > 0
        assert all(isinstance(r, str) for r in recs)
