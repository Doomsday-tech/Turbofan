import pandas as pd
import numpy as np
import pytest
from app.ml.preprocessing import generate_rul_labels
from app.ml.feature_engineering import add_rolling_features

def test_generate_rul_labels():
    # Mock data: Engine 1 has 3 cycles, Engine 2 has 2 cycles
    data = {
        'engine_id': [1, 1, 1, 2, 2],
        'cycle': [1, 2, 3, 1, 2]
    }
    df = pd.DataFrame(data)
    
    result = generate_rul_labels(df, clip_cap=1)
    
    # Check uncapped RUL
    assert result['RUL'].tolist() == [2, 1, 0, 1, 0]
    
    # Check clipped RUL (capped at 1)
    assert result['RUL_clipped'].tolist() == [1, 1, 0, 1, 0]

def test_leakage_in_rolling_features():
    # Mock data: Engine 2 starts with a drastic change in sensor value
    data = {
        'engine_id': [1, 1, 1, 2, 2],
        'cycle': [1, 2, 3, 1, 2],
        'sensor_1': [10, 10, 10, 100, 100] 
    }
    df = pd.DataFrame(data)
    
    # Window of 3
    result = add_rolling_features(df, sensors=['sensor_1'], windows=[3])
    
    # The rolling mean for engine 2, cycle 1 should be EXACTLY 100.
    # If it leaked, it would average the end of engine 1 (10) with engine 2 (100).
    engine_2_cycle_1_mean = result[(result['engine_id'] == 2) & (result['cycle'] == 1)]['sensor_1_mean_3'].values[0]
    
    assert engine_2_cycle_1_mean == 100.0, "Data leakage detected: Engine 2 rolling features are contaminated by Engine 1"
