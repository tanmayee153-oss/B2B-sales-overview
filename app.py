import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ================================
# PAGE CONFIG
# ================================

st.set_page_config(
    page_title="Interactive Dashboard",
    layout="wide"
)

st.title("📊 Interactive Business Dashboard")


# ================================
# FILE UPLOAD
# ================================

st.sidebar.header("Upload Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


# ================================
# MAIN APP
# ================================

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("File Uploaded Successfully!")


    # ================================
    # DATA PREVIEW
    # ================================

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())


    # ================================
    # COLUMN SELECTION
    # ================================

    st.sidebar.header("Select Columns")


    numeric_cols = df.select_dtypes(include=["int64","float64"]).columns.tolist()


    if len(numeric_cols) == 0:
        st.error("No numeric columns found in file.")
        st.stop()


    sales_col = st.sidebar.selectbox(
        "Select Sales / Revenue Column",
        numeric_cols
    )


    profit_col = st.sidebar.selectbox(
        "Select Profit Column (Optional)",
        ["None"] + numeric_cols
    )


    region_col = st.sidebar.selectbox(
        "Select Region Column (Optional)",
        ["None"] + df.columns.tolist()
    )


    category_col = st.sidebar.selectbox(
        "Select Category Column (Optional)",
        ["None"] + df.columns.tolist()
    )


    # ================================
    # FILTERS
    # ================================

    filtered_df = df.copy()


    if region_col != "None":

        regions = st.sidebar.multiselect(
            "Filter Region",
            df[region_col].unique()
        )

        if regions:
            filtered_df = filtered_df[
                filtered_df[region_col].isin(regions)
            ]


    if category_col != "None":

        categories = st.sidebar.multiselect(
            "Filter Category",
            df[category_col].unique()
        )

        if categories:
            filtered_df = filtered_df[
                filtered_df[category_col].isin(categories)
            ]


    # ================================
    # KPI SECTION
    # ================================

    st.subheader("📌 Key Performance Indicators")


    total_sales = filtered_df[sales_col].sum()

    avg_sales = filtered_df[sales_col].mean()


    if profit_col != "None":
        total_profit = filtered_df[profit_col].sum()
    else:
        total_profit = 0


    col1, col2, col3 = st.columns(3)


    col1.metric("Total Value", round(total_sales,2))

    col2.metric("Average Value", round(avg_sales,2))

    col3.metric("Total Profit", round(total_profit,2))


    # ================================
    # BAR CHART
    # ================================

    if region_col != "None":

        st.subheader("🌍 Value by Region")

        fig1, ax1 = plt.subplots()

        region_data = filtered_df.groupby(region_col)[sales_col].sum()

        region_data.plot(kind="bar", ax=ax1)

        st.pyplot(fig1)


    # ================================
    # CATEGORY CHART
    # ================================

    if category_col != "None":

        st.subheader("📦 Category Analysis")

        fig2, ax2 = plt.subplots()

        sns.barplot(
            x=category_col,
            y=sales_col,
            data=filtered_df,
            ax=ax2
        )

        st.pyplot(fig2)


    # ================================
    # SCATTER PLOT
    # ================================

    if profit_col != "None":

        st.subheader("💰 Value vs Profit")

        fig3, ax3 = plt.subplots()

        sns.scatterplot(
            x=sales_col,
            y=profit_col,
            data=filtered_df,
            ax=ax3
        )

        st.pyplot(fig3)


    # ================================
    # TOP RECORDS
    # ================================

    st.subheader("🏆 Top 10 Records")

    top10 = filtered_df.sort_values(
        by=sales_col,
        ascending=False
    ).head(10)

    st.dataframe(top10)


    # ================================
    # INSIGHTS
    # ================================

    st.subheader("🧠 Auto Insights")


    st.info(f"📌 Highest Value: {round(filtered_df[sales_col].max(),2)}")

    st.info(f"📌 Lowest Value: {round(filtered_df[sales_col].min(),2)}")

    st.info(f"📌 Average Value: {round(avg_sales,2)}")


    st.success("Dashboard Generated Successfully!")


else:

    st.warning("Please Upload a CSV File to Start")
