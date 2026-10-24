"""
Unit and Integration Tests for Database & DataStorage Module
"""

import os
import tempfile
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from database import DataStorage

class TestDataStorageCSV:
    def test_init_csv_storage(self, temp_csv):
        """Test initializing DataStorage in CSV mode"""
        storage = DataStorage(use_supabase=False)
        storage.csv_path = temp_csv
        assert storage.use_supabase is False
        assert storage.csv_path == temp_csv

    def test_save_user_input_without_stress(self, temp_csv, sample_user_data):
        """Test saving survey input when user does not report actual stress"""
        storage = DataStorage(use_supabase=False)
        storage.csv_path = temp_csv

        success = storage.save_user_input(sample_user_data, include_stress=False)
        assert success is True
        assert os.path.exists(temp_csv)

        df = pd.read_csv(temp_csv)
        assert len(df) == 1
        assert df.iloc[0]['sleep_quality'] == sample_user_data['sleep_quality']
        assert df.iloc[0]['headaches_per_week'] == sample_user_data['headaches_per_week']
        assert pd.isna(df.iloc[0]['stress_level'])

    def test_save_user_input_with_actual_stress(self, temp_csv, sample_user_data):
        """Test saving survey input with ground-truth stress level"""
        storage = DataStorage(use_supabase=False)
        storage.csv_path = temp_csv

        success = storage.save_user_input(sample_user_data, include_stress=True)
        assert success is True

        df = pd.read_csv(temp_csv)
        assert len(df) == 1
        assert df.iloc[0]['stress_level'] == sample_user_data['actual_stress']

    def test_get_statistics_calculation(self, temp_csv):
        """Test computation of average metrics across multiple records"""
        storage = DataStorage(use_supabase=False)
        storage.csv_path = temp_csv

        # Insert 2 distinct records
        rec1 = {
            "sleep_quality": 2,
            "headaches_per_week": 4,
            "academic_performance": 3,
            "study_load": 4,
            "extracurricular_frequency": 1,
            "actual_stress": 4
        }
        rec2 = {
            "sleep_quality": 4,
            "headaches_per_week": 0,
            "academic_performance": 5,
            "study_load": 2,
            "extracurricular_frequency": 3,
            "actual_stress": 2
        }

        storage.save_user_input(rec1, include_stress=True)
        storage.save_user_input(rec2, include_stress=True)

        stats = storage.get_statistics()
        assert stats['total_submissions'] == 2
        assert stats['avg_sleep'] == 3.0  # (2 + 4) / 2
        assert stats['avg_headaches'] == 2.0  # (4 + 0) / 2
        assert stats['avg_stress'] == 3.0  # (4 + 2) / 2
        assert stats['avg_study_load'] == 3.0  # (4 + 2) / 2

    def test_get_statistics_empty_dataset(self, temp_csv):
        """Test statistics return zeros when storage file does not exist"""
        storage = DataStorage(use_supabase=False)
        storage.csv_path = "non_existent_file_path.csv"

        stats = storage.get_statistics()
        assert stats['total_submissions'] == 0
        assert stats['avg_stress'] is None
        assert stats['avg_sleep'] is None

    def test_export_for_training(self, temp_csv, sample_user_data):
        """Test exporting stored inputs for retraining only includes rows with stress labels"""
        storage = DataStorage(use_supabase=False)
        storage.csv_path = temp_csv

        # Row 1: with label
        storage.save_user_input(sample_user_data, include_stress=True)
        # Row 2: without label
        storage.save_user_input(sample_user_data, include_stress=False)

        export_target = temp_csv + "_export.csv"
        try:
            success = storage.export_for_training(export_target)
            assert success is True
            assert os.path.exists(export_target)

            exported_df = pd.read_csv(export_target)
            assert len(exported_df) == 1
            assert exported_df.iloc[0]['stress_level'] == sample_user_data['actual_stress']
        finally:
            if os.path.exists(export_target):
                os.remove(export_target)


class TestDataStorageSupabaseMocked:
    def test_save_to_supabase_success(self):
        """Test Supabase insert when API returns success"""
        storage = DataStorage(use_supabase=False)
        storage.use_supabase = True

        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_insert = MagicMock()
        mock_result = MagicMock()

        mock_result.error = None
        mock_result.data = [{"id": "uuid-123"}]
        mock_insert.execute.return_value = mock_result
        mock_table.insert.return_value = mock_insert
        mock_client.table.return_value = mock_table

        storage.supabase_client = mock_client

        record = {
            'sleep_quality': 4,
            'headaches_per_week': 1,
            'academic_performance': 4,
            'study_load': 3,
            'extracurricular_frequency': 2,
            'timestamp': "2026-10-24T12:00:00",
            'source': 'test'
        }

        result = storage._save_to_supabase(record)
        assert result is True
        mock_client.table.assert_called_with('user_inputs')
        mock_table.insert.assert_called_with(record)

    def test_get_from_supabase_returns_dataframe(self):
        """Test Supabase select converts records to pandas DataFrame"""
        storage = DataStorage(use_supabase=False)
        storage.use_supabase = True

        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_select = MagicMock()
        mock_result = MagicMock()

        mock_result.error = None
        mock_result.data = [
            {"sleep_quality": 3, "headaches_per_week": 1, "stress_level": 2},
            {"sleep_quality": 4, "headaches_per_week": 2, "stress_level": 3}
        ]
        mock_select.execute.return_value = mock_result
        mock_table.select.return_value = mock_select
        mock_client.table.return_value = mock_table

        storage.supabase_client = mock_client

        df = storage._get_from_supabase()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert df.iloc[0]['sleep_quality'] == 3
