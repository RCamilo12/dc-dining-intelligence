-- Enable spatial functionality in the current database.
CREATE EXTENSION IF NOT EXISTS postgis;

-- Imported datasets that remain close to their source structure.
CREATE SCHEMA IF NOT EXISTS staging;

-- Geographic reference data, including wards and neighborhood clusters.
CREATE SCHEMA IF NOT EXISTS reference;

-- Cleaned, deduplicated and analysis-ready tables.
CREATE SCHEMA IF NOT EXISTS analytics;