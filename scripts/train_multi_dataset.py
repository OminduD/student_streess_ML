import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

def train_multi_dataset_model(processed_folder='../data/processed', model_folder='model'):
    """
    Trains model on combined multi-dataset with hyperparameter tuning.
    """
    print("=" * 70)
    print("ADVANCED MULTI-DATASET MODEL TRAINING (with Hyperparameter Tuning)") 
    print("=" * 70)
    
    # Load processed data
    try:
        X_train = pd.read_csv(os.path.join(processed_folder, 'X_train.csv'))
        X_test = pd.read_csv(os.path.join(processed_folder, 'X_test.csv'))
        y_train = pd.read_csv(os.path.join(processed_folder, 'y_train.csv')).values.ravel()
        y_test = pd.read_csv(os.path.join(processed_folder, 'y_test.csv')).values.ravel()
        
        print(f"\n✓ Data loaded successfully!")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Testing samples: {len(X_test)}")
        print(f"  Features: {len(X_train.columns)}")
        print(f"  Feature names: {X_train.columns.tolist()}")
        
    except FileNotFoundError:
        print("❌ Error: Processed data not found.")
        print("Please run 'python3 scripts/ingest_multi_dataset.py' first! ")
        return False
    
    # Define models and parameter grids for GridSearchCV
    models_and_params = {
        'Random Forest': {
            'model': RandomForestClassifier(random_state=42),
            'params': {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            }
        },
        'Gradient Boosting': {
            'model': GradientBoostingClassifier(random_state=42),
            'params': {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5]
            }
        }
    }
    
    results = {}
    best_model = None
    best_accuracy = 0
    best_model_name = ""
    
    print("\n" + "=" * 70)
    print("TRAINING MODELS WITH HYPERPARAMETER TUNING (GridSearchCV) ")
    print("=" * 70)
    
    for name, mp in models_and_params.items():
        print(f"\n[{name}]")
        print(f"Running GridSearchCV for {name}...")
        
        # Using n_jobs=-1 to use all available CPU cores
        grid_search = GridSearchCV(mp['model'], mp['params'], cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        
        print(f"✓ Best parameters found: {grid_search.best_params_}")
        
        # The best model found by the search
        model = grid_search.best_estimator_
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        results[name] = {
            'accuracy': accuracy,
            'report': report,
            'predictions': y_pred,
            'best_params': grid_search.best_params_
        }
        
        print(f"✓ Test Accuracy with best estimator: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_model_name = name
    
    # Display results comparison
    print("\n" + "=" * 70)
    print("TUNING RESULTS COMPARISON")
    print("=" * 70)
    
    for name, result in results.items():
        marker = "🏆" if name == best_model_name else "  "
        print(f"{marker} {name:20s}: {result['accuracy']:.4f} ({result['accuracy']*100:.2f}%)")
    
    print(f"\n🏆 Best Model: {best_model_name} with {best_accuracy*100:.2f}% accuracy")
    print(f"   Best parameters: {results[best_model_name]['best_params']}")
    
    # Detailed report for best model
    print("\n" + "=" * 70)
    print(f"DETAILED REPORT - {best_model_name}")
    print("=" * 70)
    
    print("\nClassification Report:")
    print(classification_report(y_test, results[best_model_name]['predictions']))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, results[best_model_name]['predictions'])
    print("\nConfusion Matrix:")
    print(cm)
    
    # Feature Importance
    if hasattr(best_model, 'feature_importances_'):
        print("\nFeature Importance:")
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in feature_importance.iterrows():
            print(f"  {row['feature']:30s}: {row['importance']:.4f}")
    
    # Save the best model
    os.makedirs(model_folder, exist_ok=True)
    
    model_path = os.path.join(model_folder, 'stress_predictor_model.joblib')
    joblib.dump(best_model, model_path)
    print(f"\n✓ Best model ({best_model_name}) saved to '{model_path}'")
    
    # Save metrics
    metrics = {
        'best_model': best_model_name,
        'accuracy': best_accuracy,
        'best_params': results[best_model_name]['best_params'],
        'all_results': {name: {'accuracy': res['accuracy']} for name, res in results.items()},
        'classification_report': results[best_model_name]['report'],
        'training_samples': len(X_train),
        'testing_samples': len(X_test),
        'features': X_train.columns.tolist()
    }
    
    metrics_path = os.path.join(model_folder, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"✓ Metrics saved to '{metrics_path}'")
    
    # Save feature importance plot
    if hasattr(best_model, 'feature_importances_'):
        plt.figure(figsize=(10, 6))
        feature_importance_sorted = feature_importance.sort_values('importance')
        plt.barh(range(len(feature_importance_sorted)), feature_importance_sorted['importance'])
        plt.yticks(range(len(feature_importance_sorted)), feature_importance_sorted['feature'])
        plt.xlabel('Importance')
        plt.title(f'Feature Importance - {best_model_name}')
        plt.tight_layout()
        
        plot_path = os.path.join(model_folder, 'feature_importance.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Feature importance plot saved to '{plot_path}'")
        plt.close()
    
    # Save confusion matrix plot
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'Confusion Matrix - {best_model_name}')
    plt.tight_layout()
    
    cm_path = os.path.join(model_folder, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    print(f"✓ Confusion matrix saved to '{cm_path}'")
    plt.close()
    
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE!")
    print("=" * 70)
    print(f"✓ Model: {best_model_name}")
    print(f"✓ Accuracy: {best_accuracy*100:.2f}%")
    print(f"✓ Training samples: {len(X_train)}")
    print(f"✓ Features used: {len(X_train.columns)}")
    
    return True

if __name__ == '__main__':
    success = train_multi_dataset_model()
    if success:
        print("\n🎉 Multi-dataset training completed successfully!")
    else:
        print("\n❌ Training failed. Check errors above.")
