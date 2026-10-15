import pandas as pd
import numpy as np

def generate_rul_labels(df: pd.DataFrame, clip_cap: int = 125) -> pd.DataFrame:
    """
    Calculates the RUL for each engine cycle and applies a clipping cap.
    Assumes data is sorted by engine_id and cycle.
    """
    df = df.copy()
    
    # Calculate max cycle for each engine
    max_cycles = df.groupby('engine_id')['cycle'].max().reset_index()
    max_cycles.columns = ['engine_id', 'max_cycle']
    
    # Merge back to calculate RUL
    df = df.merge(max_cycles, on=['engine_id'], how='left')
    df['RUL'] = df['max_cycle'] - df['cycle']
    
    # Apply clipping
    df['RUL_clipped'] = df['RUL'].clip(upper=clip_cap)
    
    # Drop intermediate max_cycle column
    df = df.drop(columns=['max_cycle'])
    
    return df

def fit_transform_scalers(train_df: pd.DataFrame, features: list):
    """
    Fits a scaler on training data and transforms it. 
    Returns the scaled dataframe and the scaler object.
    """
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    
    train_scaled = train_df.copy()
    train_scaled[features] = scaler.fit_transform(train_df[features])
    
    return train_scaled, scaler

def transform_scalers(df: pd.DataFrame, scaler, features: list):
    """
    Applies a pre-fitted scaler to validation or test data.
    """
    df_scaled = df.copy()
    df_scaled[features] = scaler.transform(df[features])
    return df_scaled
