import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from analysis import analyze_data

st.set_page_config(page_title="Employee Satisfaction Analyzer", layout="wide")

# 🎨 Title
st.title("🧠 Employee Satisfaction Analysis Dashboard")
st.markdown("### Grounded Theory + NLP Insights")

# 📂 Sidebar
st.sidebar.header("⚙️ Options")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

use_sample = st.sidebar.button("Use Sample Data")

# 📊 Load Data
if uploaded_file:
    df = pd.read_csv(uploaded_file)

elif use_sample:
    df = pd.read_csv("data/employee_feedback.csv")

else:
    st.info("👈 Upload a CSV file or use sample data to begin")
    st.stop()

# 🔍 Analyze
df, theme_count, sentiment_count = analyze_data(df)

# ===============================
# 📊 METRICS
# ===============================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total = len(df)
positive = (df['sentiment'] == "Positive").sum()
negative = (df['sentiment'] == "Negative").sum()

col1.metric("Total Responses", total)
col2.metric("Positive %", round((positive/total)*100, 2))
col3.metric("Negative %", round((negative/total)*100, 2))

# ===============================
# 📄 DATA VIEW
# ===============================
st.subheader("📄 Processed Data")
st.dataframe(df)

# ===============================
# 📊 CHARTS
# ===============================
col4, col5 = st.columns(2)

# Theme chart
with col4:
    st.subheader("📊 Theme Analysis")
    fig1, ax1 = plt.subplots()
    ax1.bar(theme_count.keys(), theme_count.values())
    ax1.set_xlabel("Factors")
    ax1.set_ylabel("Frequency")
    st.pyplot(fig1)

# Sentiment chart
with col5:
    st.subheader("😊 Sentiment Analysis")
    fig2, ax2 = plt.subplots()
    ax2.pie(sentiment_count.values, labels=sentiment_count.index, autopct='%1.1f%%')
    st.pyplot(fig2)

# ===============================
# ☁️ WORD CLOUD
# ===============================
st.subheader("☁️ Word Cloud")

text = " ".join(df['cleaned'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

fig3, ax3 = plt.subplots()
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis("off")
st.pyplot(fig3)

# ===============================
# 💡 INSIGHTS
# ===============================
st.subheader("💡 Insights")

top_theme = max(theme_count, key=theme_count.get)

st.success(f"🔹 Most common issue: {top_theme}")
st.write("🔹 Negative feedback is often linked to workload and management.")
st.write("🔹 Improving work-life balance can increase satisfaction.")
st.write("🔹 Positive sentiment is driven by good team culture and flexibility.")

# ===============================
# 🎯 FOOTER
# ===============================
st.markdown("---")
st.markdown("🚀 Built with Streamlit | NLP + Grounded Theory Project")