# Student Stress Predictor# Student Stress Predictor



A machine learning application that predicts student stress levels based on lifestyle and academic factors, featuring a web interface built with Streamlit and optional AI-powered personalized recommendations.A machine learning application that predicts student stress levels based on lifestyle and academic factors, featuring a web interface built with Streamlit and optional AI-powered personalized recommendations.



## 📋 Table of Contents



- [Features](#-features)## Project Structure## Project Structure

- [Quick Start](#-quick-start)

- [Project Structure](#-project-structure)

- [How It Works](#-how-it-works)

- [AI Recommendations](#-ai-recommendations-optional)``````

- [Model Training](#-model-training)

- [File Descriptions](#-file-descriptions)//

- [Requirements](#-requirements)

├── app.py                          # Main Streamlit application├── app.py                          # Main Streamlit application

## ✨ Features

├── requirements.txt                # Project dependencies├── requirements.txt                # Project dependencies

### Core Features

- 🎯 **Stress Level Prediction**: ML-based prediction using 5 lifestyle factors├── requirements_ui.txt             # UI-specific dependencies├── requirements_ui.txt             # UI-specific dependencies

- 📊 **Interactive Web UI**: Clean Streamlit interface for data input

- 💾 **Data Storage**: Automatic saving of user inputs and predictions├── user_inputs.csv                 # Stores data from user inputs├── user_inputs.csv                 # Stores data from user inputs

- 🤖 **AI Recommendations**: Optional personalized recommendations (Hugging Face, OpenAI, etc.)

- 🛡️ **Automatic Fallback**: Rule-based recommendations if AI is unavailable├── data/├── data/



### Input Features (5 Core Factors)│   └── processed/                  # Processed data for training│   └── processed/                  # Processed data for training

1. **Sleep Quality** (1-5): Quality of sleep rating

2. **Headaches per Week** (0-7): Frequency of headaches├── model/├── model/

3. **Academic Performance** (1-5): Academic achievement level

4. **Study Load** (1-5): Study workload intensity│   ├── stress_predictor_model.joblib # The trained model│   ├── stress_predictor_model.joblib # The trained model

5. **Extracurricular Frequency** (0-7): Weekly activities count

│   └── metrics.json                # Model performance metrics│   └── metrics.json                # Model performance metrics

### Output

- **Stress Level** (1-5):├── notebooks/├── notebooks/

  - 1: Very Low Stress

  - 2: Low Stress│   └── multi_dataset_analysis.ipynb  # Exploratory data analysis│   └── multi_dataset_analysis.ipynb  # Exploratory data analysis

  - 3: Moderate Stress

  - 4: High Stress└── scripts/└── scripts/

  - 5: Very High Stress

- **Personalized Recommendations**: Tips to manage stress (AI or rule-based)    ├── ingest_multi_dataset.py     # Data ingestion and preprocessing    ├── ingest_multi_dataset.py     # Data ingestion and preprocessing



## 🚀 Quick Start    └── train_multi_dataset.py      # Model training script    └── train_multi_dataset.py      # Model training script



### 1. Installation``````



```bash

# Create and activate a conda environment (recommended)

conda create -n studentStress_env python=3.11## ✨ AI-Powered Recommendations

conda activate studentStress_env

This project now includes **AI-powered personalized recommendations**! 

# Install dependencies

pip install -r requirements_ui.txt- 🤖 Supports **Hugging Face (FREE!)**, **OpenAI (GPT-3.5/4)**, **Anthropic (Claude)**, or **custom APIs**

```- 🆓 **Hugging Face free tier** - 1000 requests/day, no credit card needed!

- 🛡️ **Automatic fallback** to rule-based recommendations

### 2. Run the Application- 🔒 **Secure** - API keys protected by .gitignore



```bash**⚡ Quick Setup - Hugging Face (FREE, 2 minutes):**

# Start the Streamlit application```bash

streamlit run app.py# 1. Get FREE token from https://huggingface.co/settings/tokens (no card!)

```# 2. Set environment variable

export AI_API_KEY="hf_your_token_here"

The application will open in your browser at `http://localhost:8501`# 3. Enable in ai_config.json (set "enabled": true, "provider": "huggingface")

# 4. Test it (first run may take 30s)

### 3. Using the Applicationpython3 test_huggingface.py

```

1. **Enter your information** using the sliders for each factor

2. **Click "Predict Stress Level"** to get your prediction📖 **Setup Guides:** 

3. **View personalized recommendations** tailored to your stress level- 🤗 [HUGGINGFACE_SETUP.md](HUGGINGFACE_SETUP.md) - **FREE AI** (recommended for students!)

4. Your data is automatically saved to `user_inputs.csv`- 🚀 [QUICK_FIX_AI.md](QUICK_FIX_AI.md) - Quick comparison of all providers

- 📚 [AI_SETUP_GUIDE.md](AI_SETUP_GUIDE.md) - Complete OpenAI/Anthropic docs

## 📁 Project Structure

> **Note:** AI is optional! The app works perfectly with rule-based recommendations (current default).

```

SSR/---

├── app.py                          # Main Streamlit application

├── ai_recommender.py               # AI recommendation engine## Quick Start## Quick Start

├── ai_config.json                  # AI configuration file

├── requirements_ui.txt             # Project dependencies

├── user_inputs.csv                 # Stored user inputs (auto-generated)

├── README.md                       # This file### 1. Installation### 1. Installation

│

├── data/                           # Data directory

│   └── processed/                  # Processed datasets

│       ├── combined_dataset.csv    # Combined training dataFirst, ensure you have Python 3.8+ installed. Then, create a virtual environment and install the required packages.First, ensure you have Python 3.8+ installed. Then, create a virtual environment and install the required packages.

│       ├── X_train.csv             # Training features

│       ├── X_test.csv              # Test features

│       ├── y_train.csv             # Training labels

│       └── y_test.csv              # Test labels```bash```bash

│

├── model/                          # Model directory# Create and activate a virtual environment (optional but recommended)# Create and activate a virtual environment (optional but recommended)

│   ├── stress_predictor_model.joblib  # Trained ML model

│   └── metrics.json                # Model performance metricspython -m venv venvpython -m venv venv

│

├── notebooks/                      # Analysis notebookssource venv/bin/activatesource venv/bin/activate

│   └── multi_dataset_analysis.ipynb   # Data analysis

│

└── scripts/                        # Training scripts

    ├── ingest_multi_dataset.py     # Data preprocessing# Install dependencies# Install dependencies

    └── train_multi_dataset.py      # Model training

```pip install -r requirements.txtpip install -r requirements.txt



## 🔧 How It Workspip install -r requirements_ui.txtpip install -r requirements_ui.txt



### Prediction Pipeline``````



```

User Input → Feature Engineering → ML Model → Stress Level Prediction → Recommendations

```### 2. Run the Application### 2. Run the Application



### 1. Data Collection

- User inputs 5 key lifestyle and academic factors via the web interface

- Additional features are automatically engineered from the inputs:To start the Streamlit web interface, run the following command:To start the Streamlit web interface, run the following command:

  - `wellbeing_score` = (sleep_quality + (8 - headaches_per_week)) / 2

  - `academic_pressure` = (study_load + (6 - academic_performance)) / 2

  - `total_workload` = study_load + extracurricular_frequency

```bash```bash

### 2. Prediction

- The pre-trained `RandomForestClassifier` model processes the 8 featuresstreamlit run app.pystreamlit run app.py

- Model outputs a stress level prediction (1-5 scale)

- Prediction accuracy: ~94-97% on test data``````



### 3. Recommendations

- AI-powered recommendations (if enabled) or rule-based fallback

- Personalized tips based on stress level and contributing factorsNavigate to the URL provided by Streamlit in your web browser to use the application.Navigate to the URL provided by Streamlit in your web browser to use the application.

- Actionable advice for stress management



### 4. Data Storage

- All inputs and predictions are saved to `user_inputs.csv`## How It Works## How It Works

- Data can be used for future model retraining and improvement



## 🤖 AI Recommendations (Optional)

The application takes user inputs for five key factors:The application takes user inputs for five key factors:

The application includes optional AI-powered personalized recommendations with automatic fallback to rule-based recommendations.



### Supported AI Providers

1.  **Sleep Quality** (1-5)1.  **Sleep Quality** (1-5)

- **Hugging Face** (FREE) - 1000 requests/day, no credit card needed

- **OpenAI** (GPT-3.5/4) - Paid API2.  **Headaches per Week** (0-7)2.  **Headaches per Week** (0-7)

- **Anthropic** (Claude) - Paid API

- **Custom API** - Your own endpoint3.  **Academic Performance** (1-5)3.  **Academic Performance** (1-5)



### How to Enable AI Recommendations4.  **Study Load** (1-5)4.  **Study Load** (1-5)



#### Option 1: Hugging Face (FREE - Recommended)5.  **Extracurricular Frequency** (0-7)5.  **Extracurricular Frequency** (0-7)



1. **Get a FREE API token** (no credit card required):

   - Visit: https://huggingface.co/settings/tokens

   - Click "New token" → Create a token with "Read" permissionsIt then uses a pre-trained `RandomForestClassifier` model to predict the student's stress level on a scale of 1 to 5. The user's input and the model's prediction are saved to `user_inputs.csv`.It then uses a pre-trained `RandomForestClassifier` model to predict the student's stress level on a scale of 1 to 5. The user's input and the model's prediction are saved to `user_inputs.csv`.

   - Copy your token (starts with `hf_...`)



2. **Set your API key** (choose one method):

## Training the Model## Training the Model

   **Method A: Environment Variable (Recommended)**

   ```bash

   export AI_API_KEY="hf_your_token_here"

   ```If you want to retrain the model, you can run the data ingestion and training scripts.If you want to retrain the model, you can run the data ingestion and training scripts.



   **Method B: Config File**

   - Edit `ai_config.json`

   - Add your token to the `"api_key"` field```bash```bash



3. **Enable AI in configuration**:# 1. Process the raw data# 1. Process the raw data

   - Open `ai_config.json`

   - Set `"enabled": true`python scripts/ingest_multi_dataset.pypython scripts/ingest_multi_dataset.py

   - Set `"provider": "huggingface"`



4. **Restart the application**:

   ```bash# 2. Train the model# 2. Train the model

   streamlit run app.py

   ```python scripts/train_multi_dataset.pypython scripts/train_multi_dataset.py



#### Option 2: OpenAI (Paid)``````



1. Get API key from: https://platform.openai.com/api-keys

2. Set environment variable:

   ```bashThis will create a new `stress_predictor_model.joblib` file in the `model/` directory.This will create a new `stress_predictor_model.joblib` file in the `model/` directory.

   export AI_API_KEY="sk-your_openai_key"

   ```

3. In `ai_config.json`:

   - Set `"enabled": true`## Quick Start

   - Set `"provider": "openai"`

   - Set `"model": "gpt-3.5-turbo"`### 1. Installation



### AI Configuration File (`ai_config.json`)First, ensure you have Python 3.8+ installed. Then, create a virtual environment and install the required packages.



```json```bash

{# Create and activate a virtual environment (optional but recommended)

    "enabled": false,              // Set to true to enable AIpython -m venv venv

    "provider": "huggingface",     // AI provider: openai, huggingface, anthropic, customsource venv/bin/activate

    "api_key": "",                 // Your API key (or use AI_API_KEY env variable)

    "model": "mistralai/Mistral-7B-Instruct-v0.2",# Install dependencies

    "max_tokens": 500,pip install -r requirements.txt

    "timeout": 30pip install -r requirements_ui.txt

}```

```

### 2. Run the Application

### Features of AI Recommendations

To start the Streamlit web interface, run the following command:

✅ **Automatic Fallback**: If AI fails, rule-based recommendations are used  

✅ **Secure**: API keys protected by `.gitignore`  ```bash

✅ **Flexible**: Multiple provider support  streamlit run app.py

✅ **Optional**: App works perfectly without AI enabled```



### Testing AI SetupNavigate to the URL provided by Streamlit in your web browser to use the application.



To test if your AI configuration is working:## How It Works



1. Enable AI in `ai_config.json`The application takes user inputs for five key factors:

2. Run the application

3. Make a prediction1.  **Sleep Quality** (1-5)

4. Check if AI recommendations appear (look for more detailed, personalized advice)2.  **Headaches per Week** (0-7)

3.  **Academic Performance** (1-5)

**Note**: First request may take 20-30 seconds for model cold start on Hugging Face free tier.4.  **Study Load** (1-5)

5.  **Extracurricular Frequency** (0-7)

## 🎓 Model Training

It then uses a pre-trained `RandomForestClassifier` model to predict the student's stress level on a scale of 1 to 5. The user's input and the model's prediction are saved to `user_inputs.csv`.

If you want to retrain the model with new data or different parameters:

## Training the Model

### Step 1: Prepare Data

If you want to retrain the model, you can run the data ingestion and training scripts.

```bash

# Process raw datasets and create training files```bash

python scripts/ingest_multi_dataset.py# 1. Process the raw data

```python scripts/ingest_multi_dataset.py



**What it does:**# 2. Train the model

- Loads multiple stress datasetspython scripts/train_multi_dataset.py

- Cleans and preprocesses data```

- Engineers new features

- Splits into train/test setsThis will create a new `stress_predictor_model.joblib` file in the `model/` directory.

- Saves processed data to `data/processed/`

## Quick Start

### Step 2: Train Model

### 1. Installation

```bash

# Train the machine learning modelFirst, ensure you have Python 3.8+ installed. Then, create a virtual environment and install the required packages.

python scripts/train_multi_dataset.py

``````bash

# Create and activate a virtual environment (optional but recommended)

**What it does:**python -m venv venv

- Loads processed training datasource venv/bin/activate

- Trains RandomForest and GradientBoosting models

- Selects the best performing model# Install dependencies

- Saves model to `model/stress_predictor_model.joblib`pip install -r requirements.txt

- Saves performance metrics to `model/metrics.json`pip install -r requirements_ui.txt

```

### Model Performance

### 2. Run the Application

- **Algorithm**: RandomForest Classifier

- **Training Samples**: 1600+ (combined from 3 datasets)To start the Streamlit web interface, run the following command:

- **Features**: 8 (5 base + 3 engineered)

- **Accuracy**: 94-97%```bash

- **Cross-Validation**: 5-fold CV for robust evaluationstreamlit run app.py

```

## 📄 File Descriptions

Navigate to the URL provided by Streamlit in your web browser to use the application.

### Core Application Files

## How It Works

| File | Purpose | When to Use |

|------|---------|-------------|The application takes user inputs for five key factors:

| `app.py` | Main Streamlit web application | Run this to start the app |

| `ai_recommender.py` | AI recommendation engine | Generates personalized recommendations |1.  **Sleep Quality** (1-5)

| `ai_config.json` | AI configuration settings | Edit to enable/configure AI features |2.  **Headaches per Week** (0-7)

| `requirements_ui.txt` | Python dependencies | Install before running the app |3.  **Academic Performance** (1-5)

| `user_inputs.csv` | User data storage | Auto-generated when users submit data |4.  **Study Load** (1-5)

5.  **Extracurricular Frequency** (0-7)

### Data Files

It then uses a pre-trained `RandomForestClassifier` model to predict the student's stress level on a scale of 1 to 5. The user's input and the model's prediction are saved to `user_inputs.csv`.

| Directory | Contents | Purpose |

|-----------|----------|---------|## Training the Model

| `data/processed/` | Preprocessed datasets | Used for model training |

| `Stress_Dataset.csv` | Raw dataset #1 | Original data source |If you want to retrain the model, you can run the data ingestion and training scripts.

| `StressLevelDataset.csv` | Raw dataset #2 | Original data source |

| `Student Stress Factors (2).csv` | Raw dataset #3 | Original data source |```bash

# 1. Process the raw data

### Model Filespython scripts/ingest_multi_dataset.py



| File | Purpose |# 2. Train the model

|------|---------|python scripts/train_multi_dataset.py

| `model/stress_predictor_model.joblib` | Trained ML model (RandomForest) |```

| `model/metrics.json` | Model performance metrics (accuracy, etc.) |

This will create a new `stress_predictor_model.joblib` file in the `model/` directory.

### Training Scripts



| Script | Purpose | When to Run |## 🎯 Key Features

|--------|---------|-------------|

| `scripts/ingest_multi_dataset.py` | Preprocesses raw data | Before training |### 🆕 User Data Collection (NEW!)

| `scripts/train_multi_dataset.py` | Trains the ML model | After data preprocessing |- **Web Frontend**: Collect real-world data from users

- **API Integration**: RESTful API for data submission and predictions

### Analysis- **Continuous Learning**: Model improves with more user submissions

- **Real-time Statistics**: Track collected data and model performance

| File | Purpose |

|------|---------|### Input Features (5 core + 3 engineered)

| `notebooks/multi_dataset_analysis.ipynb` | Exploratory data analysis and visualizations |1. **Sleep Quality** (1-5): Sleep quality rating

2. **Headaches per Week** (0-7): Frequency of headaches

## 📦 Requirements3. **Academic Performance** (1-5): Academic achievement level

4. **Study Load** (1-5): Study workload intensity

### Python Environment5. **Extracurricular Frequency** (0-7): Weekly activities count



```bash**Engineered Features:**

# Recommended: Use Conda- `wellbeing_score` = (sleep_quality + (8 - headaches_per_week)) / 2

conda create -n studentStress_env python=3.11- `academic_pressure` = (study_load + (6 - academic_performance)) / 2

conda activate studentStress_env- `total_workload` = study_load + extracurricular_frequency

```

### Output

### Dependencies- **Stress Level** (1-5):

  - 1: Very Low Stress

The main dependencies are listed in `requirements_ui.txt`:  - 2: Low Stress

  - 3: Moderate Stress

- **streamlit** - Web application framework  - 4: High Stress

- **pandas** - Data manipulation  - 5: Very High Stress

- **numpy** - Numerical computing

- **scikit-learn** - Machine learning algorithms## 🚀 Quick Start

- **joblib** - Model serialization

- **requests** - HTTP requests for AI APIs### Installation



Install all dependencies:```bash

# Install required packages

```bashpip install -r requirements.txt

pip install -r requirements_ui.txt

```# Or install individually

pip install pandas numpy scikit-learn matplotlib seaborn joblib jupyter

## 🔍 Troubleshooting

# For API server (optional)

### Common Issuespip install flask flask-cors

```

**Issue**: "Model file not found"

- **Solution**: Ensure `model/stress_predictor_model.joblib` exists. If not, run training scripts.### 1. Data Ingestion (Includes User Data)



**Issue**: "AI recommendations not working"```bash

- **Solution**: AI is optional. Check that `ai_config.json` has `"enabled": true` and valid API key.# Multi-dataset approach including user-contributed data (recommended)

python3 scripts/ingest_multi_dataset.py

**Issue**: "Import errors"

- **Solution**: Install all dependencies: `pip install -r requirements_ui.txt`# Single dataset approach

python3 scripts/ingest.py

**Issue**: "Hugging Face cold start timeout"```

- **Solution**: First request may take 20-30 seconds. Wait or use a different model.

### 2. Model Training

### Getting Help

```bash

If you encounter issues:# Multi-dataset training (1600+ samples + user data, best accuracy)

1. Check the terminal for error messagespython3 scripts/train_multi_dataset.py

2. Verify all dependencies are installed

3. Ensure the conda environment is activated# Single dataset training

4. Check that model files exist in `model/` directorypython3 scripts/train.py

```

## 📊 Data Privacy

### 3. Frontend & API (NEW!)

- User input data is stored locally in `user_inputs.csv`

- No data is sent to external servers (except AI API if enabled)```bash

- AI API keys should be stored securely using environment variables# Start the API server

- `ai_config.json` is included in `.gitignore` to protect API keyscd scripts

python3 api_server.py

## 🎯 Use Cases

# Open the web frontend (in another terminal)

- **Students**: Self-assess stress levels and get management tipscd frontend

- **Educators**: Understand factors affecting student stresspython3 -m http.server 8000

- **Researchers**: Collect data on student stress patterns

- **Wellness Programs**: Tool for stress screening and intervention# Access at: http://localhost:8000

```

## 📚 Future Enhancements

### 4. Analysis & Visualization

- [ ] Add more input features (social factors, financial concerns)

- [ ] Implement trend tracking over time```bash

- [ ] Create mobile-friendly interface# Open Jupyter notebook

- [ ] Add data visualization dashboardjupyter notebook notebooks/multi_dataset_analysis.ipynb

- [ ] Implement user accounts and history```



---## 📊 Model Performance



**Last Updated**: October 2025  - **Algorithm**: RandomForest or GradientBoosting (auto-selected)

**Python Version**: 3.11+  - **Training Samples**: 1600+ (from 3 combined datasets)

**License**: MIT  - **Features**: 8 (5 base + 3 engineered)

**Environment**: studentStress_env (conda)- **Accuracy**: 94-97%

- **Classes**: 5 stress levels

For questions or contributions, please open an issue on the project repository.

## 🆕 User Data Collection System

This project now includes a complete system for collecting real-world user data through a web frontend!

### Features

- **📝 Data Submission**: Users can submit their stress data through a web interface
- **🔮 Real-time Predictions**: Instant stress level predictions
- **📊 Statistics Dashboard**: View collected data statistics
- **🔄 Continuous Learning**: Retrain models with new user data
- **🌐 REST API**: Full API for frontend integration

### New Files

- `user_inputs.csv` - Stores all user-submitted data
- `scripts/user_data_handler.py` - Handles user data collection and management
- `scripts/api_server.py` - Flask REST API server
- `frontend/index.html` - Web interface for data collection

### API Endpoints

- `GET /api/health` - Check API status
- `POST /api/predict` - Predict stress level from input
- `POST /api/submit` - Submit user data for training
- `GET /api/statistics` - Get collected data statistics
- `POST /api/retrain` - Retrain model with new data
- `GET /api/data/export` - Export all collected data

### How to Use

1. **Start the API Server**:
   ```bash
   cd scripts
   python3 api_server.py
   ```

2. **Open the Frontend**:
   ```bash
   cd frontend
   python3 -m http.server 8000
   # Visit: http://localhost:8000
   ```

3. **Submit Data**: Use the web interface to:
   - Get stress predictions
   - Submit your actual stress levels
   - View statistics

4. **Retrain Model** (when you have enough new data):
   ```bash
   # The ingestion script now automatically includes user data
   python3 scripts/ingest_multi_dataset.py
   python3 scripts/train_multi_dataset.py
   ```

## 🔧 Requirements

### Python Environment

```bash
conda activate studentStress_env
```

### Required Packages

Install all dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

**Core packages**:

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- joblib
- jupyter (for notebooks)

**For API/Frontend (optional)**:

- flask
- flask-cors

## 📈 Workflow

```
1. Data Ingestion
   └─> scripts/ingest_multi_dataset.py
       └─> Combines 3 datasets
       └─> Creates engineered features
       └─> Saves to data/processed/

2. Model Training
   └─> scripts/train_multi_dataset.py
       └─> Loads processed data
       └─> Trains RandomForest + GradientBoosting
       └─> Selects best model
       └─> Saves to model/

3. Analysis & Visualization
   └─> notebooks/multi_dataset_analysis.ipynb
       └─> 12 comprehensive analysis sections
       └─> Generates 30+ visualizations
       └─> Statistical tests and insights
```

## 📝 Key Files

### Essential Training Scripts
- `scripts/ingest_multi_dataset.py` - Data preprocessing and feature engineering
- `scripts/train_multi_dataset.py` - Model training and evaluation

### Trained Model
- `model/stress_predictor_model.joblib` - Production-ready model

### Analysis Notebooks
- `notebooks/multi_dataset_analysis.ipynb` - Complete analysis with visualizations

### Documentation
- `MULTI_DATASET_GUIDE.md` - Detailed usage instructions
- `MULTI_DATASET_SUMMARY.md` - Project overview and methodology

## 🎨 Visualizations

The project includes 30+ generated visualizations:
- Correlation matrices
- Box plots and violin plots
- Pair plots and distribution charts
- Feature importance charts
- Confusion matrices
- Stress level distributions
- Dataset comparisons

All visualizations are saved in the `notebooks/` directory.

## 💡 Usage Examples

### Training a New Model
```bash
# Activate environment
conda activate studentStress_env

# Run full pipeline
python3 scripts/ingest_multi_dataset.py
python3 scripts/train_multi_dataset.py
```

### Making Predictions (programmatically)
```python
import joblib
import pandas as pd

# Load model
model = joblib.load('model/stress_predictor_model.joblib')

# Prepare input
data = pd.DataFrame([{
    'sleep_quality': 3,
    'headaches_per_week': 2,
    'academic_performance': 4,
    'study_load': 3,
    'extracurricular_frequency': 2,
    'wellbeing_score': 4.0,
    'academic_pressure': 2.5,
    'total_workload': 5
}])

# Predict
stress_level = model.predict(data)[0]
print(f"Predicted Stress Level: {stress_level}")
```

## 🔍 Dataset Information

### Combined Dataset Statistics
- **Total Samples**: 1600+
- **Sources**: 3 different datasets
- **Features**: 8 (5 original + 3 engineered)
- **Classes**: 5 stress levels (balanced distribution)

### Data Quality
- ✅ No missing values (after preprocessing)
- ✅ Feature scaling applied
- ✅ Train-test split: 80-20
- ✅ Balanced class distribution

## 🎯 Project Status

✅ **Completed:**
- Multi-dataset integration (3 datasets)
- Feature engineering (3 new features)
- Model training (94-97% accuracy)
- Comprehensive analysis notebook
- 30+ visualizations
- Complete documentation
- Clean project structure

## 📚 Documentation

1. **MULTI_DATASET_GUIDE.md** - Step-by-step usage guide
2. **MULTI_DATASET_SUMMARY.md** - Project methodology and results
3. **Notebook Comments** - Inline documentation in Jupyter notebooks

## 🤝 Contributing

To extend this project:
1. Add new features in `scripts/ingest_multi_dataset.py`
2. Experiment with algorithms in `scripts/train_multi_dataset.py`
3. Create new visualizations in notebooks
4. Update documentation as needed

## 📊 Model Files

All model artifacts are stored in the `model/` directory:
- Trained model (joblib format)
- Performance metrics (JSON)
- Visualizations (PNG)

These files are generated automatically during training.

---

**Last Updated**: October 2025  
**Python Version**: 3.11+  
**Environment**: studentStress_env (conda)
