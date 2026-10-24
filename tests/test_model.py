"""
Unit tests for Machine Learning Model and Feature Engineering
"""

import os
import joblib
import pandas as pd
import numpy as np
import pytest

from app import calculate_engineered_features, predict_stress

MODEL_PATH = "model/stress_predictor_model.joblib"

class TestModelPipeline:
    def test_model_artifact_exists(self):
        """Verify the serialized trained model artifact exists on disk"""
        assert os.path.exists(MODEL_PATH), f"Expected model file at {MODEL_PATH}"
        assert os.path.getsize(MODEL_PATH) > 1000, "Model artifact file is empty or corrupted"

    def test_model_can_be_loaded(self):
        """Verify the joblib model can be cleanly loaded and has predict capability"""
        model = joblib.load(MODEL_PATH)
        assert hasattr(model, "predict"), "Loaded artifact does not possess a predict() method"

    def test_engineered_features_calculation(self):
        """Test business logic for calculating derived student features"""
        sleep_quality = 4
        headaches_per_week = 2
        academic_performance = 5
        study_load = 3
        extracurricular_frequency = 4

        wb, ap, tw = calculate_engineered_features(
            sleep_quality,
            headaches_per_week,
            academic_performance,
            study_load,
            extracurricular_frequency
        )

        # Expected:
        # wellbeing_score = 4 - (2 / 2) = 3.0
        # academic_pressure = 3 * (6 - 5) = 3.0
        # total_workload = 3 + (4 / 2) = 5.0
        assert wb == 3.0
        assert ap == 3.0
        assert tw == 5.0

    def test_model_prediction_valid_input(self):
        """Test inference pipeline with a realistic feature dataframe"""
        model = joblib.load(MODEL_PATH)

        sleep_quality = 3
        headaches_per_week = 1
        academic_performance = 4
        study_load = 2
        extracurricular_frequency = 3

        wb, ap, tw = calculate_engineered_features(
            sleep_quality,
            headaches_per_week,
            academic_performance,
            study_load,
            extracurricular_frequency
        )

        features = pd.DataFrame([{
            'sleep_quality': sleep_quality,
            'headaches_per_week': headaches_per_week,
            'academic_performance': academic_performance,
            'study_load': study_load,
            'extracurricular_frequency': extracurricular_frequency,
            'wellbeing_score': wb,
            'academic_pressure': ap,
            'total_workload': tw
        }])

        prediction, confidence = predict_stress(model, features)

        assert prediction is not None, "Model failed to produce a prediction"
        assert isinstance(prediction, int), "Prediction must be an integer category"
        assert prediction in [0, 1, 2, 3, 4, 5], f"Unexpected prediction value: {prediction}"

        if confidence is not None:
            assert 0.0 <= confidence <= 100.0, f"Confidence {confidence} is out of 0-100% bounds"

    def test_model_prediction_extreme_stressed_profile(self):
        """Test high-stress profile yields high stress classification"""
        model = joblib.load(MODEL_PATH)

        # High workload, poor sleep, frequent headaches
        sleep_quality = 1
        headaches_per_week = 7
        academic_performance = 1
        study_load = 5
        extracurricular_frequency = 7

        wb, ap, tw = calculate_engineered_features(
            sleep_quality,
            headaches_per_week,
            academic_performance,
            study_load,
            extracurricular_frequency
        )

        features = pd.DataFrame([{
            'sleep_quality': sleep_quality,
            'headaches_per_week': headaches_per_week,
            'academic_performance': academic_performance,
            'study_load': study_load,
            'extracurricular_frequency': extracurricular_frequency,
            'wellbeing_score': wb,
            'academic_pressure': ap,
            'total_workload': tw
        }])

        prediction, _ = predict_stress(model, features)
        assert prediction is not None
        # Should classify as elevated stress level (>= 1)
        assert prediction >= 1, "Extreme stress profile was unexpectedly classified as low/zero stress"
