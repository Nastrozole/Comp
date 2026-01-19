import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("⚖️ Crypto Regulation Dashboard")
st.markdown("Morocco 2025 Draft vs Global Frameworks")

# Data
countries = ["🇲🇦 Morocco (Draft 2025)", "🇪🇺 EU (MiCA)", "🇦🇪 UAE", "🇸🇬 Singapore"]
scores = [63, 82, 88, 86]
innovation = [42, 72, 95, 85]
protection = [85, 92, 78, 88]
access = [35, 78, 97, 82]

df = pd.DataFrame({
    "Country": countries,
    "Score": scores,
    "Innovation": innovation,
    "Protection": protection,
    "Access": access
})

# Display
st.subheader("📊 Scores")
cols = st.columns(4)
for i in range(4):
    with cols[i]:
        st.metric(countries[i], f"{scores[i]}/100")

st.subheader("📈 Comparison")
st.bar_chart(df.set_index("Country")[["Innovation", "Protection", "Access"]])

st.subheader("📋 Data Table")
st.dataframe(df)

# Morocco analysis
st.subheader("🎯 Morocco Analysis")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Innovation Gap", "42/100", "-53 vs UAE")
with col2:
    st.metric("Protection Strength", "85/100", "+7 vs UAE")
with col3:
    st.metric("Market Access", "35/100", "-62 vs UAE")

st.markdown("""
**Key Insights:**
1. Morocco's draft is conservative (high protection, low innovation)
2. No crypto payments allowed
3. Dual licensing (AMMC + Bank Al-Maghrib)
4. Strong AML/CFT requirements
""")

st.caption("Data sources: Morocco Finance Ministry • EU MiCA • 2025")
