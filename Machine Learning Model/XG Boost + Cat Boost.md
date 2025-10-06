** ml/preprocess.py **

```python

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

def load_and_preprocess(data_path: str):
    # Load dataset
    df = pd.read_csv(data_path)

    # Define numerical and categorical columns
    numerical_cols = ['age', 'albumin', 'sugar', 'glucose', 'urea', 'creatinine', 'sodium', 'potassium']
    categorical_cols = ['diabetes_mellitus', 'appetite']

    # Handle missing values
    imputer = KNNImputer(n_neighbors=5)
    df[numerical_cols] = imputer.fit_transform(df[numerical_cols])

    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Normalize numerical features
    scaler = MinMaxScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    # Encode categorical features
    encoder = LabelEncoder()
    for col in categorical_cols:
        df[col] = encoder.fit_transform(df[col])

    # Split features and target
    X = df[numerical_cols + categorical_cols]
    y = df['class']  # CKD or not

    return X, y

```

** ml/train_catboost.py **
```python

from preprocess import load_and_preprocess
from catboost import CatBoostClassifier
import optuna
import joblib

DATA_PATH = "data/ckd_dataset.csv"
MODEL_PATH = "../model/catboost_model.cbm"

def objective(trial):
    X, y = load_and_preprocess(DATA_PATH)
    model = CatBoostClassifier(
        iterations=trial.suggest_int("iterations", 50, 300),
        depth=trial.suggest_int("depth", 3, 10),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3),
        eval_metric="F1",
        verbose=False
    )
    train_size = int(0.7 * len(X))
    X_train, X_valid = X[:train_size], X[train_size:]
    y_train, y_valid = y[:train_size], y[train_size:]
    model.fit(X_train, y_train, eval_set=(X_valid, y_valid))
    return model.get_best_score()['validation']['F1']

def train_best_model():
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=20)
    best_params = study.best_params
    print("Best Params:", best_params)

    X, y = load_and_preprocess(DATA_PATH)
    model = CatBoostClassifier(**best_params, verbose=False)
    model.fit(X, y)
    model.save_model(MODEL_PATH)

if __name__ == "__main__":
    train_best_model()
```

**  ml/train_xgboost.py ** 

```python

from preprocess import load_and_preprocess
import xgboost as xgb
import optuna
import joblib

DATA_PATH = "data/ckd_dataset.csv"
MODEL_PATH = "../model/xgboost_model.json"

def objective(trial):
    X, y = load_and_preprocess(DATA_PATH)
    dtrain = xgb.DMatrix(X, label=y)
    params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "eta": trial.suggest_float("eta", 0.01, 0.3),
        "max_depth": trial.suggest_int("max_depth", 3, 10)
    }
    res = xgb.cv(params, dtrain, num_boost_round=100, nfold=5, early_stopping_rounds=10)
    return res["test-logloss-mean"].min()

def train_best_model():
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=20)
    best_params = study.best_params
    print("Best Params:", best_params)

    X, y = load_and_preprocess(DATA_PATH)
    model = xgb.XGBClassifier(**best_params)
    model.fit(X, y)
    model.save_model(MODEL_PATH)

if __name__ == "__main__":
    train_best_model()
```

**  ml/evaluation.ipynb **

```python

# Evaluation of CKD Models

from preprocess import load_and_preprocess
from catboost import CatBoostClassifier
import xgboost as xgb
from sklearn.metrics import classification_report

# Load data
X, y = load_and_preprocess("data/ckd_dataset.csv")

# CatBoost Evaluation
cat_model = CatBoostClassifier()
cat_model.load_model("../model/catboost_model.cbm")
y_pred_cat = cat_model.predict(X)
print("CatBoost Report:\n", classification_report(y, y_pred_cat))

# XGBoost Evaluation
xgb_model = xgb.XGBClassifier()
xgb_model.load_model("../model/xgboost_model.json")
y_pred_xgb = xgb_model.predict(X)
print("XGBoost Report:\n", classification_report(y, y_pred_xgb))

```
