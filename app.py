"""
📊 Trading Strategy Backtest Dashboard
=====================================
배포 URL: https://YOUR-APP.streamlit.app
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# 커스텀 CSS
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
        color: #64748b;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
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
        background-color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 700;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 0.875rem;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #6366f1;
        padding: 1rem 1.5rem;
        border-radius: 0 0.5rem 0.5rem 0;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 4px solid #ef4444;
        padding: 1rem 1.5rem;
        border-radius: 0 0.5rem 0.5rem 0;
        margin: 1rem 0;
    }
    
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 데이터 로드
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    """백테스트 결과 데이터"""
    data = {
        'Strategy': ['TQQQ Sniper', 'Bitget Futures', 'Bitget Futures', 'Bitget Futures', 'Bitget Futures',
                     'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit',
                     'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit', 'Upbit'],
        'Ticker': ['TQQQ', 'SOLUSDT', 'SUIUSDT', 'ETHUSDT', 'BTCUSDT',
                   'KRW-SUI', 'KRW-SOL', 'KRW-ETH', 'KRW-BTC', 'KRW-AVAX',
                   'KRW-VET', 'KRW-SAND', 'KRW-HBAR', 'KRW-XRP', 'KRW-ADA',
                   'KRW-POL', 'KRW-NEAR', 'KRW-THETA', 'KRW-MANA', 'KRW-ANKR',
                   'KRW-DOT', 'KRW-DOGE', 'KRW-LINK', 'KRW-XLM', 'KRW-BCH'],
        'CAGR': [26.65, 1911.81, 1162.43, 657.60, 417.06,
                 540.26, 181.14, 140.52, 101.66, 216.14,
                 223.26, 229.50, 209.28, 173.31, 170.85,
                 178.98, 187.47, 159.82, 169.52, 159.05,
                 132.68, 101.08, 118.04, 127.94, 69.32],
        'MDD': [-38.39, -74.39, -62.94, -67.84, -63.21,
                -46.10, -27.58, -27.78, -32.75, -33.18,
                -59.31, -62.15, -57.38, -69.08, -51.46,
                -32.79, -51.73, -59.23, -63.16, -60.64,
                -54.32, -59.66, -47.56, -59.56, -51.92],
        'Sharpe': [0.85, 2.54, 2.22, 2.11, 2.00,
                   2.75, 2.16, 2.10, 2.10, 2.16,
                   1.90, 1.69, 1.69, 1.56, 1.85,
                   1.93, 1.82, 1.57, 1.36, 1.44,
                   1.66, 1.35, 1.49, 1.44, 1.10],
        'WinRate': [44.2, 19.0, 18.1, 20.0, 21.2,
                    25.4, 18.4, 19.2, 23.5, 25.5,
                    22.2, 20.9, 21.2, 18.0, 20.9,
                    20.9, 21.9, 18.9, 19.4, 20.4,
                    20.2, 20.8, 21.8, 15.6, 17.4],
        'Years': [14.83, 5.06, 2.30, 5.83, 6.08,
                  2.17, 3.64, 7.58, 7.72, 3.41,
                  5.31, 4.53, 5.75, 8.07, 7.62,
                  3.53, 3.46, 6.46, 6.53, 5.95,
                  4.70, 4.33, 5.00, 8.05, 7.99],
        'Trades': [688, 260, 64, 150, 176,
                   98, 190, 246, 288, 300,
                   342, 106, 336, 394, 284,
                   268, 122, 220, 276, 238,
                   263, 268, 380, 470, 405],
    }
    return pd.DataFrame(data)

@st.cache_data
def load_yearly_returns():
    """연도별 수익률"""
    return pd.DataFrame({
        'Year': ['2020', '2021', '2022', '2023', '2024', '2025'],
        'TQQQ': [110.3, 34.5, -23.3, 80.4, 25.3, 45.7],
        'BTCUSDT': [610.9, 321.0, -36.9, 321.2, 226.2, 24.2],
        'ETHUSDT': [476.8, 749.7, 177.1, 123.9, 196.3, 290.1],
        'SOLUSDT': [0, 2379.2, 42.3, 778.4, 259.9, 97.4],
    })

@st.cache_data
def load_correlation():
    """상관관계 매트릭스"""
    tickers = ['TQQQ', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'KRW-BTC', 'KRW-ETH', 'KRW-SOL']
    corr = np.array([
        [1.00, 0.11, 0.19, 0.12, 0.10, 0.19, 0.13],
        [0.11, 1.00, 0.40, 0.38, 0.73, 0.40, 0.34],
        [0.19, 0.40, 1.00, 0.28, 0.37, 0.80, 0.29],
        [0.12, 0.38, 0.28, 1.00, 0.33, 0.27, 0.84],
        [0.10, 0.73, 0.37, 0.33, 1.00, 0.41, 0.34],
        [0.19, 0.40, 0.80, 0.27, 0.41, 1.00, 0.30],
        [0.13, 0.34, 0.29, 0.84, 0.34, 0.30, 1.00],
    ])
    return pd.DataFrame(corr, index=tickers, columns=tickers)

# 데이터 로드
df = load_data()
yearly_returns = load_yearly_returns()
corr_df = load_correlation()

# ═══════════════════════════════════════════════════════════════════════════════
# 사이드바
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ⚙️ 필터 설정")
    st.markdown("---")
    
    # 전략 필터
    strategies = st.multiselect(
        "🎯 전략 선택",
        options=['TQQQ Sniper', 'Upbit', 'Bitget Futures'],
        default=['TQQQ Sniper', 'Upbit', 'Bitget Futures']
    )
    
    # 기간 필터
    min_years = st.slider("📅 최소 테스트 기간 (년)", 0.0, 15.0, 0.0, 0.5)
    
    # MDD 필터
    max_mdd = st.slider("⚠️ 최대 MDD (%)", -100, 0, -100)
    
    st.markdown("---")
    st.markdown("### 📊 데이터 정보")
    st.info(f"""
    - **전략 수**: {len(df['Strategy'].unique())}개
    - **자산 수**: {len(df)}개
    - **기간**: 2010-2025
    """)

# 필터 적용
filtered_df = df[
    (df['Strategy'].isin(strategies)) &
    (df['Years'] >= min_years) &
    (df['MDD'] >= max_mdd)
]

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<p class="main-header">📊 Trading Strategy Backtest Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">TQQQ Sniper • Upbit 암호화폐 • Bitget 선물 | 3개 전략 통합 분석</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 핵심 지표 카드
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

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: Overview
# ═══════════════════════════════════════════════════════════════════════════════

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
        fig.update_layout(barmode='group', height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 전략 분포")
        count = filtered_df['Strategy'].value_counts()
        fig = px.pie(values=count.values, names=count.index, hole=0.4, color_discrete_sequence=['#6366f1', '#22c55e', '#f59e0b'])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top 10 테이블
    st.markdown("### 🏆 Top 10 Performance Rankings")
    top10 = filtered_df.sort_values('CAGR', ascending=False).head(10)[['Ticker', 'Strategy', 'CAGR', 'MDD', 'Sharpe', 'WinRate', 'Years']]
    
    st.dataframe(
        top10.style.format({
            'CAGR': '{:.1f}%', 'MDD': '{:.1f}%', 'Sharpe': '{:.2f}', 'WinRate': '{:.1f}%', 'Years': '{:.1f}'
        }).background_gradient(subset=['CAGR'], cmap='Greens')
         .background_gradient(subset=['MDD'], cmap='Reds_r'),
        use_container_width=True, height=400
    )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: Performance
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### 📅 연도별 수익률 비교")
    
    fig = go.Figure()
    colors = {'TQQQ': '#6366f1', 'BTCUSDT': '#f59e0b', 'ETHUSDT': '#22c55e', 'SOLUSDT': '#ef4444'}
    for col in ['TQQQ', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT']:
        fig.add_trace(go.Bar(name=col, x=yearly_returns['Year'], y=yearly_returns[col], marker_color=colors[col]))
    fig.update_layout(barmode='group', height=450, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 🎯 리스크-수익률 분포")
    fig = px.scatter(
        filtered_df, x=filtered_df['MDD'].abs(), y='CAGR', 
        size='Sharpe', color='Strategy', hover_name='Ticker',
        size_max=40, color_discrete_map={'TQQQ Sniper': '#6366f1', 'Upbit': '#22c55e', 'Bitget Futures': '#f59e0b'}
    )
    fig.update_layout(height=450, xaxis_title='MDD (%, Absolute)', yaxis_title='CAGR (%)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: Risk
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ MDD 비교")
        mdd_data = filtered_df.sort_values('MDD', ascending=True).head(15)
        fig = go.Figure(go.Bar(
            x=mdd_data['MDD'], y=mdd_data['Ticker'], orientation='h',
            marker_color=[('#22c55e' if v > -40 else '#f59e0b' if v > -60 else '#ef4444') for v in mdd_data['MDD']]
        ))
        fig.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Sharpe Ratio")
        sharpe_data = filtered_df.sort_values('Sharpe', ascending=False).head(15)
        fig = go.Figure(go.Bar(
            x=sharpe_data['Sharpe'], y=sharpe_data['Ticker'], orientation='h',
            marker_color=[('#22c55e' if v > 2 else '#f59e0b' if v > 1 else '#ef4444') for v in sharpe_data['Sharpe']]
        ))
        fig.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    # 리스크 등급
    col1, col2, col3 = st.columns(3)
    safe = filtered_df[filtered_df['MDD'] > -40]
    caution = filtered_df[(filtered_df['MDD'] <= -40) & (filtered_df['MDD'] > -60)]
    danger = filtered_df[filtered_df['MDD'] <= -60]
    
    with col1:
        st.success(f"🟢 안전: {len(safe)}개")
        st.caption("MDD > -40%")
    with col2:
        st.warning(f"🟡 주의: {len(caution)}개")
        st.caption("-60% < MDD ≤ -40%")
    with col3:
        st.error(f"🔴 위험: {len(danger)}개")
        st.caption("MDD ≤ -60%")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: Correlation
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### 🔗 전략 간 상관관계 매트릭스")
    
    fig = px.imshow(
        corr_df, labels=dict(color="Correlation"),
        x=corr_df.columns, y=corr_df.index,
        color_continuous_scale='RdYlGn', zmin=-1, zmax=1, text_auto='.2f'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="highlight-box">
        <h4>🔍 핵심 인사이트</h4>
        <ul>
            <li><strong>TQQQ ↔ 암호화폐</strong>: 0.06~0.19 (매우 낮음)</li>
            <li><strong>동일 코인 Upbit/Bitget</strong>: 0.73~0.84 (높음)</li>
            <li><strong>알트코인 간</strong>: 0.15~0.40 (중간)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
        <h4>💡 시사점</h4>
        <ul>
            <li>✅ TQQQ + 암호화폐 = 최적 분산</li>
            <li>❌ 동일 코인 중복 투자 비효율</li>
            <li>⚠️ SUI, SOL은 분산 효과 우수</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5: Portfolio
# ═══════════════════════════════════════════════════════════════════════════════

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
            fig = go.Figure(go.Pie(
                labels=['TQQQ', 'Upbit', 'Bitget'],
                values=[p['tqqq'], p['upbit'], p['bitget']],
                hole=0.4, marker_colors=['#6366f1', '#22c55e', '#f59e0b']
            ))
            fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"**CAGR**: {p['cagr']} | **MDD**: {p['mdd']}")
    
    # 커스텀 계산기
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
    
    # 예상 성과
    avg = df.groupby('Strategy').agg({'CAGR': 'mean', 'MDD': 'mean'})
    exp_cagr = (w_tqqq/100 * avg.loc['TQQQ Sniper', 'CAGR'] + 
                w_upbit/100 * avg.loc['Upbit', 'CAGR'] + 
                w_bitget/100 * avg.loc['Bitget Futures', 'CAGR'])
    exp_mdd = (w_tqqq/100 * avg.loc['TQQQ Sniper', 'MDD'] + 
               w_upbit/100 * avg.loc['Upbit', 'MDD'] + 
               w_bitget/100 * avg.loc['Bitget Futures', 'MDD'])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("예상 CAGR", f"{exp_cagr:.1f}%")
    with c2:
        st.metric("예상 MDD", f"{exp_mdd:.1f}%")
    with c3:
        st.metric("효율성", f"{exp_cagr/abs(exp_mdd):.2f}")
    
    # 경고
    st.markdown("""
    <div class="warning-box">
    <h4>⚠️ 투자 주의사항</h4>
    <ul>
        <li>과거 성과가 미래 수익을 보장하지 않습니다</li>
        <li>단기 데이터 코인은 과적합 위험이 있습니다</li>
        <li>실제 거래 시 슬리피지로 성과가 하락할 수 있습니다</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 푸터
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 1rem;'>
    📊 Trading Strategy Backtest Dashboard<br>
    Data: 2010-2025 | Built with Streamlit + Plotly<br>
    <small>Last Updated: 2025-12-30</small>
</div>
""", unsafe_allow_html=True)
