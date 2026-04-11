import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ── Page Config ──────────────────────────────
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    layout="wide"
)

# ── Connect to MySQL ─────────────────────────
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1702",
        database="phonepe"
    )

def run_query(query):
    conn = get_connection()
    return pd.read_sql(query, conn)

# ── Header ───────────────────────────────────
st.title(" PhonePe Pulse - Transaction Insights")
st.markdown("An interactive dashboard analyzing PhonePe transaction data across India")

# ── Sidebar Filters ──────────────────────────
st.sidebar.header("🔍 Filters")
year = st.sidebar.selectbox("Select Year", [2018, 2019, 2020, 2021, 2022, 2023, 2024])
quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])

# ════════════════════════════════════════════
# SCENARIO 1 — Transaction Dynamics
# ════════════════════════════════════════════
st.header("1️⃣ Decoding Transaction Dynamics")


# Top 10 states by transaction amount
df1 = run_query(f"""
    SELECT state, SUM(transaction_amount) AS total_amount
    FROM aggregated_transactions
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY state
    ORDER BY total_amount DESC
    LIMIT 10
""")
fig1 = px.bar(df1, x="total_amount", y="state", orientation='h',
                title=f"Top 10 States by Transaction Amount ({year} Q{quarter})",
                color="total_amount", color_continuous_scale="blues")
st.plotly_chart(fig1, use_container_width=True)

# Payment type breakdown
df2 = run_query(f"""
    SELECT transaction_name, SUM(transaction_count) AS total_count
    FROM aggregated_transactions
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY transaction_name
    ORDER BY total_count DESC
""")
fig2 = px.pie(df2, values="total_count", names="transaction_name",
                title=f"Transaction Type Breakdown ({year} Q{quarter})",
                color_discrete_sequence=px.colors.sequential.Blues_r)
st.plotly_chart(fig2, use_container_width=True)

# Year-wise growth (line chart)
df3 = run_query("""
    SELECT year, SUM(transaction_count) AS total_count
    FROM aggregated_transactions
    GROUP BY year 
    ORDER BY year
""")
fig3 = px.line(df3, x="year", y="total_count",
            title="📈 Year-wise Transaction Growth",
            markers=True, color_discrete_sequence=["#1d4ed8"])
st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════
# SCENARIO 2 — Device & User Engagement
# ════════════════════════════════════════════
st.header("2️⃣ Device Dominance & User Engagement")


# Top mobile brands
df4 = run_query(f"""
    SELECT user_brand, SUM(user_count) AS total_users
    FROM aggregated_users
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY user_brand
    ORDER BY total_users DESC
    LIMIT 10
""")
fig4 = px.bar(df4, x="user_brand", y="total_users",
                title=f"Top Mobile Brands ({year} Q{quarter})",
                color="total_users", color_continuous_scale="blues")
st.plotly_chart(fig4, use_container_width=True)


# App opens by state
df5 = run_query(f"""
    SELECT state, SUM(user_appopens) AS total_opens
    FROM map_users
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY state
    ORDER BY total_opens DESC
    LIMIT 10
""")
fig5 = px.bar(df5, x="total_opens", y="state", orientation='h',
                title=f"Top States by App Opens ({year} Q{quarter})",
                color="total_opens", color_continuous_scale="blues")
st.plotly_chart(fig5, use_container_width=True)


# ════════════════════════════════════════════
# SCENARIO 3 — Insurance Penetration
# ════════════════════════════════════════════
st.header("3️⃣ Insurance Penetration & Growth")



# Insurance growth by year
df6 = run_query("""
    SELECT year, SUM(insurance_count) AS total_policies
    FROM aggregated_insurance
    GROUP BY year ORDER BY year
""")
fig6 = px.line(df6, x="year", y="total_policies",
                title="📈 Insurance Growth Over Years",
                markers=True, color_discrete_sequence=["#1d4ed8"])
st.plotly_chart(fig6, use_container_width=True)


# Top states for insurance
df7 = run_query(f"""
    SELECT state, SUM(insurance_count) AS total_policies
    FROM map_insurance
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY state
    ORDER BY total_policies DESC
    LIMIT 10
""")
fig7 = px.bar(df7, x="total_policies", y="state", orientation='h',
                title=f"Top States by Insurance ({year} Q{quarter})",
                color="total_policies", color_continuous_scale="blues")
st.plotly_chart(fig7, use_container_width=True)

