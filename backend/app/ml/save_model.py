import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from app.ml.data_loader import load_cmapss_data
from app.ml.preprocessing import generate_rul_labels, fit_transform_scalers, transform_scalers
from app.ml.feature_engineering import add_rolling_features, get_constant_sensors
from app.ml.metrics import get_all_metrics

def train_and_save_model():
    print("Loading data...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(base_dir, 'data', 'raw')
    train_df, test_df, rul_df = load_cmapss_data(data_dir, subset='FD001')
    
    # Preprocess training data
    train_df = generate_rul_labels(train_df, clip_cap=125)
    sensor_cols = [f'sensor_{i}' for i in range(1, 22)]
    train_df = add_rolling_features(train_df, sensors=sensor_cols, windows=[5, 10])
    
    constant_sensors = get_constant_sensors(train_df, sensor_cols)
    features = [col for col in train_df.columns if col not in ['engine_id', 'cycle', 'RUL', 'RUL_clipped'] + constant_sensors]
    
    train_df, scaler = fit_transform_scalers(train_df, features)
    
    print("Training final Gradient Boosting model...")
    model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
    model.fit(train_df[features], train_df['RUL_clipped'])
    
    # Preprocess test data
    print("Evaluating on official test set...")
    test_df = add_rolling_features(test_df, sensors=sensor_cols, windows=[5, 10])
    test_df = transform_scalers(test_df, scaler, features)
    
    # Extract the last cycle for each test engine
    test_last_cycle = test_df.groupby('engine_id').last().reset_index()
    X_test = test_last_cycle[features]
    y_true = rul_df['RUL_truth'].values
    
    y_pred = model.predict(X_test)
    metrics = get_all_metrics(y_true, y_pred)
    print(f"Test Metrics: RMSE={metrics['rmse']:.2f}, NASA Score={metrics['nasa_score']:.2f}, MAE={metrics['mae']:.2f}")
    
    print("Calculating permutation importance...")
    importance = permutation_importance(model, X_test, y_true, n_repeats=10, random_state=42)
    imp_df = pd.DataFrame({'feature': features, 'importance': importance.importances_mean})
    imp_df = imp_df.sort_values(by='importance', ascending=False).head(10)
    
    # Package artifact
    artifact = {
        'model': model,
        'scaler': scaler,
        'features': features,
        'constant_sensors': constant_sensors,
        'clip_cap': 125,
        'metrics': metrics,
        'importance': imp_df.to_dict('records'),
        'metadata': {
            'model_name': 'Gradient Boosting Regressor',
            'dataset': 'FD001',
            'engines_evaluated': len(y_true)
        }
    }
    
    model_path = os.path.join(base_dir, 'app', 'models', 'rul_model.joblib')
    joblib.dump(artifact, model_path)
    print(f"Model artifact saved to {model_path}")

if __name__ == '__main__':
    train_and_save_model()
