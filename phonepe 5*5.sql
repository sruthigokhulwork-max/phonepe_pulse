
-- PhonePe Pulse — Business Case Study SQL Queries
USE phonepe;


-- CASE STUDY 1: Decoding Transaction Dynamics
-- Scenario: PhonePe identified significant variations in
-- transaction behavior across states, quarters, and payment
-- categories. Leadership seeks deeper understanding to drive
-- targeted business strategies.


-- Query 1.1: Top 10 states by total transaction amount (all time)
-- Business Use: Identify which states generate highest revenue
SELECT 
    state,
    SUM(transaction_count)            AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount_INR
FROM aggregated_transactions
GROUP BY state
ORDER BY total_amount_INR DESC
LIMIT 10;

-- Query 1.2: Payment category breakdown with percentage share
-- Business Use: Understand which payment types dominate
SELECT 
    transaction_name                  AS payment_category,
    SUM(transaction_count)            AS total_count,
    ROUND(SUM(transaction_amount), 2) AS total_amount,
    ROUND(SUM(transaction_count) * 100.0 /
          SUM(SUM(transaction_count)) OVER(),2) AS percentage_share
FROM aggregated_transactions
GROUP BY transaction_name
ORDER BY total_count DESC;

-- Query 1.3: Year-wise transaction growth with average value
-- Business Use: Track growth trend and transaction quality
SELECT 
    year,
    SUM(transaction_count)            AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount_INR,
    ROUND(SUM(transaction_amount) /
          NULLIF(SUM(transaction_count), 0), 2) AS avg_transaction_value
FROM aggregated_transactions
GROUP BY year
ORDER BY year;

-- Query 1.4: Quarter-wise performance comparison across years
-- Business Use: Identify seasonal trends and festive spikes
SELECT 
    year,
    quarter,
    SUM(transaction_count)            AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount_INR
FROM aggregated_transactions
GROUP BY year, quarter
ORDER BY year, quarter;

-- Query 1.5: States with declining transactions (bottom performers)
-- Business Use: Identify states needing intervention strategies
SELECT 
    state,
    SUM(transaction_count)            AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount_INR,
    ROUND(SUM(transaction_amount) /
          NULLIF(SUM(transaction_count), 0), 2) AS avg_transaction_value
FROM aggregated_transactions
GROUP BY state
ORDER BY total_transactions ASC
LIMIT 10;



-- CASE STUDY 2: Device Dominance & User Engagement
-- Scenario: PhonePe aims to enhance user engagement by
-- understanding user preferences across device brands.
-- Some devices are underutilized despite high registrations.


-- Query 2.1: Top 10 mobile brands by total registered users
-- Business Use: Know which devices to optimize app for
SELECT 
    user_brand,
    SUM(user_count)                AS total_users,
    ROUND(AVG(user_percentage), 2) AS avg_market_share_pct
FROM aggregated_users
GROUP BY user_brand
ORDER BY total_users DESC
LIMIT 10;

-- Query 2.2: Brand-wise user growth year over year
-- Business Use: Track which brands are gaining or losing users
SELECT 
    year,
    user_brand,
    SUM(user_count) AS total_users
FROM aggregated_users
GROUP BY year, user_brand
ORDER BY year, total_users DESC;

-- Query 2.3: States with highest app opens per registered user
-- Business Use: Find most engaged states for best practices
SELECT 
    state,
    SUM(user_registered)              AS total_registered,
    SUM(user_appopens)                AS total_app_opens,
    ROUND(SUM(user_appopens) * 1.0 /
          NULLIF(SUM(user_registered), 0), 2) AS opens_per_user
FROM map_users
GROUP BY state
ORDER BY opens_per_user DESC
LIMIT 10;

-- Query 2.4: States with HIGH registration but LOW engagement
-- Business Use: These are re-engagement campaign targets
SELECT 
    state,
    SUM(user_registered)  AS total_registered,
    SUM(user_appopens)    AS total_app_opens,
    ROUND(SUM(user_appopens) * 100.0 /
          NULLIF(SUM(user_registered), 0), 2) AS engagement_rate_pct
FROM map_users
GROUP BY state
HAVING engagement_rate_pct < 50
ORDER BY total_registered DESC;

-- Query 2.5: District-wise user registration hotspots
-- Business Use: Find hyper-local areas with highest user density
SELECT 
    state,
    user_district,
    SUM(user_registered) AS total_registered,
    SUM(user_appopens)   AS total_app_opens
FROM map_users
GROUP BY state, user_district
ORDER BY total_registered DESC
LIMIT 10;


-- CASE STUDY 3: Insurance Penetration & Growth Analysis
-- Scenario: PhonePe entered insurance domain and seeks to
-- analyze growth trajectory and identify untapped opportunities
-- for insurance adoption at state level.


-- Query 3.1: Year-wise insurance growth with average premium
-- Business Use: Track insurance business growth over time
SELECT 
    year,
    SUM(insurance_count)              AS total_policies,
    ROUND(SUM(insurance_amount), 2)   AS total_premium_INR,
    ROUND(SUM(insurance_amount) /
          NULLIF(SUM(insurance_count), 0), 2) AS avg_premium_per_policy
FROM aggregated_insurance
GROUP BY year
ORDER BY year;

-- Query 3.2: Top 10 states by insurance penetration
-- Business Use: Identify states driving insurance revenue
SELECT 
    state,
    SUM(insurance_count)              AS total_policies,
    ROUND(SUM(insurance_amount), 2)   AS total_premium_INR