# ════════════════════════════════════════════════════════
# SCENARIO 4 — Market Expansion
# ════════════════════════════════════════════════════════
st.header("4️⃣ Transaction Analysis for Market Expansion")



df = run_query(f"""
    SELECT district_name, SUM(transaction_count) AS total_count
    FROM map_transactions
    WHERE year={year} AND quarter={quarter}
    GROUP BY district_name
    ORDER BY total_count DESC
    LIMIT 10
""")
fig = px.bar(df, x="total_count", y="district_name", orientation='h',
                title=f"Top 10 Districts by Transactions ({year} Q{quarter})",
                color="total_count",
                color_continuous_scale="blues",
                labels={"total_count":"Transactions","district_name":"District"})
st.plotly_chart(fig, use_container_width=True)


df = run_query(f"""
    SELECT district_name, SUM(transaction_amount) AS total_amount
    FROM map_transactions
    WHERE year={year} AND quarter={quarter}
    GROUP BY district_name
    ORDER BY total_amount ASC
    LIMIT 10
""")
fig = px.bar(df, x="total_amount", y="district_name", orientation='h',
                title=f"Bottom 10 Districts (Expansion Opportunities)",
                color="total_amount",
                color_continuous_scale="blues",
                labels={"total_amount":"Amount (₹)","district_name":"District"})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════════════
# SCENARIO 5 — User Engagement & Growth Strategy
# ════════════════════════════════════════════════════════
st.header("5️⃣ User Engagement & Growth Strategy")



df = run_query(f"""
    SELECT state,
            SUM(user_registered) AS total_users,
            SUM(user_appopens) AS total_opens
    FROM map_users
    WHERE year={year} AND quarter={quarter}
    GROUP BY state
    ORDER BY total_users DESC
    LIMIT 10
""")
fig = px.scatter(df, x="total_users", y="total_opens",
                    text="state",
                    title="Users vs App Opens by State",
                    color="total_opens",
                    color_continuous_scale="blues",
                    labels={"total_users":"Registered Users",
                            "total_opens":"App Opens"})
fig.update_traces(textposition='top center')
st.plotly_chart(fig, use_container_width=True)


df = run_query(f"""
    SELECT state, SUM(registered_users) AS total_users
    FROM top_users
    WHERE year={year} AND quarter={quarter}
    GROUP BY state
    ORDER BY total_users DESC
    LIMIT 10
""")
fig = px.bar(df, x="state", y="total_users",
                title=f"Top 10 States by Registered Users ({year} Q{quarter})",
                color="total_users",
                color_continuous_scale="blues",
                labels={"total_users":"Users","state":"State"})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# # ════════════════════════════════════════════════════════
# # SCENARIO 6 — Insurance Engagement
# # ════════════════════════════════════════════════════════
# st.header("6️⃣ Insurance Engagement Analysis")

# col11, col12 = st.columns(2)

# with col11:
#     df = run_query(f"""
#         SELECT district_name, SUM(insurance_count) AS total_policies
#         FROM map_insurance
#         WHERE year={year} AND quarter={quarter}
#         GROUP BY district_name
#         ORDER BY total_policies DESC
#         LIMIT 10
#     """)
#     fig = px.bar(df, x="total_policies", y="district_name", orientation='h',
#                  title=f"Top 10 Districts by Insurance ({year} Q{quarter})",
#                  color="total_policies",
#                  color_continuous_scale="blues",
#                  labels={"total_policies":"Policies","district_name":"District"})
#     st.plotly_chart(fig, use_container_width=True)

# with col12:
#     df = run_query(f"""
#         SELECT state,
#                SUM(insurance_count)  AS total_count,
#                SUM(insurance_amount) AS total_amount
#         FROM map_insurance
#         WHERE year={year} AND quarter={quarter}
#         GROUP BY state
#         ORDER BY total_count DESC
#     """)
#     fig = px.scatter(df, x="total_count", y="total_amount",
#                      text="state",
#                      title="Insurance Count vs Amount by State",
#                      color="total_amount",
#                      color_continuous_scale="blues",
#                      labels={"total_count":"Insurance Count",
#                              "total_amount":"Amount (₹)"})
#     fig.update_traces(textposition='top center')
#     st.plotly_chart(fig, use_container_width=True)

# ── Footer ───────────────────────────────────────────────
st.markdown("---")
st.markdown("Built using Streamlit | Data: PhonePe Pulse GitHub")
