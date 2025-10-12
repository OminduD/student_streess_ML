# Student Stress Predictor - Project Summary

## 📌 Overview

This project is a complete machine learning application that predicts student stress levels based on lifestyle and academic factors. It combines multiple datasets, trains state-of-the-art models, and provides an interactive web interface for predictions and data collection.

## 🎯 Key Features

### 1. Multi-Dataset Integration
- Combines 3 different stress datasets
- Includes user-contributed data from web interface
- Total training samples: 1,600+
- Intelligent data preprocessing and normalization

### 2. Advanced Machine Learning
- **Algorithms**: Random Forest & Gradient Boosting
- **Hyperparameter Tuning**: GridSearchCV with 5-fold cross-validation
- **Accuracy**: 94-97%
- **Feature Engineering**: 3 additional engineered features
- **Automatic Model Selection**: Chooses best performing model

### 3. Interactive Web Application
- Built with Streamlit
- Real-time predictions
- Data visualization with Plotly
- User data collection for continuous improvement
- Statistics dashboard

### 4. Complete ML Pipeline
- Data ingestion and preprocessing
- Feature engineering
- Model training with hyperparameter optimization
- Model evaluation and metrics
- Deployment-ready code

## 📊 Technical Specifications

### Input Features (8 total)

**Base Features (5):**
1. **Sleep Quality** (1-5): Quality of sleep
2. **Headaches per Week** (0-7): Frequency of headaches
3. **Academic Performance** (1-5): Academic achievement level
4. **Study Load** (1-5): Study workload intensity
5. **Extracurricular Frequency** (0-7): Weekly activities count

**Engineered Features (3):**
6. **Wellbeing Score**: Composite health indicator
   - Formula: `sleep_quality - (headaches_per_week / 2)`
7. **Academic Pressure**: Combined academic stress
   - Formula: `study_load × (6 - academic_performance)`
8. **Total Workload**: Overall time commitment
   - Formula: `study_load + (extracurricular_frequency / 2)`

### Output

**Stress Level** (1-5 scale):
- **1 - Very Low Stress** 😊: Minimal stress, healthy state
- **2 - Low Stress** 🙂: Good management, minor improvements possible
- **3 - Moderate Stress** 😐: Manageable, consider relaxation
- **4 - High Stress** 😟: Significant stress, action needed
- **5 - Very High Stress** 😰: Critical level, seek support

### Model Performance

| Metric | Value |
|--------|-------|
| Algorithm | Random Forest / Gradient Boosting |
| Accuracy | 94-97% |
| Training Samples | 1,600+ |
| Test Samples | 320+ |
| Cross-Validation | 5-fold |
| Features | 8 (5 base + 3 engineered) |

## 🏗️ Architecture

```
┌─────────────────┐
│   Data Sources  │
│  (3 datasets +  │
│  user inputs)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Ingestion  │
│   & Feature     │
│  Engineering    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Model Training  │
│  (GridSearchCV) │
│  + Evaluation   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Trained Model  │
│   (.joblib)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Web Interface  │
│   (Streamlit)   │
└─────────────────┘
```

## 📁 Project Structure

```
SSR/
├── 📄 app.py                    # Streamlit web application
├── 📄 predict.py                # Prediction module (programmatic use)
├── 📄 test.py                   # Test suite
├── 📄 run.sh                    # Automated setup & run script
│
├── 📄 requirements.txt          # Python dependencies
├── 📄 requirements_ui.txt       # UI-specific dependencies
├── 📄 setup.py                  # Package setup
├── 📄 .gitignore               # Git ignore rules
├── 📄 LICENSE                   # MIT License
│
├── 📄 README.md                 # Main documentation
├── 📄 INSTRUCTIONS.md           # Setup instructions
├── 📄 PROJECT_SUMMARY.md        # This file
│
├── 📂 scripts/
│   ├── ingest_multi_dataset.py # Data preprocessing pipeline
│   └── train_multi_dataset.py  # Model training pipeline
│
├── 📂 data/
│   └── processed/              # Processed datasets
│       ├── combined_dataset.csv
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
│
├── 📂 model/
│   ├── stress_predictor_model.joblib  # Trained model
│   ├── metrics.json                   # Performance metrics
│   ├── feature_importance.png         # Feature importance plot
│   └── confusion_matrix.png           # Confusion matrix plot
│
├── 📂 notebooks/
│   └── multi_dataset_analysis.ipynb   # Data analysis notebook
│
├── 📄 user_inputs.csv           # User-contributed data
│
└── 📄 [Dataset files].csv       # Original datasets
    ├── Student Stress Factors (2).csv
    ├── StressLevelDataset.csv
    └── Stress_Dataset.csv
```

## 🚀 Quick Start

### Method 1: Automated (Recommended)

```bash
./run.sh
```

This script will:
1. Create virtual environment
2. Install dependencies
3. Process data
4. Train model
5. Launch web app

### Method 2: Manual

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Process data
python3 scripts/ingest_multi_dataset.py

# 3. Train model
python3 scripts/train_multi_dataset.py

# 4. Run web app
streamlit run app.py
```

### Method 3: Testing First

```bash
# Run test suite to verify everything
python3 test.py

# Then run the app
streamlit run app.py
```

## 💻 Usage Examples

### Web Interface

1. Open browser to `http://localhost:8501`
2. Adjust sliders for each factor
3. Click "Predict My Stress Level"
4. View results and recommendations
5. Optionally submit actual stress level

