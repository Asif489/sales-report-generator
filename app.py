import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# =========================
# TITLE
# =========================
st.title("📊 Sales Report Dashboard")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="latin1")

    # Data preprocessing
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    df['YEAR'] = df['ORDERDATE'].dt.year
    df['MONTH'] = df['ORDERDATE'].dt.month

    # =========================
    # SIDEBAR FILTERS
    # =========================
    st.sidebar.header("🔍 Filters")

    selected_year = st.sidebar.multiselect(
        "Select Year",
        options=df['YEAR'].unique(),
        default=df['YEAR'].unique()
    )

    selected_country = st.sidebar.multiselect(
        "Select Country",
        options=df['COUNTRY'].unique(),
        default=df['COUNTRY'].unique()
    )

    filtered_df = df[
        (df['YEAR'].isin(selected_year)) &
        (df['COUNTRY'].isin(selected_country))
    ]

    # =========================
    # KPIs
    # =========================
    total_sales = filtered_df['SALES'].sum()
    total_orders = filtered_df['ORDERNUMBER'].nunique()
    total_customers = filtered_df['CUSTOMERNAME'].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
    col2.metric("📦 Orders", total_orders)
    col3.metric("👥 Customers", total_customers)

    st.markdown("---")

    # =========================
    # CHARTS
    # =========================

    # Sales by Year
    st.subheader("📅 Sales by Year")
    sales_by_year = filtered_df.groupby('YEAR')['SALES'].sum()
    fig1, ax1 = plt.subplots()
    sales_by_year.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    # Sales by Country
    st.subheader("🌍 Top Countries")
    sales_by_country = filtered_df.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=False).head(10)
    fig2, ax2 = plt.subplots()
    sales_by_country.plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

    # Product Line
    st.subheader("📦 Product Line Performance")
    product_sales = filtered_df.groupby('PRODUCTLINE')['SALES'].sum()
    fig3, ax3 = plt.subplots()
    product_sales.plot(kind='bar', ax=ax3)
    st.pyplot(fig3)

    # Monthly Trend
    st.subheader("📈 Monthly Sales Trend")
    monthly_sales = filtered_df.groupby(['YEAR', 'MONTH'])['SALES'].sum()
    fig4, ax4 = plt.subplots()
    monthly_sales.plot(ax=ax4)
    st.pyplot(fig4)

    # Top Customers
    st.subheader("🏆 Top Customers")
    top_customers = filtered_df.groupby('CUSTOMERNAME')['SALES'].sum().sort_values(ascending=False).head(10)
    st.dataframe(top_customers)

else:
    st.info("👆 Upload the dataset to get started")