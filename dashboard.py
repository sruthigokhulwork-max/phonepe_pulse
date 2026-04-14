
import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ── Page Config
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    layout="wide"
)
# @st.cache_resource
# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root1702",
#         database="phonepe"
#     )

# def run_query(query):
#     conn = get_connection()
#     return pd.read_sql(query, conn)

def run_query(query):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1702",
            database="phonepe"
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

#Header 
st.title(" PhonePe Pulse - Transaction Insights")
st.markdown("An interactive dashboard analyzing PhonePe transaction data across India")

# Sidebar Filters 
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", [2018, 2019, 2020, 2021, 2022, 2023, 2024])
quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])



# SCENARIO 1 — Transaction Dynamics

st.header("1. Decoding Transaction Dynamics")


# Top 10 states by transaction amount

col1,col2 = st.columns(2)

with col1:
    df1 = run_query(f"""
        SELECT 
        state, 
        SUM(transaction_amount) AS total_amount
        FROM aggregated_transactions
        WHERE year = {year} AND quarter = {quarter}
        GROUP BY state
        ORDER BY total_amount DESC
        LIMIT 10
    """)
    fig1 = px.bar(df1, x="total_amount", y="state", orientation='h',
                    title=f"Top 10 States by Transaction Amount ({year} Q{quarter})",
                    color="total_amount", color_continuous_scale="blues")
    st.plotly_chart(fig1, width='stretch')

# Bottom 10 states by transaction amount
with col2:
    df1 = run_query(f"""
        SELECT 
        state,
        SUM(transaction_amount) AS total_amount
        FROM aggregated_transactions
        WHERE year = {year} AND quarter = {quarter}
        GROUP BY state
        ORDER BY total_amount ASC
        LIMIT 10
    """)
    fig1 = px.bar(df1, x="total_amount", y="state", orientation='h',
                    title=f"Bottom 10 States by Transaction Amount ({year} Q{quarter})",
                    color="total_amount", color_continuous_scale="blues")
    st.plotly_chart(fig1, width='stretch')

# Payment type breakdown per quarter
col3, col4 = st.columns(2)
with col3:
    df2 = run_query(f"""
        SELECT 
        transaction_name, 
        SUM(transaction_count) AS total_count
        FROM aggregated_transactions
        WHERE year = {year} AND quarter = {quarter}
        GROUP BY transaction_name
        ORDER BY total_count DESC
    """)
    fig2 = px.pie(df2, values="total_count", names="transaction_name",
                    title=f"Transaction Type Breakdown ({year} Q{quarter})",
                    color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig2, width='stretch')

# Overall payment type breakdown
with col4:
    df2 = run_query(f"""
        SELECT 
        transaction_name, 
        SUM(transaction_count) AS total_count
        FROM aggregated_transactions
        GROUP BY transaction_name
        ORDER BY total_count DESC
    """)
    fig2 = px.pie(df2, values="total_count", names="transaction_name",
                    title=f"Transaction Type Breakdown for whole data",
                    color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig2, width='stretch')

# Year-wise growth (line chart)
df3 = run_query("""
    SELECT 
    year, 
    SUM(transaction_count) AS total_count
    FROM aggregated_transactions
    GROUP BY year 
    ORDER BY year
""")
fig3 = px.line(df3, x="year", y="total_count",
            title="📈 Year-wise Transaction Growth",
            markers=True, color_discrete_sequence=["#1d4ed8"])
st.plotly_chart(fig3, width='stretch')


# SCENARIO 2 — Device & User Engagement

st.header("2.Device Dominance & User Engagement")


# Top 5 mobile brands

col5,col6 = st.columns(2)

with col5:
    df4 = run_query(f"""
        SELECT
        user_brand, 
        SUM(user_count) AS total_users
        FROM aggregated_users
        WHERE year = {year} AND quarter = {quarter}
        GROUP BY user_brand
        ORDER BY total_users DESC
        LIMIT 5
    """)
    fig4 = px.bar(df4, x="user_brand", y="total_users",
                    title=f"Top Mobile Brands ({year} Q{quarter})",
                    color="total_users", color_continuous_scale="blues")
    st.plotly_chart(fig4, width='stretch')

# Bottom 5 mobile brands

with col6:

    df4 = run_query(f"""
        SELECT 
        user_brand, 
        SUM(user_count) AS total_users
        FROM aggregated_users
        WHERE year = {year} AND quarter = {quarter}
        GROUP BY user_brand
        ORDER BY total_users ASC
        LIMIT 5
    """)
    fig4 = px.bar(df4, x="user_brand", y="total_users",
                    title=f"Bottom  Mobile Brands ({year} Q{quarter})",
                    color="total_users", color_continuous_scale="blues")
    st.plotly_chart(fig4, width='stretch')


