import streamlit as st
import pandas as pd
from utils.helpers import load_data

# ========== 页面配置 ==========
st.set_page_config(
    page_title="📊 个人投研中心",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========== 自定义CSS（手机适配 + 美化） ==========
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .metric-card h3 {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: bold;
    }
    .module-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    .module-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #3498db;
    }
    .module-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .module-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.3rem;
    }
    .module-desc {
        font-size: 0.85rem;
        color: #7f8c8d;
    }
    @media (max-width: 768px) {
        .main-title { font-size: 1.8rem !important; }
        .module-icon { font-size: 2rem !important; }
        .module-title { font-size: 1rem !important; }
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏导航 ==========
with st.sidebar:
    st.markdown("## 📊 投研导航")
    st.markdown("---")
    if st.button("🏠 首页概览", use_container_width=True):
        st.switch_page("app.py")
    if st.button("📈 股票看板", use_container_width=True):
        st.switch_page("pages/1_📈_股票看板.py")
    if st.button("📊 基金分析", use_container_width=True):
        st.switch_page("pages/2_📊_基金分析.py")
    if st.button("🌍 宏观经济", use_container_width=True):
        st.switch_page("pages/3_🌍_宏观经济.py")
    st.markdown("---")
    st.markdown("### 💡 使用说明")
    st.info("""
    数据更新方式：
    1. 打开 data/ 文件夹
    2. 用 Excel/WPS 编辑 CSV 文件
    3. 保存后刷新网页即可

    添加新模块：
    复制现有页面文件，
    修改名称和内容
    """)
    st.markdown("---")
    st.caption("🛠️ 个人投研中心 v1.0")

# ========== 主页面内容 ==========
st.markdown('<div class="main-title">📊 个人投研中心</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">实时数据 · 智能分析 · 自主管理</div>', unsafe_allow_html=True)

df_stocks = load_data("stocks.csv")
df_funds = load_data("funds.csv")
df_macro = load_data("macro.csv")

# ========== 顶部指标卡片区 ==========
if not df_stocks.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>📈 关注股票数</h3><div class="value">{len(df_stocks)}</div></div>', unsafe_allow_html=True)
    with col2:
        buy_count = len(df_stocks[df_stocks["推荐评级"] == "买入"]) if "推荐评级" in df_stocks.columns else 0
        st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);"><h3>✅ 买入评级</h3><div class="value">{buy_count}</div></div>', unsafe_allow_html=True)
    with col3:
        fund_count = len(df_funds) if not df_funds.empty else 0
        st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);"><h3>📊 关注基金数</h3><div class="value">{fund_count}</div></div>', unsafe_allow_html=True)
    with col4:
        gdp_str = "--"
        if not df_macro.empty and "最新值" in df_macro.columns:
            gdp_val = df_macro[df_macro["指标名称"] == "GDP增速"]["最新值"].values
            if len(gdp_val) > 0:
                gdp_str = f"{gdp_val[0]}%"
        st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);"><h3>🌍 GDP增速</h3><div class="value">{gdp_str}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ========== 模块入口区 ==========
st.markdown("## 🚀 功能模块")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="module-card"><div class="module-icon">📈</div><div class="module-title">股票看板</div><div class="module-desc">个股分析 · 行业对比 · 估值筛选</div></div>', unsafe_allow_html=True)
    if st.button("进入股票看板", key="btn_stock", use_container_width=True):
        st.switch_page("pages/1_📈_股票看板.py")
with col2:
    st.markdown('<div class="module-card"><div class="module-icon">📊</div><div class="module-title">基金分析</div><div class="module-desc">基金筛选 · 业绩对比 · 持仓分析</div></div>', unsafe_allow_html=True)
    if st.button("进入基金分析", key="btn_fund", use_container_width=True):
        st.switch_page("pages/2_📊_基金分析.py")
with col3:
    st.markdown('<div class="module-card"><div class="module-icon">🌍</div><div class="module-title">宏观经济</div><div class="module-desc">宏观指标 · 政策跟踪 · 市场情绪</div></div>', unsafe_allow_html=True)
    if st.button("进入宏观经济", key="btn_macro", use_container_width=True):
        st.switch_page("pages/3_🌍_宏观经济.py")

st.markdown("---")

# ========== 数据概览区 ==========
st.markdown("## 📋 最新数据速览")
tab1, tab2, tab3 = st.tabs(["📈 股票", "📊 基金", "🌍 宏观"])
with tab1:
    if not df_stocks.empty:
        st.dataframe(df_stocks, use_container_width=True, hide_index=True)
    else:
        st.info("暂无股票数据，请在 data/stocks.csv 中添加")
with tab2:
    if not df_funds.empty:
        st.dataframe(df_funds, use_container_width=True, hide_index=True)
    else:
        st.info("暂无基金数据，请在 data/funds.csv 中添加")
with tab3:
    if not df_macro.empty:
        st.dataframe(df_macro, use_container_width=True, hide_index=True)
    else:
        st.info("暂无宏观数据，请在 data/macro.csv 中添加")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #95a5a6; font-size: 0.85rem;"><p>💡 提示：点击左侧导航或上方按钮进入各模块详细分析</p><p>📁 数据文件位置：data/ 文件夹下的 CSV 文件</p></div>', unsafe_allow_html=True)
