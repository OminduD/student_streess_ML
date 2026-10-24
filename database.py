"""
Database Module for Student Stress Predictor
Uses Supabase for persistent data storage in cloud deployment
"""

import os
from datetime import datetime
from typing import Optional, Dict, List
import pandas as pd
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    st = None
    HAS_STREAMLIT = False

def _notify(kind: str, msg: str):
    if st is not None:
        try:
            fn = getattr(st, kind, None)
            if fn:
                fn(msg)
                return
        except Exception:
            pass
    print(f"[{kind.upper()}] {msg}")

# Try to import supabase, but allow fallback to CSV
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except (ImportError, Exception):
    SUPABASE_AVAILABLE = False
    _notify("warning", "⚠️ Supabase library not available or incompatible. Using local CSV fallback.")

class DataStorage:
    """
    Handles data storage with cloud database (Supabase) or CSV fallback
    """
    
    def __init__(self, use_supabase: bool = True):
        """
        Initialize data storage
        
        Args:
            use_supabase: If True, attempt to use Supabase. Falls back to CSV if not available.
        """
        self.use_supabase = use_supabase and SUPABASE_AVAILABLE
        self.supabase_client: Optional[Client] = None
        self.csv_path = "user_inputs.csv"
        
        if self.use_supabase:
            self._init_supabase()
    
    def _init_supabase(self):
        """Initialize Supabase client"""
        try:
            # First, try to get from Streamlit secrets
            try:
                supabase_url = st.secrets["SUPABASE_URL"]
                supabase_key = st.secrets["SUPABASE_KEY"]
                print("✓ Loaded Supabase credentials from Streamlit secrets.")
            except Exception:
                # Fallback to environment variables
                print("ℹ️ Streamlit secrets not found. Falling back to environment variables.")
                # Load from local .env if available
                if os.path.exists(".env"):
                    try:
                        with open(".env", "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith("#") and "=" in line:
                                    k, v = line.split("=", 1)
                                    os.environ.setdefault(k.strip(), v.strip())
                    except Exception:
                        pass

                supabase_url = os.getenv("SUPABASE_URL")
                supabase_key = os.getenv("SUPABASE_KEY")

            if not supabase_url or not supabase_key:
                self.connection_status = "unconfigured"
                self.connection_error = "SUPABASE_URL or SUPABASE_KEY not set. Operating in local CSV storage mode."
                self.use_supabase = False
                return

            # Clean URL: ensure no trailing slash or /rest/v1
            supabase_url = supabase_url.strip().rstrip("/")
            if supabase_url.endswith("/rest/v1"):
                supabase_url = supabase_url[:-8].rstrip("/")
            
            self.supabase_client = create_client(supabase_url, supabase_key)
            self.connection_status = "connected"
            self.connection_error = None
            
        except Exception as e:
            self.connection_status = "offline"
            self.connection_error = f"Failed to connect to Supabase: {str(e)}"
            self.use_supabase = False
    
    def save_user_input(self, data: Dict, include_stress: bool = False) -> bool:
        """
        Save user input to database or CSV
        
        Args:
            data: Dictionary with user input data
            include_stress: Whether to include actual stress level
            
        Returns:
            True if successful, False otherwise
        """
        # Prepare record
        record = {
            'sleep_quality': data['sleep_quality'],
            'headaches_per_week': data['headaches_per_week'],
            'academic_performance': data['academic_performance'],
            'study_load': data['study_load'],
            'extracurricular_frequency': data['extracurricular_frequency'],
            'timestamp': datetime.now().isoformat(),
            'source': data.get('source', 'streamlit_app')
        }
        
        if include_stress and 'actual_stress' in data:
            record['stress_level'] = data['actual_stress']
        else:
            record['stress_level'] = None
        
        if self.use_supabase:
            success = self._save_to_supabase(record)
            if success:
                self.last_storage_medium = "supabase"
                return True
            # Fall back to CSV if Supabase failed
            csv_saved = self._save_to_csv(record)
            if csv_saved:
                self.last_storage_medium = "csv_fallback"
            return csv_saved
        else:
            saved = self._save_to_csv(record)
            if saved:
                self.last_storage_medium = "csv"
            return saved
    
    def _save_to_supabase(self, record: Dict) -> bool:
        """Save record to Supabase"""
        if not self.supabase_client:
            self.last_error = "Cannot save to Supabase: client is uninitialized."
            return False
        try:
            result = self.supabase_client.table('user_inputs').insert(record).execute()
            
            # Check for API errors in the result
            if hasattr(result, 'error') and result.error:
                self.last_error = f"Supabase API Error: {result.error.message}"
                return False

            self.last_error = None
            return True
        except Exception as e:
            self.last_error = f"Error saving to Supabase: {str(e)}"
            return False
    
    def _save_to_csv(self, record: Dict) -> bool:
        """Save record to CSV file"""
        try:
            df = pd.DataFrame([record])
            
            file_has_content = os.path.exists(self.csv_path) and os.path.getsize(self.csv_path) > 0
            if file_has_content:
                df.to_csv(self.csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(self.csv_path, mode='w', header=True, index=False)
            
            self.last_error = None
            return True
        except Exception as e:
            self.last_error = f"Error saving to CSV: {str(e)}"
            return False
    
    def get_all_data(self) -> Optional[pd.DataFrame]:
        """
        Retrieve all user input data
        
        Returns:
            DataFrame with all data, or None if error
        """
        if self.use_supabase and self.supabase_client:
            df = self._get_from_supabase()
            if df is not None:
                return df
        return self._get_from_csv()
    
    def _get_from_supabase(self) -> Optional[pd.DataFrame]:
        """Retrieve data from Supabase"""
        if not self.supabase_client:
            return None
        try:
            result = self.supabase_client.table('user_inputs').select("*").execute()
            
            if hasattr(result, 'error') and result.error:
                self.last_error = f"Supabase API Error (get_all_data): {result.error.message}"
                return None

            if result.data:
                return pd.DataFrame(result.data)
            else:
                return pd.DataFrame() # Return empty dataframe
                
        except Exception as e:
            self.last_error = f"Error retrieving from Supabase: {str(e)}"
            return None
    
    def _get_from_csv(self) -> Optional[pd.DataFrame]:
        """Retrieve data from CSV file"""
        try:
            if os.path.exists(self.csv_path):
                df = pd.read_csv(self.csv_path)
                df = df.dropna(subset=['sleep_quality'])
                return df
            else:
                return None
        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")
            return None
    
    def get_statistics(self) -> Dict:
        """Get statistics from stored data"""
        df = self.get_all_data()
        
        if df is None or df.empty:
            return {
                'total_submissions': 0,
                'avg_stress': None,
                'avg_sleep': None,
                'avg_headaches': None
            }
        
        stats = {
            'total_submissions': len(df),
            'avg_sleep': df['sleep_quality'].mean(),
            'avg_headaches': df['headaches_per_week'].mean(),
            'avg_study_load': df['study_load'].mean(),
            'avg_academic_performance': df['academic_performance'].mean(),
        }
        
        # Calculate avg stress if available
        if 'stress_level' in df.columns:
            valid_stress = pd.to_numeric(df['stress_level'], errors='coerce').dropna()
            if len(valid_stress) > 0:
                stats['avg_stress'] = valid_stress.mean()
            else:
                stats['avg_stress'] = None
        else:
            stats['avg_stress'] = None
        
        return stats
    
    def export_for_training(self, output_path: str = "training_data_export.csv") -> bool:
        """
        Export all data for model retraining
        
        Args:
            output_path: Path to save the exported data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df = self.get_all_data()
            
            if df is None or df.empty:
                print("⚠️ No data to export")
                return False
            
            # Filter to only rows with stress_level for training
            training_df = df[df['stress_level'].notna()].copy()
            
            if len(training_df) == 0:
                print("⚠️ No labeled data available for training")
                return False
            
            training_df.to_csv(output_path, index=False)
            print(f"✓ Exported {len(training_df)} records to {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return False


# Singleton instance for the DataStorage class
_storage_instance: Optional[DataStorage] = None

def get_storage() -> DataStorage:
    """
    Get or create the storage singleton instance.
    Using st.cache_resource ensures the connection is made only once when running in Streamlit.
    """
    global _storage_instance
    if _storage_instance is None:
        print("Creating new DataStorage instance.")
        _storage_instance = DataStorage()
    return _storage_instance

if HAS_STREAMLIT:
    get_storage = st.cache_resource(get_storage)