# App opens by state
df5 = run_query(f"""
    SELECT 
    state, 
    SUM(user_appopens) AS total_opens
    FROM map_users
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY state
    ORDER BY total_opens DESC
    LIMIT 10
""")
fig5 = px.bar(df5, x="total_opens", y="state", orientation='h',
                title=f"Top States by App Opens ({year} Q{quarter})",
                color="total_opens", color_continuous_scale="blues")
st.plotly_chart(fig5, width='stretch')


# App opens by district
df6 = run_query(f"""
    SELECT 
    state,
    user_district,
    SUM(user_appopens) AS total_appopens
FROM map_users
GROUP BY state, user_district
ORDER BY total_appopens DESC
LIMIT 10;
""")
fig6 = px.bar(df6, x="total_appopens", y="user_district", orientation='h',
                title=f"Top districts by App Opens ({year} Q{quarter})",
                color="total_appopens", color_continuous_scale="blues")
st.plotly_chart(fig6,width='stretch')

# Number of users in each brand
df7 = run_query(f"""
    SELECT
    year,
    user_brand,
    SUM(user_count) AS total_users
FROM aggregated_users
GROUP BY year, user_brand
ORDER BY year ASC, total_users DESC;
LIMIT 10;
""")
fig7 = px.bar(df7, x="total_users", y="user_brand", orientation='h',
                title=f"Number of users in each brand ({year} Q{quarter})",
                color="total_users", color_continuous_scale="blues")
st.plotly_chart(fig7, width='stretch')

# SCENARIO 3 — Insurance Penetration

st.header("3. Insurance Penetration & Growth")

# Insurance growth by year
df8 = run_query(f"""
    SELECT 
    year, 
    SUM(insurance_count) AS total_policies
    FROM aggregated_insurance
    GROUP BY year 
    ORDER BY year
""")
fig8 = px.line(df8, x="year", y="total_policies",
                title="Insurance Growth Over Years",
                markers="True", color_discrete_sequence=["#1d4ed8"])
st.plotly_chart(fig8, width='stretch')


# Insurance growth by quarter

df9 = run_query("""
    SELECT 
    year,
    quarter,
    SUM(insurance_count) AS total_insurance_count
    FROM aggregated_insurance
    GROUP BY year, quarter
    ORDER BY year, quarter;
""")

df9['timeline'] = df9['year'].astype(str) + "-Q" + df9['quarter'].astype(str)

fig9 = px.line(df9, x="timeline", y="total_insurance_count",
                title="Insurance Growth Over quarter",
                markers="True", color_discrete_sequence=["#1d4ed8"])
st.plotly_chart(fig9, width='stretch')


# Top states for insurance

df10 = run_query(f"""
    SELECT 
    state, 
    SUM(insurance_count) AS total_policies
    FROM map_insurance
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY state
    ORDER BY total_policies DESC
    LIMIT 10
""")
fig10 = px.bar(df10, x="total_policies", y="state", orientation='h',
                title=f"Top States by Insurance ({year} Q{quarter})",
                color="total_policies", color_continuous_scale="blues")
st.plotly_chart(fig10, width='stretch')

#Bottom states for insurance

df11 = run_query(f"""
    SELECT
    state, 
    SUM(insurance_count) AS total_policies
    FROM map_insurance
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY state
    ORDER BY total_policies ASC
    LIMIT 10
""")
fig11 = px.bar(df11, x="total_policies", y="state", orientation='h',
                title=f"Bottom States by Insurance ({year} Q{quarter})",
                color="total_policies", color_continuous_scale="blues")
st.plotly_chart(fig11, width='stretch')

# Districts having more insurance policies

df12 = run_query(f"""
    SELECT 
        district_name, 
        SUM(insurance_count) AS total_policies
    FROM map_insurance
    WHERE year = {year} AND quarter = {quarter}
    GROUP BY district_name
    ORDER BY total_policies DESC
    LIMIT 10;
""")

print(df12)
fig12 = px.bar(
    df12, 
    x="total_policies", 
    y="district_name", 
    orientation='h',
    title=f"Top 10 Districts by Insurance Policies ({year} Q{quarter})",
    color="total_policies", 
    color_continuous_scale="blues"
)

st.plotly_chart(fig12, use_container_width=True)

# SCENARIO 4 — Market Expansion

st.header("4. Transaction Analysis for Market Expansion")

#  Top  districts transactions 

