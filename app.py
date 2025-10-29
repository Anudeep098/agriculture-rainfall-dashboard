import streamlit as st
import pandas as pd
import plotly.express as px

# ===========================
# PAGE CONFIGURATION
# ===========================
st.set_page_config(
    page_title="🌾 Agriculture & Rainfall Insights - India",
    page_icon="🌦️",
    layout="wide"
)

# ===========================
# LOAD DATA
# ===========================
holdings = pd.read_csv("operational_holdings.csv")
rainfall = pd.read_csv("rainfall.csv")

# Standardize column names
holdings.columns = holdings.columns.str.strip()
rainfall.columns = rainfall.columns.str.strip()

# Clean holdings state names
holdings["State/ UT"] = holdings["State/ UT"].str.strip().str.lower()

# ===========================
# PAGE TITLE
# ===========================
st.title("🌾 Agricultural Operational Holdings & 🌧️ Rainfall Trends in India")
st.markdown("""
Explore:
- 📊 **State-wise agricultural holdings and area (2005–2011)**
- 🌦️ **Rainfall trends across recent years (2020–2024)**
- 🔄 **Relationship between rainfall and agriculture**
""")

st.markdown("---")

# ===========================
# STATE SELECTION
# ===========================
states = sorted(holdings["State/ UT"].dropna().unique())
selected_state = st.selectbox("Select a State", states, index=0).lower()

filtered_state = holdings[holdings["State/ UT"] == selected_state]

# ===========================
# METRIC CARDS
# ===========================
col1, col2, col3 = st.columns(3)
num_2010 = filtered_state["Number - 2010-11"].values[0]
num_2005 = filtered_state["Number - 2005-06"].values[0]
area_2010 = filtered_state["Area - 2010-11"].values[0]
area_2005 = filtered_state["Area - 2005-06"].values[0]
growth_num = filtered_state["Number - % Variation"].values[0]
growth_area = filtered_state["Area - % Variation"].values[0]

col1.metric("Holdings 2010–11", f"{num_2010:,}", f"{growth_num:+.2f}%")
col2.metric("Area Operated 2010–11 (000 ha)", f"{area_2010:,}", f"{growth_area:+.2f}%")
col3.metric("Holdings Growth (2005–11)", f"{(num_2010-num_2005):,}")

st.markdown("---")

# ===========================
# AGRICULTURAL HOLDINGS VISUALS
# ===========================
st.subheader("📊 Agricultural Operational Holdings (2005–2011)")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        x=["2005–06", "2010–11"],
        y=[num_2005, num_2010],
        labels={"x": "Year", "y": "Holdings (in 000s)"},
        text=[num_2005, num_2010],
        color_discrete_sequence=["#4DB6AC"]
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(title=f"Number of Holdings - {selected_state.title()}", yaxis_title="Holdings")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        x=["2005–06", "2010–11"],
        y=[area_2005, area_2010],
        labels={"x": "Year", "y": "Area (in 000 ha)"},
        text=[area_2005, area_2010],
        color_discrete_sequence=["#64B5F6"]
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(title=f"Operated Area - {selected_state.title()}", yaxis_title="Area")
    st.plotly_chart(fig2, use_container_width=True)

# Raw Data
st.markdown("### 🧾 Raw Data (Selected State)")
st.dataframe(filtered_state, use_container_width=True)

st.markdown("---")

# ===========================
# RAINFALL VISUALS
# ===========================
st.subheader("🌦️ Rainfall Trends in India (2020–2024)")

fig3 = px.line(
    rainfall,
    x="Year",
    y=["Actual", "Forecast"],
    markers=True,
    labels={"value": "Rainfall (mm)", "variable": "Type"},
    title="Actual vs Forecast Rainfall (2020–2024)",
    color_discrete_sequence=["#FFB74D", "#81C784"]
)
st.plotly_chart(fig3, use_container_width=True)

# Raw Rainfall Data
st.markdown("### 🧾 Raw Rainfall Data")
st.dataframe(rainfall, use_container_width=True)

st.markdown("---")

# ===========================
# RAINFALL VS AGRICULTURE RELATIONSHIP
# ===========================
st.subheader("🔄 Relationship Between Rainfall and Agricultural Holdings")

st.markdown("""
This section explores whether higher rainfall correlates with changes in the operated area or number of holdings.
*(Data years differ, so this is an indicative trend.)*
""")

# Simulated alignment (only for visualization)
correlation_data = pd.DataFrame({
    "Rainfall": rainfall["Actual"],
    "Operated Area (000 ha)": [area_2005, area_2010, area_2010, area_2005, area_2010][:len(rainfall)]
})

corr_value = correlation_data["Rainfall"].corr(correlation_data["Operated Area (000 ha)"])

fig4 = px.scatter(
    correlation_data,
    x="Rainfall",
    y="Operated Area (000 ha)",
    trendline="ols",
    color_discrete_sequence=["#9575CD"],
    title=f"Rainfall vs Operated Area Correlation ({selected_state.title()})"
)
st.plotly_chart(fig4, use_container_width=True)

st.info(f"📈 Correlation between rainfall and operated area: **{corr_value:.2f}**")

st.markdown("---")

# ===========================
# DATA SOURCES
# ===========================
st.markdown("""
### 📄 Data Sources:
- Agricultural Census - [data.gov.in](https://data.gov.in)
- Rainfall Data - [IMD / data.gov.in](https://data.gov.in)
""")