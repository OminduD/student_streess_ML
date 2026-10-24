"""
Tests configuration and shared fixtures for student_streess_ML test suite.
"""

import os
import sys
import tempfile
import pytest
import pandas as pd

# Add repo root to python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_user_data():
    """Standard valid student submission payload"""
    return {
        "sleep_quality": 3,
        "headaches_per_week": 2,
        "academic_performance": 4,
        "study_load": 3,
        "extracurricular_frequency": 2,
        "actual_stress": 3
    }

@pytest.fixture
def temp_csv():
    """Provides an isolated temporary CSV file for testing DataStorage"""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
        temp_path = tf.name
    yield temp_path
    if os.path.exists(temp_path):
        os.remove(temp_path)

@pytest.fixture
def mock_model():
    """Mock ML classifier with predictable output for pipeline tests"""
    class MockEstimator:
        def __init__(self):
            self.classes_ = [0, 1, 2]
            self.feature_names_in_ = [
                "sleep_quality",
                "headaches_per_week",
                "academic_performance",
                "study_load",
                "extracurricular_frequency",
                "wellbeing_score",
                "academic_pressure",
                "total_workload"
            ]

        def predict(self, X):
            return [2]

        def predict_proba(self, X):
            return [[0.1, 0.2, 0.7]]

    return MockEstimator()
