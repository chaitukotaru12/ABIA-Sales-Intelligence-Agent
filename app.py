
import html
from pathlib import Path

import pandas as pd
import streamlit as st

from src.bi_agent.orchestrator import SalesIntelligenceAgent


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ABIA | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM DESIGN SYSTEM
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #4169e1;
        --purple: #7856d8;
        --ink: #17233f;
        --muted: #64748b;
        --border: #e5eaf3;
        --surface: #ffffff;
        --background: #f5f7fc;
    }

    html, body, [class*="css"], p, label, span, div {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--background);
        color: var(--ink);
    }

    [data-testid="stAppViewContainer"] {
        background: var(--background);
    }

    [data-testid="stHeader"] {
        background: rgba(245,247,252,0.95);
    }

    [data-testid="stMain"] {
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: #263451 !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: #f7f9ff;
        border: 1px dashed #bdc9e8;
        border-radius: 12px;
        padding: 10px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--ink) !important;
        font-weight: 700 !important;
        letter-spacing: -0.4px;
    }

    p, li, label, .stMarkdown, .stCaption {
        color: #40506d;
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    [data-testid="stMetricValue"] {
        color: #17233f !important;
    }

    [data-testid="stFileUploader"] {
        color: #263451 !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    .abia-header {
        background: linear-gradient(110deg, #24418e 0%, #4269d9 55%, #7655d6 100%);
        border-radius: 18px;
        padding: 25px 30px;
        color: #ffffff !important;
        margin-bottom: 22px;
        box-shadow: 0 9px 24px rgba(53, 81, 170, 0.16);
    }

    .abia-header h1 {
        color: #ffffff !important;
        font-size: 30px;
        font-weight: 800;
        margin: 0;
    }

    .abia-header p {
        color: #e9eeff !important;
        font-size: 14px;
        margin: 7px 0 0 0;
    }

    .eyebrow {
        color: #5471c9 !important;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.3px;
        margin-bottom: 8px;
    }

    .welcome-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 14px rgba(30, 50, 90, 0.04);
        margin-bottom: 22px;
    }

    .welcome-card h2 {
        color: var(--ink) !important;
        font-size: 23px;
        margin: 0 0 8px 0;
    }

    .welcome-card p {
        color: var(--muted) !important;
        margin: 0;
        line-height: 1.6;
    }

    .feature-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 19px;
        min-height: 135px;
        box-shadow: 0 4px 12px rgba(30, 50, 90, 0.035);
    }

    .feature-icon {
        font-size: 23px;
        margin-bottom: 12px;
    }

    .feature-title {
        color: #1e2c4b !important;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .feature-description {
        color: #64748b !important;
        font-size: 12px;
        line-height: 1.5;
    }

    .section-title {
        color: #1d2b49 !important;
        font-size: 20px;
        font-weight: 750;
        margin: 22px 0 14px 0;
    }

    .kpi-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 19px;
        min-height: 120px;
        box-shadow: 0 4px 13px rgba(30, 50, 90, 0.045);
    }

    .kpi-card.blue { border-top: 4px solid #4777eb; }
    .kpi-card.purple { border-top: 4px solid #8963df; }
    .kpi-card.teal { border-top: 4px solid #18a58e; }
    .kpi-card.orange { border-top: 4px solid #ed9b45; }

    .kpi-label {
        color: #687791 !important;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }

    .kpi-value {
        color: #192746 !important;
        font-size: 24px;
        font-weight: 800;
        overflow-wrap: anywhere;
    }

    .surface-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 18px;
        box-shadow: 0 4px 13px rgba(30, 50, 90, 0.035);
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 13px;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #4169e1, #7656d8);
        color: #ffffff !important;
        border: 0;
        border-radius: 10px;
        min-height: 45px;
        font-weight: 700;
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(100deg, #3158ce, #6844c9);
        color: #ffffff !important;
        border: 0;
    }

    div.stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid #cbd6ef;
        color: #3456aa !important;
        background: #f7f9ff;
        font-weight: 600;
    }

    [data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: #e4e9f2;
    }

    .footer {
        color: #94a0b5 !important;
        text-align: center;
        font-size: 11px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="abia-header">
        <h1>📊 ABIA</h1>
        <p>Autonomous Business Intelligence Agent
        &nbsp; · &nbsp; Local AI &nbsp; · &nbsp; Qwen3 + Python + Pandas</p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 📂 Workspace")
    st.caption("Your business intelligence workspace")

    uploaded_file = st.file_uploader(
        "Upload your sales CSV",
        type=["csv"],
        help="ABIA detects common sales column names automatically."
    )

    st.divider()

    st.markdown("### 🧠 Agent Components")

    st.markdown(
        """
        **01 · Planner**
        
        Qwen3 analysis planning

        **02 · Executor**

        Python and Pandas tools

        **03 · Critic**

        Evidence validation

        **04 · Reporter**

        Business report generation
        """
    )

    st.divider()

    st.caption("ABIA · Local AI Business Intelligence")


# --------------------------------------------------
# WELCOME SCREEN
# --------------------------------------------------

if uploaded_file is None:

    st.markdown(
        """
        <div class="welcome-card">
            <div class="eyebrow">YOUR AI-POWERED ANALYTICS WORKSPACE</div>
            <h2>Turn business data into better decisions.</h2>
            <p>
                Upload a sales dataset to explore performance, discover
                trends, and ask your own AI business analyst questions.
                ABIA plans analyses, executes approved tools, reviews
                evidence, and generates reports.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">What you can do with ABIA</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)

    features = [
        (
            f1,
            "📈",
            "Explore performance",
            "Track revenue, products, regions and monthly trends."
        ),
        (
            f2,
            "🤖",
            "Ask your AI analyst",
            "Ask business questions in natural language."
        ),
        (
            f3,
            "🛡️",
            "Validate the evidence",
            "Review findings before generating business reports."
        )
    ]

    for column, icon, title, description in features:

        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div class="footer">
            ABIA · Autonomous Business Intelligence Agent
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# DATASET APPLICATION
# --------------------------------------------------

else:

    try:

        data_directory = Path("data/uploads")
        data_directory.mkdir(parents=True, exist_ok=True)

        file_path = data_directory / "uploaded_sales.csv"
        file_path.write_bytes(uploaded_file.getvalue())

        with st.spinner("Preparing your dataset..."):

            agent = SalesIntelligenceAgent(
                data_path=str(file_path)
            )

        analyzer = agent.analyzer
        overview = analyzer.get_overview()
        quality = analyzer.get_data_quality()

        st.markdown(
            '<div class="section-title">📁 Dataset Overview</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="surface-card">
                <strong>📄 {html.escape(uploaded_file.name)}</strong>
                <p style="color:#64748b; font-size:12px; margin:7px 0 0 0;">
                    {quality['total_records']:,} source records
                    &nbsp; · &nbsp;
                    {quality['valid_records']:,} valid records
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --------------------------------------------------
        # KPI CARDS
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">✨ Business Performance</div>',
            unsafe_allow_html=True
        )

        kpi_values = [
            (
                "TOTAL REVENUE",
                f"{overview['total_revenue']:,.2f}",
                "blue"
            ),
            (
                "QUANTITY SOLD",
                f"{overview['total_quantity']:,.0f}",
                "purple"
            ),
            (
                "VALID RECORDS",
                f"{quality['valid_records']:,}",
                "teal"
            ),
            (
                "AVG. REVENUE / RECORD",
                f"{overview['average_transaction_value']:,.2f}",
                "orange"
            )
        ]

        columns = st.columns(4)

        for column, (label, value, style) in zip(columns, kpi_values):

            with column:
                st.markdown(
                    f"""
                    <div class="kpi-card {style}">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.caption(
            "Revenue is displayed in the source dataset's currency or "
            "units. Average revenue per record is not necessarily average "
            "order value."
        )

        # --------------------------------------------------
        # COLUMN MAPPING AND DATA PREVIEW
        # --------------------------------------------------

        with st.expander("🔗 View automatic CSV column mapping"):

            mapping_rows = [
                {
                    "ABIA Field": field,
                    "Detected CSV Column": source
                }
                for field, source in analyzer.column_mapping.items()
                if source is not None
            ]

            st.dataframe(
                pd.DataFrame(mapping_rows),
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"Revenue calculation: {analyzer.revenue_calculation}"
            )

        with st.expander("👀 Preview standardized dataset"):

            st.dataframe(
                analyzer.df.head(100),
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # ANALYTICS
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">📊 Sales Analytics</div>',
            unsafe_allow_html=True
        )

        chart1, chart2 = st.columns(2)

        with chart1:

            st.markdown("#### 🏆 Revenue by Product")

            product_chart = (
                analyzer.revenue_by_product()
                .rename("Revenue")
                .to_frame()
            )

            st.bar_chart(product_chart, color="#4777EB")

        with chart2:

            st.markdown("#### 🌍 Revenue by Region")

            region_chart = (
                analyzer.revenue_by_region()
                .rename("Revenue")
                .to_frame()
            )

            st.bar_chart(region_chart, color="#17A58B")

        st.markdown("#### 📅 Monthly Revenue Trend")

        monthly_chart = (
            analyzer.monthly_revenue()
            .rename("Revenue")
            .to_frame()
        )

        monthly_chart.index = monthly_chart.index.astype(str)

        st.line_chart(monthly_chart, color="#8656DC")

        # --------------------------------------------------
        # DATA QUALITY
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">🛡️ Data Quality Monitor</div>',
            unsafe_allow_html=True
        )

        q1, q2, q3, q4 = st.columns(4)

        q1.metric("Source Records", f"{quality['total_records']:,}")
        q2.metric("Valid Records", f"{quality['valid_records']:,}")
        q3.metric("Missing Values", f"{quality['missing_values']:,}")
        q4.metric("Invalid Rows Removed", f"{quality['invalid_rows_removed']:,}")

        st.metric("Duplicate Rows", f"{quality['duplicate_rows']:,}")

        if (
            quality["missing_values"] == 0
            and quality["invalid_rows_removed"] == 0
            and quality["duplicate_rows"] == 0
        ):
            st.success("Dataset passed the current data quality checks.")
        else:
            st.warning(
                "Data quality issues detected. Review before interpreting results."
            )

        # --------------------------------------------------
        # AI ANALYSIS
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">🤖 Ask ABIA</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="surface-card">
                <strong>Your AI Business Analyst</strong>
                <p style="color:#64748b; font-size:13px;">
                    Ask a question. ABIA will plan, execute, review and report.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        question = st.text_area(
            "What would you like to understand?",
            placeholder="Which product generated the highest revenue?",
            height=100,
            key="abia_business_question"
        )

        if st.button(
            "🚀 Run AI Analysis",
            type="primary",
            use_container_width=True
        ):

            if not question.strip():

                st.warning("Please enter a business question.")

            else:

                try:

                    with st.spinner(
                        "ABIA is planning, executing and reviewing..."
                    ):

                        response = agent.run(question)

                    st.success("Analysis completed successfully!")

                    with st.expander("🧠 View AI Analysis Plan"):

                        st.json(response["plan"])

                    st.markdown("### ⚙️ Tool Execution Results")

                    for tool_name, result in response["results"].items():

                        with st.expander(
                            tool_name.replace("_", " ").title()
                        ):

                            if isinstance(result, dict):

                                st.dataframe(
                                    pd.DataFrame(
                                        list(result.items()),
                                        columns=["Category", "Value"]
                                    ),
                                    use_container_width=True,
                                    hide_index=True
                                )

                            else:
                                st.write(result)

                    st.markdown("### 🛡️ Critic Review")

                    review = response["review"]

                    if review["approved"]:
                        st.success("Analysis approved by ABIA Critic.")
                    else:
                        st.error("Analysis rejected by ABIA Critic.")

                    if review.get("issues"):

                        for issue in review["issues"]:
                            st.warning(issue)

                    if review.get("findings"):

                        st.markdown("#### Verified Findings")
                        st.json(review["findings"])

                    st.markdown("### 📄 Business Report")

                    st.text(response["report"])

                    st.download_button(
                        label="⬇️ Download Business Report",
                        data=response["report"],
                        file_name="ABIA_Sales_Report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                except Exception as analysis_error:

                    st.error(
                        f"ABIA could not complete the analysis: "
                        f"{analysis_error}"
                    )

    except Exception as error:

        st.error(f"Unable to process this dataset: {error}")

        st.info(
            "Check that your CSV contains recognizable date, product, "
            "region, quantity and revenue or unit-price columns."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        ABIA · Autonomous Business Intelligence Agent
        · Built with Python, Pandas, Streamlit and Qwen3
    </div>
    """,
    unsafe_allow_html=True
)
