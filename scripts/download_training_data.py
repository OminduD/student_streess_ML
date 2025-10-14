"""
Download training data from Supabase for model retraining
Run by GitHub Actions or manually
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_storage

def download_data():
    """Download data from Supabase and save for training"""
    print("=" * 70)
    print("DOWNLOADING TRAINING DATA FROM SUPABASE")
    print("=" * 70)
    
    storage = get_storage()
    
    # Export data for training
    success = storage.export_for_training("user_inputs.csv")
    
    if success:
        print("\n✓ Data downloaded successfully!")
        return True
    else:
        print("\n⚠️ No new data to download or error occurred")
        return False

if __name__ == "__main__":
    success = download_data()
    sys.exit(0 if success else 1)
