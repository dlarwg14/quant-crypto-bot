import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

def backtest_zscore(days=30):
    # Historical BTC data (mock for now)
    prices = np.random.normal(100000, 5000, 24*60*days)  # 1-min bars
    returns = np.diff(np.log(prices))
    
    # Z-Score calculation
    window = 20
    z_scores = (returns[-window:] - returns[-window:].mean()) / returns[-window:].std()
    
    # Signals
    signals = np.where(z_scores < -1.5, 1, np.where(z_scores > 1.5, -1, 0))
    print(f"Backtest Results: {signals.sum()} trades, Win Rate: {np.mean(signals)}")
    
backtest_zscore()
