# 📊 个人投研中心

一个基于 Streamlit 的投研可视化网站，支持股票、基金、宏观经济数据的可视化分析。

## 🚀 快速开始

### 1. 本地运行
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 2. 部署到 Streamlit Cloud（免费）
1. 将代码上传到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接你的 GitHub 仓库
4. 选择 `app.py` 作为主文件
5. 点击 Deploy，免费获得独立网址

## 📁 项目结构

```
.
├── app.py                    # 主入口（首页）
├── pages/                    # 各功能模块页面
│   ├── 1_📈_股票看板.py
│   ├── 2_📊_基金分析.py
│   └── 3_🌍_宏观经济.py
├── data/                     # 【数据后台】用Excel编辑这些文件
│   ├── stocks.csv
│   ├── funds.csv
│   └── macro.csv
├── utils/
│   └── helpers.py            # 公共工具函数
└── requirements.txt          # Python依赖包
```

## 📝 如何更新数据

### 方法一：直接编辑CSV（最简单）
1. 用 Excel 或 WPS 打开 `data/` 文件夹下的 CSV 文件
2. 修改数据，保存
3. 刷新网页即可看到更新

### 方法二：添加新模块
1. 在 `pages/` 文件夹下复制一个现有页面文件
2. 修改文件名（如 `4_📉_债券分析.py`）
3. 修改里面的数据和图表逻辑
4. 在 `data/` 下添加对应的数据文件
5. 在 `app.py` 首页添加模块入口

## 📱 特性

- ✅ 手机端自适应
- ✅ 数据后台自主管理
- ✅ 模块化可扩展
- ✅ 免费部署
- ✅ 交互式图表

## 🔗 在线演示

部署后可获得类似 `https://xxx.streamlit.app` 的独立网址，手机电脑都能访问。

---

**提示**：所有数据均为示例，请替换为你自己的真实投研数据。
