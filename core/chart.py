import plotly.graph_objects as go
from plotly.offline import plot

def get_responsive_layout(title="", height=None):
    return dict(
        template="plotly_dark",
        autosize=True,
        height=450,  # Reduced height further
        margin=dict(l=20, r=20, t=20, b=20, pad=5),
        paper_bgcolor='#2c3e50',
        plot_bgcolor='#34495e',
        hovermode='x unified',
        hoverdistance=100,
        hoverlabel=dict(
            bgcolor='rgba(44, 62, 80, 0.95)',
            bordercolor='white',
            font=dict(size=12, color='white', family="Roboto, sans-serif")
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            showspikes=True,
            spikesnap="cursor",
            spikemode="across",
            spikecolor="white",
            spikethickness=1,
            spikedash="dot",
            automargin=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            showspikes=True,
            spikecolor="white",
            spikethickness=1,
            spikedash="dot",
            automargin=True
        )
    )

def generate_candlestick_chart(ohlc_df):
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=ohlc_df['STT_DATE'],
        open=ohlc_df['Open'],
        high=ohlc_df['High'],
        low=ohlc_df['Low'],
        close=ohlc_df['Close'],
        increasing_line_color='#00c853',
        decreasing_line_color='#ff3d00',
        name='Price'
    ))
    
    # Guide line connecting closing prices
    fig.add_trace(go.Scatter(
        x=ohlc_df['STT_DATE'],
        y=ohlc_df['Close'],
        name='Trend Line',
        line=dict(color='rgba(255, 255, 255, 0.8)', width=1.5, dash='dot'),
        opacity=0.8
    ))
    
    fig.update_layout(**get_responsive_layout())
    
    return plot(fig, output_type='div', include_plotlyjs=True, config={
        'responsive': True,
        'displayModeBar': True,
        'scrollZoom': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'autosizable': True
    })

def generate_macd_chart(ohlc_df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ohlc_df['STT_DATE'],
        y=ohlc_df['MACD'],
        name='MACD',
        line=dict(color='#2196f3', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=ohlc_df['STT_DATE'],
        y=ohlc_df['Signal_Line'],
        name='Signal Line',
        line=dict(color='#ff9800', width=2)
    ))
    
    fig.update_layout(**get_responsive_layout("MACD Analysis"))
    return plot(fig, output_type='div', config={'responsive': True})

def generate_rsi_chart(ohlc_df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ohlc_df['STT_DATE'],
        y=ohlc_df['RSI'],
        name='RSI',
        line=dict(color='#673ab7', width=2)
    ))
    
    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5)
    
    fig.update_layout(**get_responsive_layout("RSI Analysis"))
    return plot(fig, output_type='div', config={'responsive': True})

def generate_volume_chart(ohlc_df):
    colors = ['#00c853' if close >= open_ else '#ff3d00' 
              for close, open_ in zip(ohlc_df['Close'], ohlc_df['Open'])]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ohlc_df['STT_DATE'],
        y=ohlc_df['Volume'],
        marker=dict(color=colors, opacity=0.8),
        name='Volume'
    ))
    
    fig.update_layout(**get_responsive_layout("Trading Volume"))
    return plot(fig, output_type='div', config={'responsive': True})

def generate_sma_chart(ohlc_df):
    fig = go.Figure()
    
    for period in [100, 200, 300]:
        fig.add_trace(go.Scatter(
            x=ohlc_df['STT_DATE'],
            y=ohlc_df[f'SMA_{period}'],
            name=f'SMA {period}',
            line=dict(width=2)
        ))
    
    fig.update_layout(**get_responsive_layout("Moving Averages"))
    return plot(fig, output_type='div', config={'responsive': True})

def generate_projection_chart(projected_dates, projected_values):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=projected_dates,
        y=projected_values,
        name='Price Projection',
        line=dict(color='#2196f3', dash='dash', width=2)
    ))
    
    fig.update_layout(**get_responsive_layout("Price Projections"))
    return plot(fig, output_type='div', config={'responsive': True})
