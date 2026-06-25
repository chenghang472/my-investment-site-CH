import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import load_data

st.set_page_config(page_title="📈 股票看板", page_icon="📈", layout="wide")

# ========== CSS ==========
st.markdown("""
<style>
    .stock-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .stock-card:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stock-name { font-size: 1.1rem; font-weight: bold; color: #2c3e50; }
    .stock-code { font-size: 0.8rem; color: #95a5a6; }
    .stock-price { font-size: 1.5rem; font-weight: bold; }
    .up { color: #e74c3c; }
    .down { color: #2ecc71; }
    @media (max-width: 768px) {
        .stock-price { font-size: 1.2rem; }
    }
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown("## 📈 股票看板")
    st.markdown("---")
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")
    if st.button("📊 基金分析", use_container_width=True):
        st.switch_page("pages/2_📊_基金分析.py")
    if st.button("🌍 宏观经济", use_container_width=True):
        st.switch_page("pages/3_🌍_宏观经济.py")
    st.markdown("---")
    st.info("💡 数据文件: data/stocks.csv\n\n用 Excel 编辑后刷新即可")

# ========== 加载数据 ==========
df = load_data("stocks.csv")

if df.empty:
    st.error("❌ 没有找到股票数据，请检查 data/stocks.csv 文件")
    st.stop()

# ========== 页面标题 ==========
st.markdown("# 📈 股票看板")
st.markdown("---")

# ========== 筛选器 ==========
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    industries = ["全部"] + sorted(df["行业"].unique().tolist()) if "行业" in df.columns else ["全部"]
    selected_industry = st.selectbox("🏭 行业筛选", industries)
with col2:
    ratings = ["全部"] + sorted(df["推荐评级"].unique().tolist()) if "推荐评级" in df.columns else ["全部"]
    selected_rating = st.selectbox("⭐ 评级筛选", ratings)
with col3:
    sort_by = st.selectbox("📊 排序", ["默认", "市值", "涨跌幅", "PE", "ROE"])

# 筛选数据
filtered_df = df.copy()
if selected_industry != "全部" and "行业" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["行业"] == selected_industry]
if selected_rating != "全部" and "推荐评级" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["推荐评级"] == selected_rating]

# 排序
if sort_by == "市值" and "市值亿" in filtered_df.columns:
    filtered_df = filtered_df.sort_values("市值亿", ascending=False)
elif sort_by == "涨跌幅" and "涨跌幅" in filtered_df.columns:
    filtered_df = filtered_df.sort_values("涨跌幅", ascending=False)
elif sort_by == "PE" and "PE" in filtered_df.columns:
    filtered_df = filtered_df.sort_values("PE", ascending=True)
elif sort_by == "ROE" and "ROE" in filtered_df.columns:
    filtered_df = filtered_df.sort_values("ROE", ascending=False)

st.markdown(f"**共筛选出 {len(filtered_df)} 只股票**")

# ========== 图表区 ==========
if len(filtered_df) > 0:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 行业分布", "💰 市值排行", "📈 涨跌分布", "🔍 估值散点"])

    with tab1:
        if "行业" in filtered_df.columns:
            industry_counts = filtered_df["行业"].value_counts().reset_index()
            industry_counts.columns = ["行业", "数量"]
            fig = px.pie(industry_counts, names="行业", values="数量", 
                        title="行业分布", color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if "名称" in filtered_df.columns and "市值亿" in filtered_df.columns:
            top10 = filtered_df.nlargest(10, "市值亿")
            fig = px.bar(top10, x="名称", y="市值亿", color="行业" if "行业" in top10.columns else None,
                        title="市值 TOP10", color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=450, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if "名称" in filtered_df.columns and "涨跌幅" in filtered_df.columns:
            colors = ["#e74c3c" if x > 0 else "#2ecc71" if x < 0 else "#95a5a6" for x in filtered_df["涨跌幅"]]
            fig = px.bar(filtered_df, x="名称", y="涨跌幅", 
                        title="涨跌幅分布", color_discrete_sequence=["#3498db"])
            fig.update_traces(marker_color=colors)
            fig.update_layout(height=450, xaxis_tickangle=-45)
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        if all(col in filtered_df.columns for col in ["PE", "PB", "名称"]):
            fig = px.scatter(filtered_df, x="PE", y="PB", size="市值亿" if "市值亿" in filtered_df.columns else None,
                            color="行业" if "行业" in filtered_df.columns else None,
                            hover_name="名称", title="PE-PB 估值散点图",
                            color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ========== 股票卡片列表 ==========
st.markdown("## 📋 股票详情")

for idx, row in filtered_df.iterrows():
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 1.5, 1.5, 1.5, 1.5])

        with col1:
            name = row.get("名称", "未知")
            code = row.get("代码", "")
            industry = row.get("行业", "")
            st.markdown(f"<div class="stock-name">{name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class="stock-code">{code} | {industry}</div>", unsafe_allow_html=True)

        with col2:
            price = row.get("最新价", "--")
            change = row.get("涨跌幅", 0)
            color_class = "up" if change > 0 else "down" if change < 0 else ""
            st.markdown(f"<div class="stock-price {color_class}">{price}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class="{color_class}">{change:+.2f}%</div>" if isinstance(change, (int, float)) else f"<div>{change}</div>", unsafe_allow_html=True)

        with col3:
            pe = row.get("PE", "--")
            st.metric("PE", f"{pe:.1f}" if isinstance(pe, (int, float)) else pe)

        with col4:
            pb = row.get("PB", "--")
            st.metric("PB", f"{pb:.2f}" if isinstance(pb, (int, float)) else pb)

        with col5:
            roe = row.get("ROE", "--")
            st.metric("ROE", f"{roe:.1f}%" if isinstance(roe, (int, float)) else roe)

        with col6:
            rating = row.get("推荐评级", "--")
            rating_color = {"买入": "🟢", "持有": "🟡", "卖出": "🔴"}
            emoji = rating_color.get(rating, "⚪")
            st.markdown(f"**{emoji} {rating}**")

        st.markdown("---")

# ========== 数据表格 ==========
with st.expander("📊 查看完整数据表"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