FROM map_insurance
GROUP BY state
ORDER BY total_policies DESC
LIMIT 10;

-- Query 3.3: Bottom 10 states — untapped insurance markets
-- Business Use: Prioritize these for marketing investment
SELECT 
    state,
    SUM(insurance_count)              AS total_policies,
    ROUND(SUM(insurance_amount), 2)   AS total_premium_INR
FROM map_insurance
GROUP BY state
ORDER BY total_policies ASC
LIMIT 10;

-- Query 3.4: Quarter-wise insurance adoption trend
-- Business Use: Understand seasonal patterns in insurance buying
SELECT 
    year,
    quarter,
    SUM(insurance_count)              AS total_policies,
    ROUND(SUM(insurance_amount), 2)   AS total_premium_INR
FROM aggregated_insurance
GROUP BY year, quarter
ORDER BY year, quarter;

-- Query 3.5: Top districts by insurance count
-- Business Use: Find district-level insurance hotspots
SELECT 
    state,
    district_name,
    SUM(insurance_count)              AS total_policies,
    ROUND(SUM(insurance_amount), 2)   AS total_premium_INR
FROM map_insurance
GROUP BY state, district_name
ORDER BY total_policies DESC
LIMIT 10;



-- CASE STUDY 4: Transaction Analysis for Market Expansion
-- Scenario: PhonePe operates in a highly competitive market.
-- Understanding transaction dynamics at district level is
-- crucial for identifying expansion opportunities.


-- Query 4.1: Top 10 districts by transaction volume
-- Business Use: Identify high-performing districts for premium features
SELECT 
    state,
    district_name,
    SUM(transaction_count)            AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount_INR
FROM map_transactions
GROUP BY state, district_name
ORDER BY total_transactions DESC
LIMIT 10;

-- Query 4.2: Bottom 10 districts — expansion opportunities
-- Business Use: Target these with awareness and incentive campaigns
SELECT 
    state,
    district_name,
    SUM(transaction_count)            AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount_INR
FROM map_transactions
GROUP BY state, district_name
ORDER BY total_transactions ASC
LIMIT 10;

-- Query 4.3: Average transaction value by district
-- Business Use: High avg value = premium users worth targeting
SELECT 
    state,
    district_name,
    SUM(transaction_count)  AS total_count,
    ROUND(SUM(transaction_amount) /
          NULLIF(SUM(transaction_count), 0), 2) AS avg_txn_value_INR
FROM map_transactions
GROUP BY state, district_name
ORDER BY avg_txn_value_INR DESC
LIMIT 10;

-- Query 4.4: State-wise total transactions with district count
-- Business Use: Understand transaction spread within states
SELECT 
    state,
    COUNT(DISTINCT district_name)     AS total_districts,
    SUM(transaction_count)            AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount_INR,
    ROUND(SUM(transaction_count) /
          NULLIF(COUNT(DISTINCT district_name), 0), 0) AS avg_txn_per_district
FROM map_transactions
GROUP BY state
ORDER BY total_transactions DESC
LIMIT 10;

-- Query 4.5: Top 10 pincodes by transaction volume
-- Business Use: Pincode-level targeting for hyperlocal campaigns
SELECT 
    state,
    pincode,
    SUM(transaction_count)            AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_amount_INR
FROM top_transactions
GROUP BY state, pincode
ORDER BY total_transactions DESC
LIMIT 10;



-- CASE STUDY 5: User Engagement & Growth Strategy
-- Scenario: PhonePe seeks to enhance market position by
-- analyzing user engagement across states and districts.
-- High registrations but varying app usage patterns need
-- targeted growth strategies.


-- Query 5.1: Top 10 states by total registered users
-- Business Use: Identify states with largest user base
SELECT 
    state,
    SUM(registered_users) AS total_registered_users
FROM top_users
GROUP BY state
ORDER BY total_registered_users DESC
LIMIT 10;

-- Query 5.2: Top 10 pincodes by user registration
-- Business Use: Find hyperlocal user registration hotspots
SELECT 
    state,
    pincode,
    SUM(registered_users) AS total_users
FROM top_users
GROUP BY state, pincode
ORDER BY total_users DESC
LIMIT 10;

-- Query 5.3: States with highest engagement ratio
-- Business Use: Find best-performing states to replicate strategy
SELECT 
    state,
    SUM(user_registered)  AS total_users,
    SUM(user_appopens)    AS total_opens,
    ROUND(SUM(user_appopens) /
          NULLIF(SUM(user_registered), 0), 2) AS engagement_ratio
FROM map_users
GROUP BY state
ORDER BY engagement_ratio DESC
LIMIT 10;

-- Query 5.4: Year-wise user growth by state
-- Business Use: Track which states are growing fastest in users
SELECT 
    state,
    year,
    SUM(user_registered) AS total_registered,
    SUM(user_appopens)   AS total_opens
FROM map_users
GROUP BY state, year
ORDER BY year, total_registered DESC;

-- Query 5.5: Districts with highest registered users
-- Business Use: District-level targeting for user growth campaigns
SELECT 
    state,
    user_district,
    SUM(user_registered)  AS total_registered,
    SUM(user_appopens)    AS total_opens,
    ROUND(SUM(user_appopens) /
          NULLIF(SUM(user_registered), 0), 2) AS engagement_ratio
FROM map_users
GROUP BY state, user_district
ORDER BY total_registered DESC
LIMIT 10;


