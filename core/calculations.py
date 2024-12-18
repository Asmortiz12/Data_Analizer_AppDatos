import pandas as pd
import numpy as np

def calculate_ohlc(df):
    df = df.copy()
    df['STT_DATE'] = pd.to_datetime(df['STT_DATE'])
    
    # Process daily OHLCV data
    daily_data = pd.DataFrame({
        'Open': df.groupby(df['STT_DATE'].dt.date)['STT_PRICE'].first(),
        'High': df.groupby(df['STT_DATE'].dt.date)['STT_PRICE'].max(),
        'Low': df.groupby(df['STT_DATE'].dt.date)['STT_PRICE'].min(),
        'Close': df.groupby(df['STT_DATE'].dt.date)['STT_PRICE'].last(),
        'Volume': df.groupby(df['STT_DATE'].dt.date)['STT_NUM_SHARES'].sum()
    }).reset_index()
    
    daily_data.rename(columns={'index': 'STT_DATE'}, inplace=True)
    return daily_data

def calculate_macd(df):
    # Use numpy arrays instead of matrix
    prices = np.array(df['Close'])
    
    # Calculate EMAs using arrays
    ema12 = pd.Series(prices).ewm(span=12, adjust=False).mean()
    ema26 = pd.Series(prices).ewm(span=26, adjust=False).mean()
    
    # Calculate MACD line
    df['MACD'] = ema12 - ema26
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    return df

def calculate_rsi(df, periods=14):
    # Calculate using numpy arrays
    close_delta = df['Close'].diff()
    
    # Separate gains and losses
    gains = close_delta.copy()
    losses = close_delta.copy()
    
    gains[gains < 0] = 0
    losses[losses > 0] = 0
    
    # Calculate RSI
    avg_gain = gains.rolling(window=periods).mean()
    avg_loss = abs(losses.rolling(window=periods).mean())
    
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def calculate_sma(df):
    # Calculate SMAs using numpy arrays
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
