import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import load_data

st.set_page_config(page_title="📊 基金分析", page_icon="📊", layout="wide")

# ========== CSS ==========
st.markdown("""
<style>
    .fund-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .fund-card:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .fund-name { font-size: 1.1rem; font-weight: bold; color: #2c3e50; }
    .fund-code { font-size: 0.8rem; color: #95a5a6; }
    .star { color: #f1c40f; font-size: 1.2rem; }
    @media (max-width: 768px) {
        .fund-name { font-size: 0.95rem; }
    }
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown("## 📊 基金分析")
    st.markdown("---")
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")
    if st.button("📈 股票看板", use_container_width=True):
        st.switch_page("pages/1_📈_股票看板.py")
    if st.button("🌍 宏观经济", use_container_width=True):
        st.switch_page("pages/3_🌍_宏观经济.py")
    st.markdown("---")
    st.info("💡 数据文件: data/funds.csv\n\n用 Excel 编辑后刷新即可")

# ========== 加载数据 ==========
df = load_data("funds.csv")

if df.empty:
    st.error("❌ 没有找到基金数据，请检查 data/funds.csv 文件")
    st.stop()

# ========== 页面标题 ==========
st.markdown("# 📊 基金分析")
st.markdown("---")

# ========== 筛选器 ==========
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    types = ["全部"] + sorted(df["类型"].unique().tolist()) if "类型" in df.columns else ["全部"]
    selected_type = st.selectbox("📂 类型筛选", types)
with col2:
    managers = ["全部"] + sorted(df["基金经理"].unique().tolist()) if "基金经理" in df.columns else ["全部"]
    selected_manager = st.selectbox("👤 基金经理", managers)
with col3:
    sort_options = ["默认", "近1月", "近3月", "近1年", "规模"]
    sort_by = st.selectbox("📊 排序", sort_options)

# 筛选
filtered_df = df.copy()
if selected_type != "全部" and "类型" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["类型"] == selected_type]
if selected_manager != "全部" and "基金经理" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["基金经理"] == selected_manager]

# 排序
sort_map = {"近1月": "近1月", "近3月": "近3月", "近1年": "近1年", "规模": "规模亿"}
if sort_by in sort_map and sort_map[sort_by] in filtered_df.columns:
    filtered_df = filtered_df.sort_values(sort_map[sort_by], ascending=False)

st.markdown(f"**共筛选出 {len(filtered_df)} 只基金**")

# ========== 图表区 ==========
if len(filtered_df) > 0:
    tab1, tab2, tab3 = st.tabs(["📂 类型分布", "📈 业绩排行", "💰 规模分布"])

    with tab1:
        if "类型" in filtered_df.columns:
            type_counts = filtered_df["类型"].value_counts().reset_index()
            type_counts.columns = ["类型", "数量"]
            fig = px.pie(type_counts, names="类型", values="数量",
                        title="基金类型分布", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if "名称" in filtered_df.columns and "近1年" in filtered_df.columns:
            top10 = filtered_df.nlargest(10, "近1年")
            colors = ["#e74c3c" if x > 0 else "#2ecc71" if x < 0 else "#95a5a6" for x in top10["近1年"]]
            fig = px.bar(top10, x="名称", y="近1年", color="类型" if "类型" in top10.columns else None,
                        title="近1年收益 TOP10", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_traces(marker_color=colors)
            fig.update_layout(height=450, xaxis_tickangle=-45)
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if "名称" in filtered_df.columns and "规模亿" in filtered_df.columns:
            top10 = filtered_df.nlargest(10, "规模亿")
            fig = px.bar(top10, x="名称", y="规模亿", color="类型" if "类型" in top10.columns else None,
                        title="基金规模 TOP10", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(height=450, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ========== 基金卡片列表 ==========
st.markdown("## 📋 基金详情")

for idx, row in filtered_df.iterrows():
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1.5, 1.5, 1.5, 1.5, 1.5])

        with col1:
            name = row.get("名称", "未知")
            code = row.get("代码", "")
            fund_type = row.get("类型", "")
            manager = row.get("基金经理", "")
            st.markdown(f"<div class="fund-name">{name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class="fund-code">{code} | {fund_type} | {manager}</div>", unsafe_allow_html=True)

        with col2:
            nav = row.get("净值", "--")
            day_change = row.get("日涨幅", 0)
            color = "#e74c3c" if (isinstance(day_change, (int, float)) and day_change > 0) else "#2ecc71" if (isinstance(day_change, (int, float)) and day_change < 0) else "#95a5a6"
            st.markdown(f"**净值: {nav}**")
            st.markdown(f"<span style='color:{color}'>日涨跌: {day_change:+.2f}%</span>" if isinstance(day_change, (int, float)) else f"日涨跌: {day_change}", unsafe_allow_html=True)

        with col3:
            m1 = row.get("近1月", "--")
            st.metric("近1月", f"{m1:+.2f}%" if isinstance(m1, (int, float)) else m1)

        with col4:
            m3 = row.get("近3月", "--")
            st.metric("近3月", f"{m3:+.2f}%" if isinstance(m3, (int, float)) else m3)

        with col5:
            y1 = row.get("近1年", "--")
            st.metric("近1年", f"{y1:+.2f}%" if isinstance(y1, (int, float)) else y1)

        with col6:
            rating = row.get("评级", "")
            if isinstance(rating, str) and "★" in rating:
                stars = rating.count("★")
                empty = 5 - stars
                star_html = "<span class="star">" + "★" * stars + "☆" * empty + "</span>"
                st.markdown(star_html, unsafe_allow_html=True)
            else:
                st.markdown(f"**{rating}**")

        st.markdown("---")

# ========== 数据表格 ==========
with st.expander("📊 查看完整数据表"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
