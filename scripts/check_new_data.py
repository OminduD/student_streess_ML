"""
Check if there's enough new data to warrant retraining
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

def check_new_data(MIN_LABELED_RECORDS = 5):
    """
    Check if there's enough new data for retraining
    
    Args:
        min_new_samples: Minimum number of new samples required
        
    Returns:
        True if should retrain, False otherwise
    """
    print("=" * 70)
    print("CHECKING FOR NEW TRAINING DATA")
    print("=" * 70)
    
    # Check if user_inputs.csv exists
    if not os.path.exists("user_inputs.csv"):
        print("⚠️ No user_inputs.csv found. Skipping training.")
        return False
    
    # Load data
    df = pd.read_csv("user_inputs.csv")
    
    # Filter to only labeled data (with stress_level)
    labeled_df = df[df['stress_level'].notna()]
    
    print(f"\nTotal records: {len(df)}")
    print(f"Labeled records: {len(labeled_df)}")
    
    if len(labeled_df) < MIN_LABELED_RECORDS:
        print(f"\n⚠️ Not enough labeled data ({len(labeled_df)} < {MIN_LABELED_RECORDS})")
        print("   Skipping training.")
        return False
    
    print(f"\n✓ Sufficient data found. Proceeding with training.")
    return True

if __name__ == "__main__":
    should_train = check_new_data()
    sys.exit(0 if should_train else 1)
