import pandas as pd
import numpy as np
from decimal import Decimal

def calculate_ohlc(df):
    df = df.copy()
    df['STT_DATE'] = pd.to_datetime(df['STT_DATE'])
    
    # Use a simpler aggregation structure
    ohlc_df = df.groupby(df['STT_DATE'].dt.date).agg(
        Open=('STT_PRICE', 'first'),
        High=('STT_PRICE', 'max'),
        Low=('STT_PRICE', 'min'),
        Close=('STT_PRICE', 'last'),
        Volume=('STT_NUM_SHARES', 'sum')
    ).reset_index()
    
    return ohlc_df

def calculate_macd(ohlc_df):
    # Calculate MACD components
    close_prices = ohlc_df['Close'].values
    ema_12 = pd.Series(close_prices).ewm(span=12, adjust=False).mean()
    ema_26 = pd.Series(close_prices).ewm(span=26, adjust=False).mean()
    
    ohlc_df['EMA_12'] = ema_12
    ohlc_df['EMA_26'] = ema_26
    ohlc_df['MACD'] = ohlc_df['EMA_12'] - ohlc_df['EMA_26']
    ohlc_df['Signal_Line'] = ohlc_df['MACD'].ewm(span=9, adjust=False).mean()
    
    return ohlc_df

def calculate_rsi(ohlc_df, periods=14):
    # Calculate price changes
    delta = ohlc_df['Close'].diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=periods, min_periods=1).mean()
    avg_losses = losses.rolling(window=periods, min_periods=1).mean()
    
    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    ohlc_df['RSI'] = 100 - (100 / (1 + rs))
    
    return ohlc_df

def calculate_sma(ohlc_df):
    # Calculate multiple SMAs using numpy for better performance
    close_prices = ohlc_df['Close'].values
    
    for period in [100, 200, 300]:
        sma = pd.Series(close_prices).rolling(window=period).mean()
        ohlc_df[f'SMA_{period}'] = sma
    
    return ohlc_df

def calculate_general_summary(df):
    # Ensure proper data types
    df = df.copy()
    df['STT_DATE'] = pd.to_datetime(df['STT_DATE'])
    df['STT_NUM_SHARES'] = pd.to_numeric(df['STT_NUM_SHARES'], errors='coerce')
    df['STT_CASH_VALUE'] = pd.to_numeric(df['STT_CASH_VALUE'], errors='coerce')
    
    # Calculate last month's data
    one_month_ago = pd.Timestamp.now() - pd.DateOffset(months=1)
    last_month_data = df[df['STT_DATE'] >= one_month_ago]
    
    summary = {
        'total_transactions': len(last_month_data),
        'total_shares': last_month_data['STT_NUM_SHARES'].sum(),
        'total_value': last_month_data['STT_CASH_VALUE'].sum(),
        'average_price': last_month_data['STT_CASH_VALUE'].mean() if len(last_month_data) > 0 else 0,
        'max_price': last_month_data['STT_CASH_VALUE'].max() if len(last_month_data) > 0 else 0,
        'min_price': last_month_data['STT_CASH_VALUE'].min() if len(last_month_data) > 0 else 0
    }
    
    return summary
