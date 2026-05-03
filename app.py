import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from analysis import analyze_data

# ===============================
# 🎨 PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Employee Analytics",
    layout="wide",
    page_icon="📊"
)

# ===============================
# 🌈 ADVANCED UI STYLING
# ===============================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

/* Titles */
h1, h2, h3 {
    color: white;
    font-weight: 600;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f3c88, #39a2db);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #ff7eb3, #ff758c);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
    padding: 10px;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

</style>
""", unsafe_allow_html=True)

# ===============================
# 🏢 HEADER (HERO SECTION)
# ===============================
st.markdown("""
<div class="glass">
    <h1>📊 Employee Satisfaction Analytics</h1>
    <p>AI-powered insights using NLP & Sentiment Analysis</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# 📂 SIDEBAR
# ===============================
st.sidebar.title("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
use_sample = st.sidebar.button("Use Sample Data")

# ===============================
# 📊 LOAD DATA
# ===============================
if uploaded_file:
    df = pd.read_csv(uploaded_file)
elif use_sample:
    df = pd.read_csv("data/employee_feedback.csv")
else:
    st.warning("Upload a dataset or use sample data.")
    st.stop()

# ===============================
# 🔍 ANALYSIS
# ===============================
df, theme_count, sentiment_count = analyze_data(df)

# ===============================
# 📊 METRICS (CUSTOM CARDS)
# ===============================
total = len(df)
positive = (df['sentiment'] == "Positive").sum()
negative = (df['sentiment'] == "Negative").sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="metric-card">Total Responses<br>{total}</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="metric-card">Positive<br>{(positive/total)*100:.1f}%</div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="metric-card">Negative<br>{(negative/total)*100:.1f}%</div>', unsafe_allow_html=True)

# ===============================
# 🔍 FILTERS
# ===============================
st.sidebar.subheader("🔍 Filters")

selected_sentiment = st.sidebar.multiselect(
    "Sentiment",
    df['sentiment'].unique(),
    default=df['sentiment'].unique()
)

search_text = st.sidebar.text_input("Search Feedback")

filtered_df = df[df['sentiment'].isin(selected_sentiment)]

if search_text:
    filtered_df = filtered_df[
        filtered_df['feedback'].str.contains(search_text, case=False)
    ]

# ===============================
# 📄 DATA TABLE
# ===============================
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("📄 Employee Feedback")
st.dataframe(filtered_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# 📊 VISUALS
# ===============================
col4, col5 = st.columns(2)

with col4:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📊 Theme Distribution")
    fig1, ax1 = plt.subplots()
    ax1.bar(theme_count.keys(), theme_count.values())
    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📈 Sentiment Distribution")
    fig2, ax2 = plt.subplots()
    ax2.pie(sentiment_count.values, labels=sentiment_count.index, autopct='%1.1f%%')
    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# ☁️ WORD CLOUD
# ===============================
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("☁️ Keyword Insights")

text = " ".join(filtered_df['cleaned'])
wc = WordCloud(width=800, height=400, background_color="white").generate(text)

fig3, ax3 = plt.subplots()
ax3.imshow(wc)
ax3.axis("off")
st.pyplot(fig3)
st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# 💡 INSIGHTS
# ===============================
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("💡 Key Insights")

if len(theme_count) > 0:
    top_theme = max(theme_count, key=theme_count.get)
    st.success(f"Primary Concern: {top_theme}")

st.write("• Employee satisfaction is strongly linked to management and work-life balance.")
st.write("• Positive sentiment correlates with team culture and flexibility.")
st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# 📥 DOWNLOAD
# ===============================
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("📥 Export Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Dataset", csv, "employee_data.csv")
st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("🚀 Enterprise Analytics Dashboard | Built with Streamlit")
