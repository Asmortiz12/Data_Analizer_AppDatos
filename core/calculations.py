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

def calculate_macd(ohlc_df):
    close_prices = ohlc_df['Close'].values
    ema_12 = pd.Series(close_prices).ewm(span=12, adjust=False).mean()
    ema_26 = pd.Series(close_prices).ewm(span=26, adjust=False).mean()
    
    ohlc_df['EMA_12'] = ema_12
    ohlc_df['EMA_26'] = ema_26
    ohlc_df['MACD'] = ohlc_df['EMA_12'] - ohlc_df['EMA_26']
    ohlc_df['Signal_Line'] = ohlc_df['MACD'].ewm(span=9, adjust=False).mean()
    
    return ohlc_df

def calculate_rsi(ohlc_df, periods=14):
    close_prices = ohlc_df['Close'].values
    deltas = np.diff(close_prices, prepend=close_prices[0])
    
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gains = pd.Series(gains).rolling(window=periods, min_periods=1).mean()
    avg_losses = pd.Series(losses).rolling(window=periods, min_periods=1).mean()
    
    rs = avg_gains / avg_losses
    ohlc_df['RSI'] = 100 - (100 / (1 + rs))
    
    return ohlc_df

def calculate_sma(ohlc_df):
    close_prices = ohlc_df['Close'].values
    
    for period in [100, 200, 300]:
        sma = pd.Series(close_prices).rolling(window=period).mean()
        ohlc_df[f'SMA_{period}'] = sma
    
    return ohlc_df

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