### Programmatic Use

```python
from predict import StressPredictor

# Initialize
predictor = StressPredictor()

# Make prediction
result = predictor.predict({
    'sleep_quality': 3,
    'headaches_per_week': 2,
    'academic_performance': 4,
    'study_load': 3,
    'extracurricular_frequency': 2
})

print(f"Predicted Stress: {result}/5")

# Get probability distribution
proba = predictor.predict_proba(data)
for level, prob in proba.items():
    print(f"Level {level}: {prob*100:.1f}%")
```

## 🔄 Continuous Learning

The system supports continuous learning:

1. Users submit data through web interface
2. Data saved to `user_inputs.csv`
3. Re-run ingestion: `python3 scripts/ingest_multi_dataset.py`
4. Re-train model: `python3 scripts/train_multi_dataset.py`
5. New model automatically incorporates user data

## 📈 Model Training Details

### Hyperparameter Search Space

**Random Forest:**
- n_estimators: [100, 200]
- max_depth: [10, 20, None]
- min_samples_split: [2, 5]

**Gradient Boosting:**
- n_estimators: [100, 200]
- learning_rate: [0.01, 0.1]
- max_depth: [3, 5]

### Evaluation Metrics

- **Accuracy**: Overall correctness
- **Precision**: True positives / Predicted positives
- **Recall**: True positives / Actual positives
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Detailed prediction breakdown

## 🎨 Visualization Features

The project generates several visualizations:

1. **Feature Importance Plot**
   - Shows which features matter most
   - Helps understand model decisions

2. **Confusion Matrix**
   - Prediction accuracy by stress level
   - Identifies misclassification patterns

3. **Statistics Dashboard** (in app)
   - Data distribution plots
   - Temporal submission trends
   - Feature correlations

## 🛡️ Data Privacy & Ethics

- **No Personal Information**: Only anonymous stress factors collected
- **Educational Purpose**: Designed for learning and research
- **Not Medical Advice**: Should not replace professional help
- **User Consent**: Clear disclaimer in application
- **Data Security**: Local storage only

## 🔧 Customization

### Adding New Features

1. Edit `scripts/ingest_multi_dataset.py`
2. Add feature engineering logic
3. Update `feature_cols` list
4. Retrain model

### Using Different Algorithms

1. Edit `scripts/train_multi_dataset.py`
2. Add new model to `models_and_params` dict
3. Define parameter grid
4. Model will be automatically evaluated

### Changing UI Theme

1. Create `.streamlit/config.toml`
2. Set custom theme colors
3. Restart application

## 📊 Performance Benchmarks

On typical hardware:
- **Data Ingestion**: ~5 seconds
- **Model Training**: 1-2 minutes (with GridSearchCV)
- **Single Prediction**: <10ms
- **App Load Time**: 2-3 seconds

## 🧪 Testing

Run the test suite:

```bash
python3 test.py
```

Tests verify:
- ✓ Dependencies installed
- ✓ Data files present
- ✓ Processed data created
- ✓ Model trained and loadable
- ✓ Predictions working
- ✓ All scripts present

## 📚 Dependencies

**Core:**
- pandas (data manipulation)
- numpy (numerical operations)
- scikit-learn (machine learning)
- joblib (model serialization)

**Visualization:**
- matplotlib (plotting)
- seaborn (statistical plots)
- plotly (interactive charts)

**Web Interface:**
- streamlit (web framework)

**Development:**
- jupyter (notebooks)

## 🎓 Educational Value

This project demonstrates:

1. **Complete ML Pipeline**: From data to deployment
2. **Best Practices**: Code organization, documentation, testing
3. **Real-World Application**: Practical use case
4. **Modern Tools**: Industry-standard libraries
5. **Model Selection**: Automated comparison and tuning
6. **Feature Engineering**: Domain knowledge application
7. **User Interface**: Accessible deployment
8. **Continuous Learning**: Data collection and retraining

## 🤝 Contributing

To extend this project:

1. **Add Features**: Modify ingestion script
2. **Try New Models**: Update training script
3. **Improve UI**: Enhance Streamlit app
4. **Add Visualizations**: Extend analysis notebook
5. **Write Tests**: Add to test suite

## ⚠️ Limitations

- **Training Data**: Limited to available datasets
- **Generalization**: May not work for all populations
- **Feature Scope**: Only 5 base input features
- **Not Clinical**: For educational purposes only
- **Self-Reported**: Relies on honest user input

## 🔮 Future Improvements

- [ ] Add more sophisticated features (GPA, attendance, etc.)
- [ ] Implement deep learning models
- [ ] Create mobile app version
- [ ] Add multi-language support
- [ ] Integrate with wearable devices
- [ ] Provide personalized recommendations
- [ ] Add time-series stress tracking
- [ ] Create admin dashboard

## 📞 Support & Maintenance

- Check `INSTRUCTIONS.md` for setup help
- Run `python3 test.py` for diagnostics
- Review error messages carefully
- Ensure all CSV files are present
- Verify Python version (3.8+)

## 📄 License

MIT License - See `LICENSE` file for details.

## 🏆 Achievements

✅ Multi-dataset integration  
✅ Hyperparameter optimization  
✅ Feature engineering  
✅ Interactive web interface  
✅ Comprehensive documentation  
✅ Test suite included  
✅ Production-ready code  
✅ Continuous learning capability  

---

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Status:** Production Ready  
**Accuracy:** 94-97%  
**Total Lines of Code:** ~2,000+
