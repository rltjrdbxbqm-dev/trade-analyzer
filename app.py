"""
📊 Trading Strategy Backtest Dashboard
=====================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ═══════════════════════════════════════════════════════════════════════════════
# 페이지 설정
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="📊 Backtest Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 다크모드 호환 CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .highlight-box {
        background: rgba(99, 102, 241, 0.15);
        border-left: 4px solid #6366f1;
        padding: 1rem 1.5rem;
        border-radius: 0 0.5rem 0.5rem 0;
        margin: 1rem 0;
        color: inherit;
    }
    
    .highlight-box h4 {
        color: #818cf8;
        margin-bottom: 0.5rem;
    }
    
    .highlight-box ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .highlight-box li {
        margin-bottom: 0.3rem;
    }
    
    .warning-box {
        background: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        padding: 1rem 1.5rem;
        border-radius: 0 0.5rem 0.5rem 0;
        margin: 1rem 0;
        color: inherit;
    }
    
    .warning-box h4 {
        color: #f87171;
        margin-bottom: 0.5rem;
    }
    
    .warning-box ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .warning-box li {
        margin-bottom: 0.3rem;
    }
    
    .success-box {
        background: rgba(34, 197, 94, 0.15);
        border-left: 4px solid #22c55e;
        padding: 1rem 1.5rem;
        border-radius: 0 0.5rem 0.5rem 0;
        margin: 1rem 0;
        color: inherit;
    }
    
    .success-box h4 {
        color: #4ade80;
        margin-bottom: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(100, 100, 100, 0.1);
        padding: 0.5rem;
        border-radius: 0.75rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 700;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 0.875rem;
    }
    
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 데이터 로드 - 전체 37개 자산
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    """백테스트 결과 데이터 - 전체 37개 자산"""
    data = {
        'Strategy': [
            'TQQQ Sniper',
            'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit',
            'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit',
            'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit',
            'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit',
            'Bitget Futures', 'Bitget Futures', 'Bitget Futures', 'Bitget Futures'
        ],
        'Ticker': [
            'TQQQ',
            'KRW-BONK', 'KRW-UNI', 'KRW-SUI', 'KRW-MNT', 'KRW-MOVE', 'KRW-AKT', 'KRW-IMX', 'KRW-ARB',
            'KRW-VET', 'KRW-SAND', 'KRW-HBAR', 'KRW-GRT', 'KRW-AVAX', 'KRW-NEAR', 'KRW-SOL', 'KRW-THETA',
            'KRW-MANA', 'KRW-XRP', 'KRW-ANKR', 'KRW-ADA', 'KRW-POL', 'KRW-CRO', 'KRW-DOT', 'KRW-MVL',
            'KRW-ETH', 'KRW-WAXP', 'KRW-DOGE', 'KRW-XLM', 'KRW-LINK', 'KRW-AXS', 'KRW-BTC', 'KRW-BCH',
            'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'SUIUSDT'
        ],
        'CAGR': [
            26.65,
            1225.53, 1274.97, 540.26, 549.67, 470.54, 219.14, 264.82, 238.12,
            223.26, 229.50, 209.28, 208.65, 216.14, 187.47, 181.14, 159.82,
            169.52, 173.31, 159.05, 170.85, 178.98, 155.29, 132.68, 154.95,
            140.52, 124.63, 101.08, 127.94, 118.04, 105.48, 101.66, 69.32,
            417.06, 657.60, 1911.81, 1162.43
        ],
        'MDD': [
            -38.39,
            -24.51, -19.54, -46.10, -37.59, -29.63, -21.08, -28.16, -28.60,
            -59.31, -62.15, -57.38, -35.01, -33.18, -51.73, -27.58, -59.23,
            -63.16, -69.08, -60.64, -51.46, -32.79, -49.15, -54.32, -52.96,
            -27.78, -65.15, -59.66, -59.56, -47.56, -45.69, -32.75, -51.92,
            -63.21, -67.84, -74.39, -62.94
        ],
        'Sharpe': [
            0.85,
            3.87, 3.43, 2.75, 2.68, 2.55, 2.10, 2.14, 2.17,
            1.90, 1.69, 1.69, 2.02, 2.16, 1.82, 2.16, 1.57,
            1.36, 1.56, 1.44, 1.85, 1.93, 1.58, 1.66, 1.50,
            2.10, 1.05, 1.35, 1.44, 1.49, 1.25, 2.10, 1.10,
            2.00, 2.11, 2.54, 2.22
        ],
        'WinRate': [
            44.2,
            22.7, 26.7, 25.4, 22.9, 16.5, 16.5, 22.5, 19.4,
            22.2, 20.9, 21.2, 20.4, 25.5, 21.9, 18.4, 18.9,
            19.4, 18.0, 20.4, 20.9, 20.9, 18.1, 20.2, 17.7,
            19.2, 15.6, 20.8, 15.6, 21.8, 14.1, 23.5, 17.4,
            21.2, 20.0, 19.0, 18.1
        ],
        'Years': [
            14.83,
            0.59, 0.48, 2.17, 1.15, 0.65, 1.14, 2.18, 2.25,
            5.31, 4.53, 5.75, 2.21, 3.41, 3.46, 3.64, 6.46,
            6.53, 8.07, 5.95, 7.62, 3.53, 5.04, 4.70, 4.91,
            7.58, 6.68, 4.33, 8.05, 5.00, 4.53, 7.72, 7.99,
            6.08, 5.83, 5.06, 2.30
        ],
        'Trades': [
            688,
            26, 16, 98, 20, 32, 58, 106, 140,
            342, 106, 336, 70, 300, 122, 190, 220,
            276, 394, 238, 284, 268, 238, 263, 122,
            246, 412, 268, 470, 380, 112, 288, 405,
            176, 150, 260, 64
        ],
        'TotalReturn': [
            3220.82,
            361.06, 253.59, 5475.43, 755.64, 209.55, 276.17, 1584.54, 1446.11,
            50931.01, 22032.66, 66065.33, 1113.71, 4956.95, 3752.94, 4199.87, 47562.82,
            64897.01, 335244.62, 28699.96, 199219.50, 3646.93, 11161.46, 5173.49, 9765.73,
            77080.81, 22131.93, 1952.83, 75972.92, 4814.85, 2508.26, 22381.62, 6625.78,
            2172122.17, 13297012.31, 390830189.47, 33748.45
        ]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_yearly_returns():
    """전략별 연도별 수익률 (중앙값 기준)"""
    return pd.DataFrame({
        'Year': ['2020', '2021', '2022', '2023', '2024', '2025'],
        'TQQQ Sniper': [129.2, 64.1, -22.1, 77.6, 49.8, 40.6],
        'Upbit': [567.2, 2060.8, 10.9, 87.8, 116.2, 36.0],
        'Bitget Futures': [4307.2, 1147.9, -17.8, 449.9, 341.7, 79.5],
    })

@st.cache_data
def load_correlation():
    tickers = ['TQQQ', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'SUIUSDT', 'KRW-BTC', 'KRW-ETH', 'KRW-SOL']
    corr = np.array([
        [1.00, 0.11, 0.19, 0.12, 0.06, 0.10, 0.19, 0.13],
        [0.11, 1.00, 0.40, 0.38, 0.24, 0.73, 0.40, 0.34],
        [0.19, 0.40, 1.00, 0.28, 0.21, 0.37, 0.80, 0.29],
        [0.12, 0.38, 0.28, 1.00, 0.15, 0.33, 0.27, 0.84],
        [0.06, 0.24, 0.21, 0.15, 1.00, 0.14, 0.16, 0.21],
        [0.10, 0.73, 0.37, 0.33, 0.14, 1.00, 0.41, 0.34],
        [0.19, 0.40, 0.80, 0.27, 0.16, 0.41, 1.00, 0.30],
        [0.13, 0.34, 0.29, 0.84, 0.21, 0.34, 0.30, 1.00],
    ])
    return pd.DataFrame(corr, index=tickers, columns=tickers)

df = load_data()
yearly_returns = load_yearly_returns()
corr_df = load_correlation()

# ═══════════════════════════════════════════════════════════════════════════════
# 사이드바
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ⚙️ 필터 설정")
    st.markdown("---")
    
    strategies = st.multiselect(
        "🎯 전략 선택",
        options=['TQQQ Sniper', 'Upbit', 'Bitget Futures'],
        default=['TQQQ Sniper', 'Upbit', 'Bitget Futures']
    )
    
    min_years = st.slider("📅 최소 테스트 기간 (년)", 0.0, 15.0, 0.0, 0.5)
    max_mdd = st.slider("⚠️ 최대 MDD (%)", -100, 0, -100)
    
    st.markdown("---")
    st.markdown("### 📊 데이터 정보")
    st.info(f"""
    • 전략 수: **3개**  
    • 총 자산: **37개**  
    • TQQQ: 1개  
    • Upbit: 32개 코인  
    • Bitget: 4개 코인  
    • 기간: 2011-2025
    """)

filtered_df = df[
    (df['Strategy'].isin(strategies)) &
    (df['Years'] >= min_years) &
    (df['MDD'] >= max_mdd)
]

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<p class="main-header">📊 Trading Strategy Backtest Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">TQQQ Sniper • Upbit 32코인 • Bitget 선물 4코인 | 총 37개 자산 분석</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 핵심 지표
# ═══════════════════════════════════════════════════════════════════════════════

col1, col2, col3, col4 = st.columns(4)

with col1:
    best = filtered_df.loc[filtered_df['CAGR'].idxmax()] if len(filtered_df) > 0 else None
    st.metric("🏆 Best CAGR", f"{best['CAGR']:,.1f}%" if best is not None else "N/A", best['Ticker'] if best is not None else "")

with col2:
    best = filtered_df.loc[filtered_df['Sharpe'].idxmax()] if len(filtered_df) > 0 else None
    st.metric("🎯 Best Sharpe", f"{best['Sharpe']:.2f}" if best is not None else "N/A", best['Ticker'] if best is not None else "")

with col3:
    best = filtered_df.loc[filtered_df['MDD'].idxmax()] if len(filtered_df) > 0 else None
    st.metric("🛡️ Lowest MDD", f"{best['MDD']:.1f}%" if best is not None else "N/A", best['Ticker'] if best is not None else "")

with col4:
    best = filtered_df.loc[filtered_df['Years'].idxmax()] if len(filtered_df) > 0 else None
    st.metric("⏱️ Longest Test", f"{best['Years']:.1f}년" if best is not None else "N/A", best['Ticker'] if best is not None else "")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# 탭
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "📊 Performance", "⚠️ Risk", "🔗 Correlation", "💼 Portfolio"])

# TAB 1: Overview
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 전략별 평균 성과")
        strategy_avg = filtered_df.groupby('Strategy').agg({
            'CAGR': 'mean', 'MDD': 'mean', 'Sharpe': 'mean'
        }).round(2).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='CAGR (%)', x=strategy_avg['Strategy'], y=strategy_avg['CAGR'], marker_color='#6366f1'))
        fig.add_trace(go.Bar(name='|MDD| (%)', x=strategy_avg['Strategy'], y=abs(strategy_avg['MDD']), marker_color='#ef4444'))
        fig.update_layout(barmode='group', height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 전략별 자산 분포")
        count = filtered_df['Strategy'].value_counts()
        fig = px.pie(values=count.values, names=count.index, hole=0.4, color_discrete_sequence=['#22c55e', '#f59e0b', '#6366f1'])
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 🏆 Top 15 Performance")
    top_n = filtered_df.sort_values('CAGR', ascending=False).head(15)[['Ticker', 'Strategy', 'CAGR', 'MDD', 'Sharpe', 'WinRate', 'Years', 'Trades']]
    st.dataframe(
        top_n.style.format({'CAGR': '{:.1f}%', 'MDD': '{:.1f}%', 'Sharpe': '{:.2f}', 'WinRate': '{:.1f}%', 'Years': '{:.2f}'})
        .background_gradient(subset=['CAGR'], cmap='Greens').background_gradient(subset=['MDD'], cmap='Reds_r'),
        use_container_width=True, height=500
    )
    
    with st.expander("📋 전체 37개 자산 보기"):
        full_df = filtered_df.sort_values('CAGR', ascending=False)[['Ticker', 'Strategy', 'CAGR', 'MDD', 'Sharpe', 'WinRate', 'Years', 'Trades', 'TotalReturn']]
        st.dataframe(full_df.style.format({'CAGR': '{:.1f}%', 'MDD': '{:.1f}%', 'Sharpe': '{:.2f}', 'WinRate': '{:.1f}%', 'Years': '{:.2f}', 'TotalReturn': '{:,.1f}%'}), use_container_width=True, height=600)

# TAB 2: Performance
with tab2:
    # 전략별 요약 통계
    st.markdown("### 📊 전략별 요약 통계")
    
    col1, col2, col3 = st.columns(3)
    
    strategy_stats = df.groupby('Strategy').agg({
        'CAGR': ['mean', 'min', 'max'],
        'MDD': 'mean',
        'Sharpe': 'mean',
        'Years': 'mean'
    }).round(1)
    
    with col1:
        st.markdown("#### 🔵 TQQQ Sniper")
        st.metric("평균 CAGR", "26.7%")
        st.metric("MDD", "-38.4%")
        st.metric("Sharpe", "0.85")
        st.metric("테스트 기간", "14.8년")
    
    with col2:
        upbit_stats = df[df['Strategy'] == 'Upbit']
        st.markdown("#### 🟢 Upbit (32코인)")
        st.metric("평균 CAGR", f"{upbit_stats['CAGR'].mean():.1f}%", f"범위: {upbit_stats['CAGR'].min():.0f}~{upbit_stats['CAGR'].max():.0f}%")
        st.metric("평균 MDD", f"{upbit_stats['MDD'].mean():.1f}%")
        st.metric("평균 Sharpe", f"{upbit_stats['Sharpe'].mean():.2f}")
        st.metric("평균 테스트 기간", f"{upbit_stats['Years'].mean():.1f}년")
    
    with col3:
        bitget_stats = df[df['Strategy'] == 'Bitget Futures']
        st.markdown("#### 🟠 Bitget Futures (4코인)")
        st.metric("평균 CAGR", f"{bitget_stats['CAGR'].mean():.1f}%", f"범위: {bitget_stats['CAGR'].min():.0f}~{bitget_stats['CAGR'].max():.0f}%")
        st.metric("평균 MDD", f"{bitget_stats['MDD'].mean():.1f}%")
        st.metric("평균 Sharpe", f"{bitget_stats['Sharpe'].mean():.2f}")
        st.metric("평균 테스트 기간", f"{bitget_stats['Years'].mean():.1f}년")
    
    st.markdown("---")
    st.markdown("### 📅 전략별 연도별 수익률 비교")
    
    # 스케일 차이가 크므로 두 개 차트로 분리
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### TQQQ Sniper (안정형)")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='TQQQ Sniper', 
            x=yearly_returns['Year'], 
            y=yearly_returns['TQQQ Sniper'],
            marker_color=['#ef4444' if v < 0 else '#6366f1' for v in yearly_returns['TQQQ Sniper']],
            text=[f"{v:.1f}%" for v in yearly_returns['TQQQ Sniper']],
            textposition='outside'
        ))
        fig.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8', showlegend=False, yaxis_title='수익률 (%)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 암호화폐 전략 (고수익/고위험)")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Upbit', x=yearly_returns['Year'], y=yearly_returns['Upbit'], marker_color='#22c55e'))
        fig.add_trace(go.Bar(name='Bitget', x=yearly_returns['Year'], y=yearly_returns['Bitget Futures'], marker_color='#f59e0b'))
        fig.update_layout(barmode='group', height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8', yaxis_title='수익률 (%)')
        st.plotly_chart(fig, use_container_width=True)
        st.caption("💡 2020-2021년 암호화폐 강세장에서 극단적인 수익률 기록")
    
    # 통합 비교 테이블
    st.markdown("### 📊 연도별 수익률 상세")
    yearly_display = yearly_returns.copy()
    yearly_display.columns = ['연도', 'TQQQ Sniper (%)', 'Upbit (%)', 'Bitget (%)']
    st.dataframe(
        yearly_display.style.format({'TQQQ Sniper (%)': '{:.1f}', 'Upbit (%)': '{:.1f}', 'Bitget (%)': '{:.1f}'})
        .background_gradient(subset=['TQQQ Sniper (%)'], cmap='RdYlGn', vmin=-50, vmax=150)
        .background_gradient(subset=['Upbit (%)'], cmap='RdYlGn', vmin=-50, vmax=500)
        .background_gradient(subset=['Bitget (%)'], cmap='RdYlGn', vmin=-50, vmax=500),
        use_container_width=True
    )
    
    st.markdown("### 🎯 리스크-수익률 분포")
    fig = px.scatter(filtered_df, x=filtered_df['MDD'].abs(), y='CAGR', size='Sharpe', color='Strategy', hover_name='Ticker', size_max=40, color_discrete_map={'TQQQ Sniper': '#6366f1', 'Upbit': '#22c55e', 'Bitget Futures': '#f59e0b'})
    fig.update_layout(height=500, xaxis_title='MDD (%)', yaxis_title='CAGR (%)', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: Risk
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ MDD 비교 (Top 20)")
        mdd_data = filtered_df.sort_values('MDD', ascending=True).head(20)
        fig = go.Figure(go.Bar(x=mdd_data['MDD'], y=mdd_data['Ticker'], orientation='h', marker_color=[('#22c55e' if v > -40 else '#f59e0b' if v > -60 else '#ef4444') for v in mdd_data['MDD']]))
        fig.update_layout(height=550, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Sharpe Ratio (Top 20)")
        sharpe_data = filtered_df.sort_values('Sharpe', ascending=False).head(20)
        fig = go.Figure(go.Bar(x=sharpe_data['Sharpe'], y=sharpe_data['Ticker'], orientation='h', marker_color=[('#22c55e' if v > 2 else '#f59e0b' if v > 1 else '#ef4444') for v in sharpe_data['Sharpe']]))
        fig.update_layout(height=550, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📊 리스크 등급")
    col1, col2, col3 = st.columns(3)
    safe = filtered_df[filtered_df['MDD'] > -40]
    caution = filtered_df[(filtered_df['MDD'] <= -40) & (filtered_df['MDD'] > -60)]
    danger = filtered_df[filtered_df['MDD'] <= -60]
    
    with col1:
        st.markdown(f'<div class="success-box"><h4>🟢 안전: {len(safe)}개</h4>MDD > -40%</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="highlight-box"><h4>🟡 주의: {len(caution)}개</h4>-60% < MDD ≤ -40%</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="warning-box"><h4>🔴 위험: {len(danger)}개</h4>MDD ≤ -60%</div>', unsafe_allow_html=True)

# TAB 4: Correlation
with tab4:
    st.markdown("### 🔗 상관관계 매트릭스")
    fig = px.imshow(corr_df, labels=dict(color="Correlation"), x=corr_df.columns, y=corr_df.index, color_continuous_scale='RdYlGn', zmin=-1, zmax=1, text_auto='.2f')
    fig.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="highlight-box"><h4>🔍 핵심 인사이트</h4><ul><li><strong>TQQQ ↔ 암호화폐</strong>: 0.06~0.19 (매우 낮음)</li><li><strong>동일 코인 Upbit/Bitget</strong>: 0.73~0.84 (높음)</li><li><strong>SUIUSDT</strong>: 다른 자산과 0.06~0.24 (매우 낮음)</li></ul></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="success-box"><h4>💡 시사점</h4><ul><li>✅ TQQQ + 암호화폐 = 최적 분산</li><li>✅ SUIUSDT는 분산 효과 탁월</li><li>❌ 동일 코인 중복 투자 비효율</li></ul></div>', unsafe_allow_html=True)

# TAB 5: Portfolio
with tab5:
    st.markdown("### 💼 포트폴리오 구성 제안")
    
    col1, col2, col3 = st.columns(3)
    portfolios = [
        {"name": "🐢 보수적", "tqqq": 50, "upbit": 35, "bitget": 15, "cagr": "50-80%", "mdd": "-25~35%"},
        {"name": "⚖️ 균형", "tqqq": 30, "upbit": 40, "bitget": 30, "cagr": "100-150%", "mdd": "-35~50%"},
        {"name": "🚀 공격적", "tqqq": 20, "upbit": 30, "bitget": 50, "cagr": "200-400%", "mdd": "-50~70%"},
    ]
    
    for col, p in zip([col1, col2, col3], portfolios):
        with col:
            st.markdown(f"#### {p['name']}")
            fig = go.Figure(go.Pie(labels=['TQQQ', 'Upbit', 'Bitget'], values=[p['tqqq'], p['upbit'], p['bitget']], hole=0.4, marker_colors=['#6366f1', '#22c55e', '#f59e0b']))
            fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"**CAGR**: {p['cagr']} | **MDD**: {p['mdd']}")
    
    st.markdown("---")
    st.markdown("### 🧮 커스텀 포트폴리오 계산기")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        w_tqqq = st.slider("TQQQ (%)", 0, 100, 33)
    with c2:
        w_upbit = st.slider("Upbit (%)", 0, 100 - w_tqqq, 34)
    with c3:
        w_bitget = 100 - w_tqqq - w_upbit
        st.metric("Bitget (%)", w_bitget)
    
    avg = df.groupby('Strategy').agg({'CAGR': 'mean', 'MDD': 'mean'})
    exp_cagr = (w_tqqq/100 * avg.loc['TQQQ Sniper', 'CAGR'] + w_upbit/100 * avg.loc['Upbit', 'CAGR'] + w_bitget/100 * avg.loc['Bitget Futures', 'CAGR'])
    exp_mdd = (w_tqqq/100 * avg.loc['TQQQ Sniper', 'MDD'] + w_upbit/100 * avg.loc['Upbit', 'MDD'] + w_bitget/100 * avg.loc['Bitget Futures', 'MDD'])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("예상 CAGR", f"{exp_cagr:.1f}%")
    with c2:
        st.metric("예상 MDD", f"{exp_mdd:.1f}%")
    with c3:
        st.metric("효율성", f"{exp_cagr/abs(exp_mdd):.2f}")
    
    st.markdown('<div class="warning-box"><h4>⚠️ 투자 주의사항</h4><ul><li>과거 성과가 미래 수익을 보장하지 않습니다</li><li>테스트 기간 1년 미만 코인은 과적합 위험이 높습니다</li><li>실제 거래 시 슬리피지로 성과가 하락할 수 있습니다</li></ul></div>', unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown('<div style="text-align: center; color: #64748b; padding: 1rem;">📊 Trading Strategy Backtest Dashboard<br><strong>37개 자산</strong> | TQQQ 1 + Upbit 32 + Bitget 4 | 2011-2025</div>', unsafe_allow_html=True)
