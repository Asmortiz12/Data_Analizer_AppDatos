# calculations.py
import pandas as pd
from decimal import Decimal

def calculate_ohlc(df):
    df['STT_DATE'] = pd.to_datetime(df['STT_DATE'])
    df['STT_PRICE'] = pd.to_numeric(df['STT_PRICE'], errors='coerce')
    df['STT_NUM_SHARES'] = pd.to_numeric(df['STT_NUM_SHARES'], errors='coerce')
    ohlc_df = df.groupby(df['STT_DATE'].dt.date).agg({
        'STT_PRICE': ['first', 'max', 'min', 'last'],
        'STT_NUM_SHARES': 'sum'
    }).reset_index()
    ohlc_df.columns = ['STT_DATE', 'Open', 'High', 'Low', 'Close', 'Volume']
    return ohlc_df

def calculate_macd(ohlc_df):
    ohlc_df['EMA_12'] = ohlc_df['Close'].ewm(span=12, adjust=False).mean()
    ohlc_df['EMA_26'] = ohlc_df['Close'].ewm(span=26, adjust=False).mean()
    ohlc_df['MACD'] = ohlc_df['EMA_12'] - ohlc_df['EMA_26']
    ohlc_df['Signal_Line'] = ohlc_df['MACD'].ewm(span=9, adjust=False).mean()
    return ohlc_df

def calculate_rsi(ohlc_df):
    delta = ohlc_df['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    rs = avg_gain / avg_loss
    ohlc_df['RSI'] = 100 - (100 / (1 + rs))
    return ohlc_df

def calculate_sma(ohlc_df):
    ohlc_df['SMA_100'] = ohlc_df['Close'].rolling(window=100).mean()
    ohlc_df['SMA_200'] = ohlc_df['Close'].rolling(window=200).mean()
    ohlc_df['SMA_300'] = ohlc_df['Close'].rolling(window=300).mean()
    return ohlc_df

def calculate_general_summary(df):
    df['STT_DATE'] = pd.to_datetime(df['STT_DATE'])  # Asegurarse de que las fechas sean tipo Timestamp
    one_month_ago = pd.Timestamp.today() - pd.DateOffset(months=1)
    last_month = df[df['STT_DATE'] >= one_month_ago]

    summary = {
        'total_transactions': len(last_month),
        'total_shares': last_month['STT_NUM_SHARES'].sum(),
        'total_value': last_month['STT_CASH_VALUE'].sum()
    }
    return summary