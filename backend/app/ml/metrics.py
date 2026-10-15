import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

def nasa_asymmetric_score(y_true, y_pred):
    """
    Calculates the NASA asymmetric scoring function.
    Penalizes over-prediction (predicting RUL > actual) more heavily than under-prediction.
    """
    # Ensure inputs are numpy arrays
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    d = y_pred - y_true
    
    # Apply asymmetric penalty
    # d < 0 (early prediction): exp(-d / 13) - 1
    # d >= 0 (late prediction): exp(d / 10) - 1
    scores = np.where(d < 0, np.exp(-d / 13) - 1, np.exp(d / 10) - 1)
    
    return np.sum(scores)

def get_all_metrics(y_true, y_pred):
    return {
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mae': mean_absolute_error(y_true, y_pred),
        'nasa_score': nasa_asymmetric_score(y_true, y_pred)
    }
