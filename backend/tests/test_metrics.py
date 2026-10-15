import numpy as np
import pytest
from app.ml.metrics import nasa_asymmetric_score

def test_nasa_asymmetric_score_underpredict():
    # Predict 10, Actual 23. d = -13
    # Formula: exp(-(-13)/13) - 1 = exp(1) - 1 approx 1.718
    y_true = [23]
    y_pred = [10]
    score = nasa_asymmetric_score(y_true, y_pred)
    expected = np.exp(1) - 1
    assert np.isclose(score, expected)

def test_nasa_asymmetric_score_overpredict():
    # Predict 30, Actual 20. d = 10
    # Formula: exp(10/10) - 1 = exp(1) - 1 approx 1.718
    y_true = [20]
    y_pred = [30]
    score = nasa_asymmetric_score(y_true, y_pred)
    expected = np.exp(1) - 1
    assert np.isclose(score, expected)
