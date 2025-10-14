"""
Database Module for Student Stress Predictor
Uses Supabase for persistent data storage in cloud deployment
"""

import streamlit as st

# Try to import supabase, but allow fallback to CSV
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("⚠️ Supabase library not installed. `pip install supabase`. Using CSV fallback.")

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
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                st.error("❌ **Supabase Error**: `SUPABASE_URL` or `SUPABASE_KEY` not found in environment variables.")
                st.info("Please set them in your Streamlit Cloud secrets.")
                self.use_supabase = False
                return
            
            self.supabase_client = create_client(supabase_url, supabase_key)
            st.success("✅ Connected to Supabase database.")
            
        except Exception as e:
            st.error(f"❌ **Failed to connect to Supabase**: {e}")
            st.info("Using CSV as a fallback. Check your Supabase URL and Key.")
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
            'source': 'streamlit_app'
        }
        
        if include_stress and 'actual_stress' in data:
            record['stress_level'] = data['actual_stress']
        else:
            record['stress_level'] = None
        
        if self.use_supabase:
            return self._save_to_supabase(record)
        else:
            st.warning("Saving to local CSV file as a fallback.")
            return self._save_to_csv(record)
    
    def _save_to_supabase(self, record: Dict) -> bool:
        """Save record to Supabase"""
        try:
            result = self.supabase_client.table('user_inputs').insert(record).execute()
            
            # Check for API errors in the result
            if hasattr(result, 'error') and result.error:
                st.error(f"❌ **Supabase API Error**: {result.error.message}")
                return False

            st.success(f"✓ Data saved to Supabase successfully!")
            return True
        except Exception as e:
            st.error(f"❌ **Error saving to Supabase**: {e}")
            st.info("This could be due to incorrect RLS policies or table structure. Falling back to CSV.")
            return self._save_to_csv(record)
    
    def _save_to_csv(self, record: Dict) -> bool:
        """Save record to CSV file"""
        try:
            df = pd.DataFrame([record])
            
            if os.path.exists(self.csv_path):
                df.to_csv(self.csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(self.csv_path, mode='w', header=True, index=False)
            
            st.info(f"✓ Data saved to local CSV: {self.csv_path}")
            return True
        except Exception as e:
            st.error(f"❌ Error saving to CSV: {e}")
            return False
    
    def get_all_data(self) -> Optional[pd.DataFrame]:
        """
        Retrieve all user input data
        
        Returns:
            DataFrame with all data, or None if error
        """
        if self.use_supabase:
            return self._get_from_supabase()
        else:
            st.info("Loading data from local CSV file.")
            return self._get_from_csv()
    
    def _get_from_supabase(self) -> Optional[pd.DataFrame]:
        """Retrieve data from Supabase"""
        try:
            result = self.supabase_client.table('user_inputs').select("*").execute()
            
            if hasattr(result, 'error') and result.error:
                st.error(f"❌ **Supabase API Error (get_all_data)**: {result.error.message}")
                return None

            if result.data:
                df = pd.DataFrame(result.data)
                st.info(f"✓ Retrieved {len(df)} records from Supabase.")
                return df
            else:
                st.info("ℹ️ No data found in Supabase table 'user_inputs'.")
                return pd.DataFrame() # Return empty dataframe
                
        except Exception as e:
            st.error(f"❌ **Error retrieving from Supabase**: {e}")
            st.info("Falling back to CSV.")
            return self._get_from_csv()
    
    def _get_from_csv(self) -> Optional[pd.DataFrame]:
        """Retrieve data from CSV file"""
        try:
            if os.path.exists(self.csv_path):
                df = pd.read_csv(self.csv_path)
                df = df.dropna(subset=['sleep_quality'])
                st.info(f"✓ Retrieved {len(df)} records from CSV.")
                return df
            else:
                st.warning("ℹ️ No CSV file found.")
                return None
        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")
            return None
    
    def get_statistics(self) -> Dict:
        """Get statistics from stored data"""
        df = self.get_all_data()
        
        if df is None or len(df) == 0:
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
            
            if df is None or len(df) == 0:
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


# Singleton instance
_storage_instance: Optional[DataStorage] = None

@st.cache_resource
def get_storage() -> DataStorage:
    """Get or create the storage singleton instance"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = DataStorage()
    return _storage_instance

