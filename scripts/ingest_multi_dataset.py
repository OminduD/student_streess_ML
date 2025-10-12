import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

def load_student_stress_factors(filepath):
    """Load and process Student Stress Factors (2).csv"""
    print("\n[1/3] Loading Student Stress Factors dataset...")
    df = pd.read_csv(filepath)
    
    # Rename columns for easier handling
    column_mapping = {
        'Kindly Rate your Sleep Quality 😴': 'sleep_quality',
        'How many times a week do you suffer headaches 🤕?': 'headaches_per_week',
        'How would you rate you academic performance 👩‍🎓?': 'academic_performance',
        'how would you rate your study load?': 'study_load',
        'How many times a week you practice extracurricular activities 🎾?': 'extracurricular_frequency',
        'How would you rate your stress levels?': 'stress_level'
    }
    df.rename(columns=column_mapping, inplace=True)
    
    # Invert sleep quality so that a higher value means better sleep
    # The original scale was likely 1=Good, 5=Bad. We want 5=Good, 1=Bad.
    if 'sleep_quality' in df.columns:
        df['sleep_quality'] = 6 - df['sleep_quality']
    
    # Add dataset source identifier
    df['dataset_source'] = 'student_factors'
    
    print(f"✓ Loaded {len(df)} samples with {len(df.columns)} features")
    return df

