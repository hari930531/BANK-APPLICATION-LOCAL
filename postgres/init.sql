-- =============================================================================
-- Database Initialization Script: Hari's Bank of Tamil Nadu
-- Target Engine: MySQL 8.0+
-- Description: Creates the database schema, sets up customer accounts,
--              user credentials with contact information, and inserts
--              initial seed data for local testing.
-- =============================================================================

-- Step 1: Create the database schema if it doesn't already exist
CREATE DATABASE IF NOT EXISTS bankdb;

-- Step 2: Set the current active database
USE bankdb;

-- -----------------------------------------------------------------------------
-- TABLE: accounts
-- Description: Stores customer bank account identifiers and ledger balances.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS accounts (
    -- Unique identifier for the bank account (e.g., ACC101)
    account_id VARCHAR(20) PRIMARY KEY,
    
    -- Legal name of the account holder
    holder_name VARCHAR(100) NOT NULL,
    
    -- Current account balance; restricted from falling below zero
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (balance >= 0)
);

-- -----------------------------------------------------------------------------
-- TABLE: users
-- Description: Stores authentication credentials and customer contact details.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    -- Internal primary key with auto-increment
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Unique username for logging into the portal
    username VARCHAR(50) UNIQUE NOT NULL,
    
    -- Account password
    password VARCHAR(100) NOT NULL,
    
    -- Associated bank account ID (Foreign link to accounts table)
    account_id VARCHAR(20) NOT NULL,
    
    -- Customer contact email address
    email VARCHAR(100) DEFAULT NULL,
    
    -- Customer primary phone/contact number
    phone VARCHAR(15) DEFAULT NULL,
    
    -- Full residential or postal address
    address TEXT DEFAULT NULL,
    
    -- Enforce referential integrity linking to accounts
    CONSTRAINT fk_user_account 
        FOREIGN KEY (account_id) 
        REFERENCES accounts(account_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- -----------------------------------------------------------------------------
-- SEED DATA INSERTION
-- Description: Inserts initial baseline test records if they do not exist.
-- -----------------------------------------------------------------------------

-- 1. Insert initial banking accounts
INSERT IGNORE INTO accounts (account_id, holder_name, balance) VALUES
('ACC101', 'Naveen Kumar', 25000.00),
('ACC102', 'Hariharan', 10000.00);

-- 2. Insert corresponding user login credentials and profile records
INSERT IGNORE INTO users (username, password, account_id, email, phone, address) VALUES
('naveen', 'pass123', 'ACC101', 'naveen@example.com', '9876543210', 'No. 12, Anna Nagar, Chennai, Tamil Nadu'),
('kumar', 'pass123', 'ACC102', 'kumar@example.com', '9123456780', 'No. 45, Cross Cut Road, Coimbatore, Tamil Nadu');

-- -----------------------------------------------------------------------------
-- VERIFICATION QUERIES
-- Description: Run to verify successful execution and inspect table records.
-- -----------------------------------------------------------------------------
SELECT * FROM accounts;
SELECT * FROM users;