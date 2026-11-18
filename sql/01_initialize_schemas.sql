-- Creating PostGIS and the database schemas

-- Enable PostGIS spatial functionality in the current database.
CREATE EXTENSION IF NOT EXISTS postgis;

-- Creating folders inside the database
-- Imported datasets that remain close to their source structure.
CREATE SCHEMA IF NOT EXISTS staging;

-- Geographic reference data, including wards and neighborhood clusters.
CREATE SCHEMA IF NOT EXISTS reference;

-- Cleaned, deduplicated and analysis-ready tables.
CREATE SCHEMA IF NOT EXISTS analytics;