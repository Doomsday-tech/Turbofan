import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GroupKFold
from app.ml.data_loader import load_cmapss_data
from app.ml.preprocessing import generate_rul_labels, fit_transform_scalers, transform_scalers
from app.ml.feature_engineering import add_rolling_features, get_constant_sensors
from app.ml.metrics import get_all_metrics

def train_and_evaluate():
    print("Loading dataset...")
    data_dir = os.path.join(os.path.dirname(__file__), '../../data/raw')
    train_df, test_df, rul_df = load_cmapss_data(data_dir, subset='FD001')
    
    print("Generating labels and features...")
    train_df = generate_rul_labels(train_df, clip_cap=125)
    
    sensor_cols = [f'sensor_{i}' for i in range(1, 22)]
    
    # Add rolling features
    train_df = add_rolling_features(train_df, sensors=sensor_cols, windows=[5, 10])
    
    # Identify and drop constant sensors
    constant_sensors = get_constant_sensors(train_df, sensor_cols)
    print(f"Dropping constant sensors: {constant_sensors}")
    
    # Define features to use
    features = [col for col in train_df.columns if col not in ['engine_id', 'cycle', 'RUL', 'RUL_clipped'] + constant_sensors]
    
    # Scale features
    train_df, scaler = fit_transform_scalers(train_df, features)
    
    # Define Models
    models = {
        'Baseline (Mean RUL)': None, 
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=50, max_depth=5, random_state=42)
    }
    
    gkf = GroupKFold(n_splits=3)
    results = {name: {'rmse': [], 'nasa_score': []} for name in models.keys()}
    
    X = train_df[features]
    y = train_df['RUL_clipped']
    groups = train_df['engine_id']
    
    print("Running GroupKFold Cross-Validation...")
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups)):
        X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]
        
        for name, model in models.items():
            if model is None:
                # Baseline predicts the mean RUL of the training fold
                preds = np.full(len(y_val), y_train.mean())
            else:
                model.fit(X_train, y_train)
                preds = model.predict(X_val)
                
            metrics = get_all_metrics(y_val, preds)
            results[name]['rmse'].append(metrics['rmse'])
            results[name]['nasa_score'].append(metrics['nasa_score'])
            
    print("\n--- Cross-Validation Results ---")
    for name in results.keys():
        mean_rmse = np.mean(results[name]['rmse'])
        mean_nasa = np.mean(results[name]['nasa_score'])
        print(f"{name:20s} | RMSE: {mean_rmse:.2f} | NASA Score: {mean_nasa:.2f}")

if __name__ == '__main__':
    train_and_evaluate()
