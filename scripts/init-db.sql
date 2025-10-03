-- Initialize database for FitMotiv
-- This script is run when the PostgreSQL container starts

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database if it doesn't exist (this is handled by POSTGRES_DB env var)
-- But we can add any additional setup here

-- You can add any additional initialization SQL here
-- For example, creating specific roles, permissions, etc.

-- Example: Create a read-only user for analytics
-- CREATE USER analytics_user WITH PASSWORD 'analytics_password';
-- GRANT CONNECT ON DATABASE fitmotiv_db TO analytics_user;
-- GRANT USAGE ON SCHEMA public TO analytics_user;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_user;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO analytics_user;