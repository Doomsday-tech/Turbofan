from flask import Blueprint, request, jsonify
import joblib
import os
import pandas as pd
from datetime import datetime
from app.ml.feature_engineering import add_rolling_features
from app.ml.preprocessing import transform_scalers
from app.ml.data_loader import load_cmapss_data

api_bp = Blueprint('api', __name__, url_prefix='/api')

MODEL_ARTIFACT = None
RUL_THRESHOLD = 30
DATA_CACHE = {'train': None, 'test': None, 'rul': None}

def load_artifact():
    global MODEL_ARTIFACT
    if MODEL_ARTIFACT is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        path = os.path.join(base_dir, 'app', 'models', 'rul_model.joblib')
        if os.path.exists(path):
            MODEL_ARTIFACT = joblib.load(path)
    return MODEL_ARTIFACT

def load_data():
    global DATA_CACHE
    if DATA_CACHE['test'] is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_dir = os.path.join(base_dir, 'data', 'raw')
        try:
            _, test_df, _ = load_cmapss_data(data_dir, subset='FD001')
            DATA_CACHE['test'] = test_df
        except Exception:
            pass
    return DATA_CACHE['test']

@api_bp.route('/health', methods=['GET'])
def health_check():
    artifact = load_artifact()
    return jsonify({
        'status': 'online',
        'model_loaded': artifact is not None,
        'timestamp': datetime.utcnow().isoformat()
    })

@api_bp.route('/summary', methods=['GET'])
def summary():
    artifact = load_artifact()
    if not artifact:
        return jsonify({'error': 'Model not trained'}), 404
    return jsonify({
        'metadata': artifact['metadata'],
        'metrics': artifact['metrics'],
        'threshold': RUL_THRESHOLD
    })

@api_bp.route('/engines', methods=['GET'])
def get_engines():
    test_df = load_data()
    if test_df is None:
        return jsonify({'error': 'Dataset not found'}), 404
    
    engines = test_df.groupby('engine_id')['cycle'].max().reset_index()
    return jsonify(engines.to_dict('records'))

@api_bp.route('/engines/<int:engine_id>/history', methods=['GET'])
def get_engine_history(engine_id):
    test_df = load_data()
    if test_df is None:
        return jsonify({'error': 'Dataset not found'}), 404
        
    engine_data = test_df[test_df['engine_id'] == engine_id]
    if engine_data.empty:
        return jsonify({'error': 'Engine not found'}), 404
        
    return jsonify(engine_data.to_dict('records'))

@api_bp.route('/predict', methods=['POST'])
def predict():
    artifact = load_artifact()
    if not artifact:
        return jsonify({'error': 'Model not loaded'}), 503
        
    data = request.json
    if not data or 'history' not in data:
        return jsonify({'error': 'Invalid payload, missing history array'}), 400
        
    df = pd.DataFrame(data['history'])
    
    sensor_cols = [f'sensor_{i}' for i in range(1, 22)]
    df = add_rolling_features(df, sensors=sensor_cols, windows=[5, 10])
    df = transform_scalers(df, artifact['scaler'], artifact['features'])
    
    last_cycle = df.iloc[-1:]
    X = last_cycle[artifact['features']]
    pred_rul = float(artifact['model'].predict(X)[0])
    
    if pred_rul <= 10:
        status, risk = 'Critical', 'danger'
    elif pred_rul <= RUL_THRESHOLD:
        status, risk = 'Warning', 'warning'
    else:
        status, risk = 'Normal', 'success'
        
    return jsonify({
        'predicted_rul': round(pred_rul, 2),
        'model': artifact['metadata']['model_name'],
        'alert_status': status,
        'risk_category': risk,
        'threshold': RUL_THRESHOLD,
        'timestamp': datetime.utcnow().isoformat()
    })

@api_bp.route('/settings/threshold', methods=['POST'])
def update_threshold():
    global RUL_THRESHOLD
    data = request.json
    if 'threshold' in data and isinstance(data['threshold'], (int, float)):
        RUL_THRESHOLD = data['threshold']
        return jsonify({'message': 'Threshold updated', 'threshold': RUL_THRESHOLD})
    return jsonify({'error': 'Invalid threshold value'}), 400
