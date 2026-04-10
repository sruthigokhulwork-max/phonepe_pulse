
-- CREATE DATABASE phonepe;
-- USE phonepe;

-- AGGREGATED TRANSACTIONS

-- CREATE TABLE aggregated_transactions(
-- 	   id INT auto_increment PRIMARY KEY,
--     state varchar(50),
--     year int,
--     quarter int,
--     transaction_name varchar(100),
--     transaction_count bigint,
--     transaction_amount double);
-- select * from aggregated_transactions; 
-- DESCRIBE aggregated_transactions;


-- AGGREGATED USERS

--  create table aggregated_users(
-- 	       id int auto_increment primary key,
--         state varchar(50),
--         year int,
--         quarter int,
--         user_brand varchar(100),
--         user_count bigint,
--         user_percentage double);
--  select * from aggregated_users; 
-- 	DESCRIBE aggregated_users;


-- AGGREGATED INSURANCE

--  create table aggregated_insurance(
-- 		   id int auto_increment primary key,
--         state varchar(50),
--         year int,
--         quarter int,
--         insurance_name varchar(100),
--         insurance_count bigint,
--         insurance_amount double);
--  select * from aggregated_insurance;
--  describe aggregated_insurance;

-- MAP TRANSACTIONS

--  create table map_transactions(
-- 		   id int auto_increment primary key,
--         state varchar(50),
--         year int,
--         quarter int,
--         district_name varchar(100),
--         transaction_count bigint,
--         transaction_amount double);
--  select * from map_transactions;
--  describe map_transactions;

-- MAP USERS

-- create table map_users(
-- 	       id int auto_increment primary key,
--         state varchar(50),
--         year int,
--         quarter int,
--         user_district varchar(100),
--         user_registered bigint,
--         user_appopens double);
--  select * from map_users; 
-- 	DESCRIBE map_users;

-- MAP INSURANCE

--  create table map_insurance(
-- 		   id int auto_increment primary key,
-- 		   state varchar(50),
--         year int,
-- 		   quarter int,
--         district_name varchar(100),
--         insurance_count bigint,
--         insurance_amount double);
--  select * from aggregated_insurance;
--  describe aggregated_insurance;

-- TOP TRANSACTIONS

--  create table top_transactions(
-- 	       id int auto_increment primary key,
-- 	       state varchar(50),
-- 	       year int,
-- 	       quarter int,
-- 	       pincode varchar(50),
-- 	       transaction_count bigint,
-- 	       transaction_amount double);
--  select * from top_transactions;
--  describe top_transactions;

-- TOP USERS

  -- create table top_users(
  --        id int auto_increment primary key,
  --        state varchar(50),
  -- 	    year int,
  -- 	    quarter int,
  -- 		pincode varchar(50),
  -- 	    registered_users bigint);
  --  select * from aggregated_users; 
  --  DESCRIBE aggregated_users;

-- TOP INSURANCE

--   create table top_insurance(
-- 	  	    id int auto_increment primary key,
--          state varchar(50),
-- 	   	    year int,
-- 	        quarter int,
-- 	        pincode varchar(50),
-- 	        insurance_count bigint,
-- 	        insurance_amount double);
--   select * from top_insurance;
--   describe top_insurance;


 -- SHOW TABLES;
-- SELECT 'aggregated_transactions' AS tbl, COUNT(*) FROM aggregated_transactions
-- UNION ALL SELECT 'aggregated_users',    COUNT(*) FROM aggregated_users
-- UNION ALL SELECT 'aggregated_insurance', COUNT(*) FROM aggregated_insurance
-- UNION ALL SELECT 'map_transactions',    COUNT(*) FROM map_transactions
-- UNION ALL SELECT 'map_users',           COUNT(*) FROM map_users
-- UNION ALL SELECT 'map_insurance',      COUNT(*) FROM map_insurance
-- UNION ALL SELECT 'top_transactions',    COUNT(*) FROM top_transactions
-- UNION ALL SELECT 'top_users',           COUNT(*) FROM top_users
-- UNION ALL SELECT 'top_insurance',      COUNT(*) FROM top_insurance;

-- DESCRIBE aggregated_transactions;
-- DESCRIBE aggregated_users;
-- DESCRIBE aggregated_insurance;





















		   





















