import pandas as pd
import os
from typing import Tuple

COLUMN_NAMES = ['engine_id', 'cycle', 'op_setting_1', 'op_setting_2', 'op_setting_3'] + \
               [f'sensor_{i}' for i in range(1, 22)]

def load_cmapss_data(data_dir: str, subset: str = 'FD001') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_path = os.path.join(data_dir, f'train_{subset}.txt')
    test_path = os.path.join(data_dir, f'test_{subset}.txt')
    rul_path = os.path.join(data_dir, f'RUL_{subset}.txt')
    
    for path in [train_path, test_path, rul_path]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing dataset file: {path}")
            
    train_df = pd.read_csv(train_path, sep=r'\s+', header=None, usecols=range(26), names=COLUMN_NAMES)
    test_df = pd.read_csv(test_path, sep=r'\s+', header=None, usecols=range(26), names=COLUMN_NAMES)
    
    rul_df = pd.read_csv(rul_path, sep=r'\s+', header=None, names=['RUL_truth'])
    rul_df['engine_id'] = rul_df.index + 1
        
    train_df = train_df.sort_values(['engine_id', 'cycle']).reset_index(drop=True)
    test_df = test_df.sort_values(['engine_id', 'cycle']).reset_index(drop=True)
    
    return train_df, test_df, rul_df