def load_stress_level_dataset(filepath):
    """Load and process StressLevelDataset.csv"""
    print("\n[2/3] Loading Stress Level dataset...")
    df = pd.read_csv(filepath)
    
    print(f"Original shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Map to our standard features
    # This dataset likely has different structure - we'll need to map it
    df['dataset_source'] = 'stress_level'
    
    print(f"✓ Loaded {len(df)} samples")
    return df

def load_stress_dataset(filepath):
    """Load and process Stress_Dataset.csv"""
    print("\n[3/3] Loading comprehensive Stress dataset...")
    df = pd.read_csv(filepath)
    
    print(f"Original shape: {df.shape}")
    print(f"Columns: {len(df.columns)} features")
    
    # This dataset has many features - we'll extract relevant ones
    # The target is the last column which contains stress type descriptions
    
    # Extract stress type from the last column
    target_col = df.columns[-1]
    
    # Map stress types to numeric levels (1-5)
    stress_mapping = {
        'No Stress - Currently experiencing minimal to no stress.': 1,
        'Eustress (Positive Stress) - Stress that motivates and enhances performance.': 2,
        'Distress (Negative Stress) - Stress that causes anxiety and impairs well-being.': 4
    }
    
    df['stress_level'] = df[target_col].map(stress_mapping)
    
    # Select relevant features that might correlate with our original dataset
    # We'll create composite scores from the survey questions
    
    # Sleep-related: questions about sleep problems
    sleep_cols = [col for col in df.columns if 'sleep' in col.lower()]
    if sleep_cols:
        df['sleep_quality'] = 6 - df[sleep_cols].mean(axis=1)  # Invert so higher = better
    
    # Health issues: headaches, illness
    health_cols = [col for col in df.columns if 'headache' in col.lower() or 'illness' in col.lower()]
    if health_cols:
        df['headaches_per_week'] = df[health_cols].mean(axis=1) * 2
    
    # Academic: performance, workload, concentration
    academic_cols = [col for col in df.columns if 'academic' in col.lower() or 'concentration' in col.lower()]
    if academic_cols:
        df['academic_performance'] = 6 - df[academic_cols].mean(axis=1)  # Invert
        df['study_load'] = df[academic_cols].mean(axis=1)
    
    # Activities: attending classes, extracurricular
    activity_cols = [col for col in df.columns if 'classes' in col.lower() or 'extracurricular' in col.lower() or 'leisure' in col.lower()]
    if activity_cols:
        df['extracurricular_frequency'] = df[activity_cols].mean(axis=1) * 2
    
    df['dataset_source'] = 'comprehensive_stress'
    
    # Select only the mapped columns
    mapped_cols = ['sleep_quality', 'headaches_per_week', 'academic_performance', 
                   'study_load', 'extracurricular_frequency', 'stress_level', 'dataset_source']
    
    # Keep only rows where stress_level is not null
    df = df[mapped_cols].dropna(subset=['stress_level'])
    
    print(f"✓ Loaded and mapped {len(df)} samples")
    return df

def load_user_contributed_data(filepath):
    """Load and process user-contributed data from frontend"""
    print("\n[4/4] Loading User-Contributed dataset...")
    
    if not os.path.exists(filepath):
        print("⚠ No user-contributed data found yet (this is normal for first run)")
        return pd.DataFrame()
    
    df = pd.read_csv(filepath)
    
    if len(df) == 0:
        print("⚠ User-contributed file is empty")
        return pd.DataFrame()
    
    # Keep only the core columns needed for training
    required_cols = ['sleep_quality', 'headaches_per_week', 'academic_performance',
                     'study_load', 'extracurricular_frequency', 'stress_level']
    
    # Check if all required columns exist
    if not all(col in df.columns for col in required_cols):
        print(f"⚠ Warning: User data missing required columns. Skipping.")
        return pd.DataFrame()
    
    df = df[required_cols].copy()
    
    # Add dataset source identifier
    df['dataset_source'] = 'user_contributed'
    
    # Clean data
    df = df.dropna()
    
    print(f"✓ Loaded {len(df)} user-contributed samples")
    return df

def combine_datasets(df1, df2, df3, df_user=None):
    """Combine all datasets including user-contributed data into one unified dataset"""
    print("\n=== Combining Datasets ===")
    
    # Get common columns
    common_cols = ['sleep_quality', 'headaches_per_week', 'academic_performance', 
                   'study_load', 'extracurricular_frequency', 'stress_level', 'dataset_source']
    
    # Ensure all datasets have these columns
    dfs = []
    
    # Dataset 1 (Student Stress Factors)
    if all(col in df1.columns for col in common_cols):
        dfs.append(df1[common_cols])
        print(f"✓ Dataset 1: {len(df1)} samples")
    
    # Dataset 2 (Stress Level)
    if all(col in df2.columns for col in common_cols):
        dfs.append(df2[common_cols])
        print(f"✓ Dataset 2: {len(df2)} samples")
    
    # Dataset 3 (Comprehensive Stress)
    if all(col in df3.columns for col in common_cols):
        dfs.append(df3[common_cols])
        print(f"✓ Dataset 3: {len(df3)} samples")
    
    # Dataset 4 (User-Contributed)
    if df_user is not None and len(df_user) > 0 and all(col in df_user.columns for col in common_cols):
        dfs.append(df_user[common_cols])
        print(f"✓ Dataset 4 (User-Contributed): {len(df_user)} samples")
    
    if len(dfs) == 0:
        print("⚠ Warning: Could not combine datasets. Using only Dataset 1.")
        return df1
    
    # Combine all datasets
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Clean the data
    combined_df = combined_df.dropna()
    
    # Convert stress_level to numeric, coercing errors
    combined_df['stress_level'] = pd.to_numeric(combined_df['stress_level'], errors='coerce')
    combined_df = combined_df.dropna(subset=['stress_level'])

    # Ensure stress_level is within 1-5 range
    combined_df['stress_level'] = combined_df['stress_level'].clip(1, 5).round()
    
    # Ensure all features are numeric and within reasonable ranges
    combined_df['sleep_quality'] = combined_df['sleep_quality'].clip(1, 5)
    combined_df['headaches_per_week'] = combined_df['headaches_per_week'].clip(0, 7)
    combined_df['academic_performance'] = combined_df['academic_performance'].clip(1, 5)
    combined_df['study_load'] = combined_df['study_load'].clip(1, 5)
    combined_df['extracurricular_frequency'] = combined_df['extracurricular_frequency'].clip(0, 7)
    
    print(f"\n✓ Combined dataset: {len(combined_df)} total samples")
    print(f"  Features: {len(combined_df.columns) - 2}")  # Excluding target and source
    print(f"\nDataset distribution:")
    print(combined_df['dataset_source'].value_counts())
    print(f"\nStress level distribution:")
    print(combined_df['stress_level'].value_counts().sort_index())
    
    return combined_df

def ingest_and_process_multi_dataset(
    dataset1_path='Student Stress Factors (2).csv',
    dataset2_path='StressLevelDataset.csv',
    dataset3_path='Stress_Dataset.csv',
    user_data_path='user_inputs.csv',
    processed_folder='data/processed'
):
    """
    Loads multiple datasets including user-contributed data, combines them, and saves train/test splits.
    """
    print("=" * 60)
    print("MULTI-DATASET INGESTION PIPELINE (Including User Data)")
    print("=" * 60)
    
    # Get absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(processed_folder):
        processed_folder = os.path.join(script_dir, processed_folder)
    
    # Load all datasets
    try:
        df1 = load_student_stress_factors(dataset1_path)
    except Exception as e:
        print(f"Error loading dataset 1: {e}")
        return False
    
    try:
        df2 = load_stress_level_dataset(dataset2_path)
    except Exception as e:
        print(f"⚠ Warning: Could not load dataset 2: {e}")
        df2 = pd.DataFrame(columns=df1.columns)
    
    try:
        df3 = load_stress_dataset(dataset3_path)
    except Exception as e:
        print(f"⚠ Warning: Could not load dataset 3: {e}")
        df3 = pd.DataFrame(columns=df1.columns)
    
    # Load user-contributed data
    try:
        df_user = load_user_contributed_data(user_data_path)
    except Exception as e:
        print(f"⚠ Warning: Could not load user data: {e}")
        df_user = pd.DataFrame()
    
    # Combine datasets
    combined_df = combine_datasets(df1, df2, df3, df_user)
    
    # Feature Engineering
    print("\n=== Feature Engineering ===")
    # Create wellbeing score (inverse of headaches and positive sleep)
    combined_df['wellbeing_score'] = (combined_df['sleep_quality'] - (combined_df['headaches_per_week'] / 2))
    
    # Create academic pressure score
    combined_df['academic_pressure'] = combined_df['study_load'] * (6 - combined_df['academic_performance'])
    
    # Create total workload
    combined_df['total_workload'] = combined_df['study_load'] + (combined_df['extracurricular_frequency'] / 2)
    
    print("✓ Created 3 engineered features")
    
    # Separate features and target
    feature_cols = ['sleep_quality', 'headaches_per_week', 'academic_performance', 
                   'study_load', 'extracurricular_frequency', 
                   'wellbeing_score', 'academic_pressure', 'total_workload']
    
    X = combined_df[feature_cols]
    y = combined_df['stress_level']
    
    print(f"\n✓ Features shape: {X.shape}")
    print(f"✓ Target shape: {y.shape}")
    
    # Split data
    print("\n=== Data Splitting ===")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"✓ Training samples: {len(X_train)}")
    print(f"✓ Testing samples: {len(X_test)}")
    
    # Save processed data
    print(f"\n=== Saving to {processed_folder} ===")
    os.makedirs(processed_folder, exist_ok=True)
    
    X_train.to_csv(os.path.join(processed_folder, 'X_train.csv'), index=False)
    X_test.to_csv(os.path.join(processed_folder, 'X_test.csv'), index=False)
    y_train.to_csv(os.path.join(processed_folder, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(processed_folder, 'y_test.csv'), index=False)
    
    # Also save the combined dataset for visualization
    combined_df.to_csv(os.path.join(processed_folder, 'combined_dataset.csv'), index=False)
    
    print("✓ All files saved successfully!")
    
    print("\n" + "=" * 60)
    print("INGESTION COMPLETE!")
    print("=" * 60)
    print(f"Total samples: {len(combined_df)}")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Features: {len(feature_cols)}")
    
    return True

if __name__ == '__main__':
    success = ingest_and_process_multi_dataset()
    if success:
        print("\n🎉 Multi-dataset ingestion completed successfully!")
    else:
        print("\n❌ Ingestion failed. Check errors above.")