df13 = run_query(f"""
    SELECT 
    district_name, 
    SUM(transaction_count) AS total_count
    FROM map_transactions
    WHERE year={year} AND quarter={quarter}
    GROUP BY district_name
    ORDER BY total_count DESC
    LIMIT 10
""")
fig13 = px.bar(df13, x="total_count", y="district_name", orientation='h',
                title=f"Top 10 Districts by Transactions ({year} Q{quarter})",
                color="total_count",
                color_continuous_scale="blues")
st.plotly_chart(fig13, width='stretch')

# Least districts by transactions

df14 = run_query(f"""
    SELECT 
    district_name, 
    SUM(transaction_amount) AS total_amount
    FROM map_transactions
    WHERE year={year} AND quarter={quarter}
    GROUP BY district_name
    ORDER BY total_amount ASC
    LIMIT 10
""")
fig14 = px.bar(df14, x="total_amount", y="district_name", orientation='h',
                title=f"Bottom 10 Districts by Transactions ({year} Q{quarter})",
                color="total_amount",
                color_continuous_scale="blues")
st.plotly_chart(fig14, width='stretch')

#  Top  districts transactions 

df13 = run_query(f"""
    SELECT 
    state, 
    SUM(transaction_count) AS total_count
    FROM map_transactions
    WHERE year={year} AND quarter={quarter}
    GROUP BY state
    ORDER BY total_count DESC
    LIMIT 10
""")
fig13 = px.bar(df13, x="total_count", y="state", orientation='h',
                title=f"Top 10 state by Transactions ({year} Q{quarter})",
                color="total_count",
                color_continuous_scale="blues")
st.plotly_chart(fig13, width='stretch')

# Least districts by transactions

df14 = run_query(f"""
    SELECT 
    state, 
    SUM(transaction_amount) AS total_amount
    FROM map_transactions
    WHERE year={year} AND quarter={quarter}
    GROUP BY state
    ORDER BY total_amount ASC
    LIMIT 10
""")
fig14 = px.bar(df14, x="total_amount", y="state", orientation='h',
                title=f"Bottom 10 state by Transactions ({year} Q{quarter})",
                color="total_amount",
                color_continuous_scale="blues")
st.plotly_chart(fig14, width='stretch')

# Top 10 pincodes by transaction count

df15 = run_query(f"""
    SELECT
    state,
    pincode,
    SUM(transaction_count) AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount
    FROM top_transactions
    GROUP BY state, pincode
    ORDER BY total_transactions DESC
    LIMIT 10;
""")
fig15 = px.bar(df15, x="total_amount", y="pincode", orientation='h',
                title=f"Top pincodes by Transactions ({year} Q{quarter})",
                color="total_amount",
                color_continuous_scale="blues")
st.plotly_chart(fig15, width='stretch')
st.markdown("---")


# # SCENARIO 5 — User Engagement & Growth Strategy

st.header("5. User Engagement & Growth Strategy")

# top users vs app opens by state

df16 = run_query(f"""
    SELECT state,
            SUM(user_registered) AS total_users,
            SUM(user_appopens) AS total_opens
    FROM map_users
    WHERE year={year} AND quarter={quarter}
    GROUP BY state
    ORDER BY total_users DESC
    LIMIT 5
""")
fig16 = px.scatter(df16, x="total_users", y="total_opens",
                    text="state",
                    title="Top Users vs App Opens by State",
                    color="total_opens",
                    color_continuous_scale="blues",
                    labels={"total_users":"Registered Users",
                            "total_opens":"App Opens"})
fig16.update_traces(textposition='top center')
st.plotly_chart(fig16, width='stretch')

# bottom users vs app opens by state
df17 = run_query(f"""
    SELECT state,
            SUM(user_registered) AS total_users,
            SUM(user_appopens) AS total_opens
    FROM map_users
    WHERE year={year} AND quarter={quarter}
    GROUP BY state
    ORDER BY total_users ASC
    LIMIT 5
""")
fig17 = px.scatter(df17, x="total_users", y="total_opens",
                    text="state",
                    title="Bottom Users vs App Opens by State",
                    color="total_opens",
                    color_continuous_scale="blues",
                    labels={"total_users":"Registered Users",
                            "total_opens":"App Opens"})
fig17.update_traces(textposition='top center')
st.plotly_chart(fig17, width='stretch')

# Top ten states by registered users
df18 = run_query(f"""
    SELECT state, SUM(registered_users) AS total_users
    FROM top_users
    WHERE year={year} AND quarter={quarter}
    GROUP BY state
    ORDER BY total_users DESC
    LIMIT 10
""")
fig18 = px.bar(df18, x="state", y="total_users",
                title=f"Top 10 States by Registered Users ({year} Q{quarter})",
                color="total_users",
                color_continuous_scale="blues",
                labels={"total_users":"Users","state":"State"})
