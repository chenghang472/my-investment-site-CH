import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import os

# ========== 数据加载工具 ==========

def load_data(filename):
    """加载CSV数据，支持中文路径"""
    filepath = os.path.join("data", filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath, encoding="utf-8")
    else:
        st.error(f"❌ 找不到数据文件: {filepath}")
        return pd.DataFrame()

def save_data(df, filename):
    """保存数据到CSV"""
    filepath = os.path.join("data", filename)
    df.to_csv(filepath, index=False, encoding="utf-8")
    return True

# ========== 颜色工具 ==========

def get_color_by_value(val, positive_good=True):
    """根据数值返回颜色"""
    if pd.isna(val):
        return "gray"
    if positive_good:
        return "#e74c3c" if val > 0 else "#2ecc71" if val < 0 else "#95a5a6"
    else:
        return "#2ecc71" if val > 0 else "#e74c3c" if val < 0 else "#95a5a6"

def get_trend_emoji(val):
    """获取趋势emoji"""
    if pd.isna(val):
        return "➡️"
    if val > 0:
        return "📈"
    elif val < 0:
        return "📉"
    return "➡️"

# ========== 图表工具 ==========

def create_bar_chart(df, x_col, y_col, title, color_col=None, orientation="v"):
    """创建柱状图"""
    if color_col:
        fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=title,
                     color_discrete_sequence=px.colors.qualitative.Set3)
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=title,
                     color_discrete_sequence=["#3498db"])

    fig.update_layout(
        template="plotly_white",
        title_font_size=18,
        title_x=0.5,
        margin=dict(l=20, r=20, t=60, b=20),
        height=400,
    )
    return fig

def create_pie_chart(df, names_col, values_col, title):
    """创建饼图"""
    fig = px.pie(df, names=names_col, values=values_col, title=title,
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(
        title_font_size=18,
        title_x=0.5,
        margin=dict(l=20, r=20, t=60, b=20),
        height=400,
    )
    return fig

def create_scatter_chart(df, x_col, y_col, title, size_col=None, color_col=None, hover_col=None):
    """创建散点图"""
    fig = px.scatter(df, x=x_col, y=y_col, size=size_col, color=color_col,
                     hover_name=hover_col, title=title,
                     color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(
        template="plotly_white",
        title_font_size=18,
        title_x=0.5,
        margin=dict(l=20, r=20, t=60, b=20),
        height=450,
    )
    return fig

def create_gauge_chart(value, title, max_val=100, suffix="%"):
    """创建仪表盘"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 16}},
        number={"suffix": suffix, "font": {"size": 28}},
        gauge={
            "axis": {"range": [0, max_val], "tickwidth": 1},
            "bar": {"color": "#3498db"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#ecf0f1",
            "steps": [
                {"range": [0, max_val * 0.3], "color": "#ffebee"},
                {"range": [max_val * 0.3, max_val * 0.7], "color": "#fff3e0"},
                {"range": [max_val * 0.7, max_val], "color": "#e8f5e9"},
            ],
        }
    ))
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=280,
    )
    return fig

# ========== 表格美化 ==========

def style_dataframe(df, numeric_cols=None):
    """美化DataFrame显示"""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    def color_negative_red(val):
        if isinstance(val, (int, float)):
            color = "#e74c3c" if val > 0 else "#2ecc71" if val < 0 else "black"
            return f"color: {color}; font-weight: bold"
        return ""

    styled = df.style.applymap(color_negative_red, subset=numeric_cols)
    return styled

# ========== 指标卡片 ==========

def metric_card(label, value, delta=None, delta_color="normal"):
    """创建指标卡片"""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.metric(label=label, value=value, delta=delta, delta_color=delta_color)
