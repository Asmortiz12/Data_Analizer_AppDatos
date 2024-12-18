import numpy as np
import pandas as pd

def calculate_ohlc(df):
    # Convert dates to datetime
    df['STT_DATE'] = pd.to_datetime(df['STT_DATE'])
    
    # Group by date and calculate OHLC using arrays
    daily_data = df.groupby('STT_DATE').agg({
        'STT_PRICE': ['first', 'max', 'min', 'last'],
        'STT_NUM_SHARES': 'sum'
    }).reset_index()
    
    # Rename columns
    daily_data.columns = ['STT_DATE', 'Open', 'High', 'Low', 'Close', 'Volume']
    return daily_data

def calculate_macd(df):
    # Use numpy arrays for calculations
    prices = np.array(df['Close'])
    
    # Calculate EMAs
    ema12 = pd.Series(prices).ewm(span=12, adjust=False).mean()
    ema26 = pd.Series(prices).ewm(span=26, adjust=False).mean()
    
    df['MACD'] = ema12 - ema26
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    return df

def calculate_rsi(df, periods=14):
    close_delta = df['Close'].diff()
    
    # Create arrays for gains and losses
    gains = np.where(close_delta > 0, close_delta, 0)
    losses = np.where(close_delta < 0, -close_delta, 0)
    
    # Calculate averages
    avg_gain = pd.Series(gains).rolling(window=periods).mean()
    avg_loss = pd.Series(losses).rolling(window=periods).mean()
    
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def calculate_sma(df):
    # Calculate SMAs using arrays
    close_prices = np.array(df['Close'])
    df['SMA_100'] = pd.Series(close_prices).rolling(window=100).mean()
    df['SMA_200'] = pd.Series(close_prices).rolling(window=200).mean()
    df['SMA_300'] = pd.Series(close_prices).rolling(window=300).mean()
    
    return df 
def calculate_general_summary(df):
    df = df.copy()
    df['STT_DATE'] = pd.to_datetime(df['STT_DATE'])
    
    one_month_ago = pd.Timestamp.now() - pd.DateOffset(months=1)
    last_month_data = df[df['STT_DATE'] >= one_month_ago]
    
    summary = {
        'total_transactions': len(last_month_data),
        'total_shares': np.sum(last_month_data['STT_NUM_SHARES'].values),
        'total_value': np.sum(last_month_data['STT_CASH_VALUE'].values),
        'average_price': np.mean(last_month_data['STT_PRICE'].values) if not last_month_data.empty else 0,
        'max_price': np.max(last_month_data['STT_PRICE'].values) if not last_month_data.empty else 0,
        'min_price': np.min(last_month_data['STT_PRICE'].values) if not last_month_data.empty else 0
    }
    
    return summary