st.plotly_chart(fig18, width='stretch')


# Bottom 10 states by registered users
df19 = run_query(f"""
    SELECT state, SUM(registered_users) AS total_users
    FROM top_users
    WHERE year={year} AND quarter={quarter}
    GROUP BY state
    ORDER BY total_users ASC
    LIMIT 10
""")
fig19 = px.bar(df19, x="state", y="total_users",
                title=f"Bottom 10 States by Registered Users ({year} Q{quarter})",
                color="total_users",
                color_continuous_scale="blues",
                labels={"total_users":"Users","state":"State"})
st.plotly_chart(fig19, width='stretch')



st.markdown("---")



# MAPPING 

# # States vs Total Transaction
# st.header("States VS Total Transactions")

# state_mapping = {
#     "andaman-&-nicobar-islands": "Andaman & Nicobar",
#     "arunachal-pradesh" : "Arunachal Pradesh",
#     "assam" : "Assam",
#     "chandigarh" : "Chandigarh",
#     "tamil-nadu": "Tamil Nadu",
#     "karnataka" : "Karnataka",
#     "manipur" : "Manipur",
#     "meghalaya" : "Meghalaya",
#     "mizoram" : "Mizoram",
#     "nagaland" : "Nagaland",
#     "punjab" : "Punjab",
#     "rajasthan" : "Rajasthan",
#     "sikkim" : "Sikkim",
#     "tripura" : "Tripura",
#     "uttarakhand" : "Uttarakhand",
#     "telangana" : "Telangana",
#     "bihar" : "Bihar",
#     "kerala" : "Kerala",
#     "madhya-pradesh" : "Madhya Pradesh",
#     "gujarat" : "Gujarat",
#     "lakshadweep" : "Lakshadweep",
#     "odisha" : "Odisha",
#     "dadra-&-nagar-haveli-&-daman-&-diu" : "Dadra and Nagar Haveli and Daman and Diu",
#     "ladakh" : "Ladakh",
#     "jammu-&-kashmir" : "Jammu & Kashmir",
#     "chhattisgarh" : "Chhattisgarh",
#     "delhi" : "Delhi",
#     "goa" : "Goa",
#     "haryana" : "Haryana",
#     "himachal Pradesh" : "Himachal Pradesh",
#     "jharkhand" : "Jharkhand",
#     "tamil-nadu" : "Tamil Nadu",
#     "uttar-pradesh" : "Uttar Pradesh",
#     "west-bengal" : "West Bengal",
#     "andhra-pradesh" : "Andhra Pradesh",
#     "puducherry" : "Puducherry",
#     "maharashtra" : "Maharashtra",
# }

# df = run_query(f'''
#                SELECT state, 
#                SUM(transaction_count) AS total_transactions
#                FROM aggregated_transactions
#                WHERE year={year} AND quarter={quarter}
#                GROUP BY state
#                ''')
# df['state'] = df['state'].replace(state_mapping)
# fig = px.choropleth(
#     df,
#     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#     featureidkey='properties.ST_NM',
#     locations='state',
#     color='total_transactions',
#     color_continuous_scale='Blues'
# )

# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(height=600)
# st.plotly_chart(fig, use_container_width=True)

# st.markdown("---")

# st.header("State VS Total Insurance")


# df = run_query(f'''
#                SELECT state, 
#                SUM(insurance_count) AS total_insured
#                FROM aggregated_insurance
#                WHERE year={year} AND quarter={quarter}
#                GROUP BY state
#                ''')
# df['state'] = df['state'].replace(state_mapping)

# fig = px.choropleth(
#     df,
#     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#     featureidkey='properties.ST_NM',
#     locations='state',
#     color='total_insured',
#     color_continuous_scale='Blues'
# )

# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(height=600)
# st.plotly_chart(fig, use_container_width=True)

# st.markdown("---")

# st.header("State VS Total Users")


# df = run_query(f'''
#                SELECT state, 
#                SUM(user_count) AS total_users
#                FROM aggregated_users
#                WHERE year={year} AND quarter={quarter}
#                GROUP BY state
#                ''')
# df['state'] = df['state'].replace(state_mapping)

# fig = px.choropleth(
#     df,
#     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#     featureidkey='properties.ST_NM',
#     locations='state',
#     color='total_users',
#     color_continuous_scale='Blues'
# )

# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(height=600)
# st.plotly_chart(fig, use_container_width=True)


# st.markdown("Built using Streamlit | Data: PhonePe Pulse GitHub")
