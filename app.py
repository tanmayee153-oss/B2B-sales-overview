import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ================================
# PAGE CONFIGURATION
# ================================

st.set_page_config(
    page_title="Interactive Sales Dashboard",
    layout="wide"
)

st.title("📊 Interactive Sales Dashboard")


# ================================
# FILE UPLOAD
# ================================

st.sidebar.header("Upload Sales Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


# ================================
# MAIN APP
# ================================

if uploaded_file is not None:

    # Load CSV
    df = pd.read_csv(uploaded_file)

    st.success("File Uploaded Successfully!")


    # ================================
    # DATA PREVIEW
    # ================================

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())


    # ================================
    # SIDEBAR FILTERS
    # ================================

    st.sidebar.header("Filters")

    # Region Filter
    if "Region" in df.columns:
        region_filter = st.sidebar.multiselect(
            "Select Region",
            df["Region"].unique()
        )
    else:
        region_filter = []


    # Category Filter
    if "Category" in df.columns:
        category_filter = st.sidebar.multiselect(
            "Select Category",
            df["Category"].unique()
        )
    else:
        category_filter = []


    # Apply Filters
    filtered_df = df.copy()

    if region_filter:
        filtered_df = filtered_df[
            filtered_df["Region"].isin(region_filter)
        ]

    if category_filter:
        filtered_df = filtered_df[
            filtered_df["Category"].isin(category_filter)
        ]


    # ================================
    # KPI CARDS
    # ================================

    st.subheader("📌 Key Performance Indicators")


    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df["Order_ID"].nunique()
    avg_sales = filtered_df["Sales"].mean()


    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"₹{round(total_sales,2)}")
    col2.metric("Total Profit", f"₹{round(total_profit,2)}")
    col3.metric("Total Orders", total_orders)
    col4.metric("Average Sales", f"₹{round(avg_sales,2)}")


    # ================================
    # SALES BY REGION
    # ================================

    if "Region" in filtered_df.columns:

        st.subheader("🌍 Sales by Region")

        fig1, ax1 = plt.subplots()

        region_sales = filtered_df.groupby("Region")["Sales"].sum()

        region_sales.plot(
            kind="bar",
            ax=ax1
        )

        ax1.set_xlabel("Region")
        ax1.set_ylabel("Total Sales")

        st.pyplot(fig1)


    # ================================
    # CATEGORY WISE SALES
    # ================================

    if "Category" in filtered_df.columns:

        st.subheader("📦 Category-wise Sales")

        fig2, ax2 = plt.subplots()

        sns.barplot(
            x="Category",
            y="Sales",
            data=filtered_df,
            ax=ax2
        )

        st.pyplot(fig2)


    # ================================
    # SALES TREND
    # ================================

    if "Order_Date" in filtered_df.columns:

        st.subheader("📈 Sales Trend Over Time")

        filtered_df["Order_Date"] = pd.to_datetime(
            filtered_df["Order_Date"]
        )

        time_sales = filtered_df.groupby("Order_Date")["Sales"].sum()

        fig3, ax3 = plt.subplots()

        ax3.plot(time_sales.index, time_sales.values)

        ax3.set_xlabel("Date")
        ax3.set_ylabel("Sales")

        st.pyplot(fig3)


    # ================================
    # PROFIT VS SALES
    # ================================

    if "Profit" in filtered_df.columns:

        st.subheader("💰 Sales vs Profit")

        fig4, ax4 = plt.subplots()

        sns.scatterplot(
            x="Sales",
            y="Profit",
            data=filtered_df,
            ax=ax4
        )

        st.pyplot(fig4)


    # ================================
    # TOP PRODUCTS
    # ================================

    if "Product" in filtered_df.columns:

        st.subheader("🏆 Top 10 Products by Sales")

        top_products = filtered_df.groupby("Product")["Sales"] \
                                  .sum() \
                                  .sort_values(ascending=False) \
                                  .head(10)

        st.dataframe(top_products)


    # ================================
    # BUSINESS INSIGHTS
    # ================================

    st.subheader("🧠 Business Insights")


    if "Region" in filtered_df.columns:
        best_region = filtered_df.groupby("Region")["Sales"].sum().idxmax()
        st.info(f"📌 Highest Sales Region: {best_region}")


    if "Category" in filtered_df.columns:
        best_category = filtered_df.groupby("Category")["Sales"].sum().idxmax()
        st.info(f"📌 Best Performing Category: {best_category}")


    st.success("Dashboard Generated Successfully!")


# ================================
# NO FILE MESSAGE
# ================================

else:

    st.warning("⚠️ Please Upload a CSV File to Continue.")
