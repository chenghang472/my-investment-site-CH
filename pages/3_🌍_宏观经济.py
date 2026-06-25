import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import load_data

st.set_page_config(page_title="🌍 宏观经济", page_icon="🌍", layout="wide")

# ========== CSS ==========
st.markdown("""
<style>
    .macro-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin: 0.3rem 0;
        transition: all 0.3s;
    }
    .macro-card:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .macro-name { font-size: 0.85rem; color: #7f8c8d; margin-bottom: 0.3rem; }
    .macro-value { font-size: 1.8rem; font-weight: bold; color: #2c3e50; }
    .macro-unit { font-size: 0.8rem; color: #95a5a6; }
    .macro-trend { font-size: 0.9rem; margin-top: 0.3rem; }
    @media (max-width: 768px) {
        .macro-value { font-size: 1.4rem; }
    }
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown("## 🌍 宏观经济")
    st.markdown("---")
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")
    if st.button("📈 股票看板", use_container_width=True):
        st.switch_page("pages/1_📈_股票看板.py")
    if st.button("📊 基金分析", use_container_width=True):
        st.switch_page("pages/2_📊_基金分析.py")
    st.markdown("---")
    st.info("💡 数据文件: data/macro.csv\n\n用 Excel 编辑后刷新即可")

# ========== 加载数据 ==========
df = load_data("macro.csv")

if df.empty:
    st.error("❌ 没有找到宏观数据，请检查 data/macro.csv 文件")
    st.stop()

# ========== 页面标题 ==========
st.markdown("# 🌍 宏观经济")
st.markdown("---")

# ========== 指标卡片区 ==========
st.markdown("## 📊 核心指标")

if len(df) > 0:
    # 每行显示4个指标
    cols_per_row = 4
    rows = (len(df) + cols_per_row - 1) // cols_per_row

    for r in range(rows):
        cols = st.columns(cols_per_row)
        for c in range(cols_per_row):
            idx = r * cols_per_row + c
            if idx < len(df):
                row = df.iloc[idx]
                with cols[c]:
                    name = row.get("指标名称", "--")
                    value = row.get("最新值", "--")
                    unit = row.get("单位", "")
                    trend = row.get("趋势", "→")

                    trend_color = {"↑": "#e74c3c", "↓": "#2ecc71", "→": "#95a5a6"}
                    color = trend_color.get(trend, "#95a5a6")

                    st.markdown(f"""
                    <div class="macro-card">
                        <div class="macro-name">{name}</div>
                        <div class="macro-value">{value}<span class="macro-unit">{unit}</span></div>
                        <div class="macro-trend" style="color: {color}">{trend}</div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("---")

# ========== 图表区 ==========
if len(df) > 0:
    tab1, tab2 = st.tabs(["📈 指标对比", "📋 数据详情"])

    with tab1:
        if "指标名称" in df.columns and "最新值" in df.columns:
            # 过滤掉非数值型指标（如汇率）
            numeric_df = df.copy()
            numeric_df["最新值"] = pd.to_numeric(numeric_df["最新值"], errors="coerce")
            numeric_df = numeric_df.dropna(subset=["最新值"])

            if len(numeric_df) > 0:
                fig = px.bar(numeric_df, x="指标名称", y="最新值", 
                            color="指标名称", title="宏观经济指标对比",
                            color_discrete_sequence=px.colors.qualitative.Bold)
                fig.update_layout(height=500, xaxis_tickangle=-30, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("暂无可用图表数据")

    with tab2:
        st.dataframe(df, use_container_width=True, hide_index=True)

# ========== 市场温度计 ==========
st.markdown("---")
st.markdown("## 🌡️ 市场温度计")

if "指标名称" in df.columns:
    # 找到关键指标
    key_indicators = ["PMI", "CPI", "十年国债收益率", "A股成交额"]

    for indicator in key_indicators:
        indicator_data = df[df["指标名称"] == indicator]
        if len(indicator_data) > 0:
            val = indicator_data.iloc[0].get("最新值", 0)
            unit = indicator_data.iloc[0].get("单位", "%")

            try:
                val = float(val)

                # 根据不同指标设置范围
                if indicator == "PMI":
                    max_val, threshold = 60, 50
                    label = "荣枯线"
                elif indicator == "CPI":
                    max_val, threshold = 5, 2
                    label = "目标值"
                elif indicator == "十年国债收益率":
                    max_val, threshold = 5, 3
                    label = "中性水平"
                elif indicator == "A股成交额":
                    max_val, threshold = 2, 1
                    label = "活跃线(万亿)"
                    unit = "万亿"
                else:
                    max_val, threshold = 100, 50
                    label = "参考值"

                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"**{indicator}**")
                    st.markdown(f"当前: **{val}{unit}**")
                with col2:
                    progress = min(val / max_val, 1.0)
                    st.progress(progress, text=f"{label}: {threshold}{unit}")
            except:
                pass

# ========== 数据表格 ==========
with st.expander("📊 查看完整数据表"):
    st.dataframe(df, use_container_width=True, hide_index=True)
