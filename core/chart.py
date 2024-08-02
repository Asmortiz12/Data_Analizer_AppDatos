
import plotly.graph_objects as go
from plotly.offline import plot

def generate_candlestick_chart(ohlc_df):
    candlestick = go.Candlestick(
        x=ohlc_df['STT_DATE'],
        open=ohlc_df['Open'],
        high=ohlc_df['High'],
        low=ohlc_df['Low'],
        close=ohlc_df['Close']
    )
    guide_line = go.Scatter(
        x=ohlc_df['STT_DATE'],
        y=ohlc_df['Close'],
        name='Línea Guía',
        line=dict(color='#131341', dash='dot', width=2),
    )
    candlestick_fig = go.Figure(data=[candlestick, guide_line])
    candlestick_fig.update_layout(
        autosize=True,
        width=1400,
        height=400
    )
    return plot(candlestick_fig, output_type='div')

def generate_macd_chart(ohlc_df):
    macd_line = go.Scatter(
        x=ohlc_df['STT_DATE'], y=ohlc_df['MACD'], name='MACD', line=dict(color='blue'))
    signal_line = go.Scatter(
        x=ohlc_df['STT_DATE'], y=ohlc_df['Signal_Line'], name='Línea de Señal', line=dict(color='red'))
    macd_chart = go.Figure(data=[macd_line, signal_line])
    macd_chart.update_layout(
        autosize=True,
        width=1400,
        height=400
    )
    return plot(macd_chart, output_type='div')

def generate_rsi_chart(ohlc_df):
    rsi_chart = go.Scatter(
        x=ohlc_df['STT_DATE'], y=ohlc_df['RSI'], name='RSI', line=dict(color='purple'))
    rsi_fig = go.Figure(data=[rsi_chart])
    rsi_fig.update_layout(
        autosize=True,
        width=1400,
        height=400
    )
    return plot(rsi_fig, output_type='div')

def generate_sma_chart(ohlc_df):
    sma_100 = go.Scatter(x=ohlc_df['STT_DATE'], y=ohlc_df['SMA_100'],
                         name='SMA 100', line=dict(color='orange'))
    sma_200 = go.Scatter(x=ohlc_df['STT_DATE'], y=ohlc_df['SMA_200'],
                         name='SMA 200', line=dict(color='green'))
    sma_300 = go.Scatter(x=ohlc_df['STT_DATE'], y=ohlc_df['SMA_300'],
                         name='SMA 300', line=dict(color='red'))
    sma_fig = go.Figure(data=[sma_100, sma_200, sma_300])
    sma_fig.update_layout(
        autosize=True,
        width=1400,
        height=400
    )
    return plot(sma_fig, output_type='div')

def generate_volume_chart(ohlc_df):
    volume_bar = go.Bar(x=ohlc_df['STT_DATE'],
                        y=ohlc_df['Volume'], name='Volumen', marker=dict(color='#6c3875'))
    volume_fig = go.Figure(data=[volume_bar])
    volume_fig.update_layout(
        autosize=True,
        width=1400,
        height=400
    )
    return plot(volume_fig, output_type='div')

def generate_projection_chart(projected_dates, projected_cash_flows):
    projection_chart = go.Scatter(
        x=projected_dates,
        y=projected_cash_flows,
        name='Proyecciones de Precios',
        line=dict(color='blue', dash='dash')
    )
    projection_fig = go.Figure(data=[projection_chart])
    projection_fig.update_layout(
        autosize=True,
        width=1400,
        height=400
    )
    return plot(projection_fig, output_type='div')

