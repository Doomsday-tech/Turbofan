import pandas as pd
import numpy as np

def add_rolling_features(df: pd.DataFrame, sensors: list, windows: list = [5, 10]) -> pd.DataFrame:
    """
    Adds rolling mean and standard deviation features for specified sensors.
    Strictly groups by engine_id to prevent leakage between engines.
    """
    df_features = df.copy()
    
    for window in windows:
        # Calculate rolling mean
        roll_mean = df_features.groupby('engine_id')[sensors].rolling(window=window, min_periods=1).mean().reset_index(level=0, drop=True)
        roll_mean.columns = [f"{sensor}_mean_{window}" for sensor in sensors]
        
        # Calculate rolling std
        roll_std = df_features.groupby('engine_id')[sensors].rolling(window=window, min_periods=1).std().reset_index(level=0, drop=True)
        roll_std.columns = [f"{sensor}_std_{window}" for sensor in sensors]
        
        # Fill NaN in std with 0 (happens when min_periods=1 and there is only 1 observation)
        roll_std = roll_std.fillna(0)
        
        # Concatenate features
        df_features = pd.concat([df_features, roll_mean, roll_std], axis=1)
        
    return df_features

def get_constant_sensors(df: pd.DataFrame, sensors: list) -> list:
    """
    Identifies sensors with zero variance in the training set.
    """
    return [sensor for sensor in sensors if df[sensor].std() == 0]
