\set ON_ERROR_STOP on

BEGIN; -- Start of operation

-- Remove any previous staging load so rerunning this file does not create duplicates.
TRUNCATE TABLE staging.restaurant_license_candidates RESTART IDENTITY; 
-- Copies the csv file result of 02_profile_business_licenses into the database
\copy staging.restaurant_license_candidates (customernumber, licensestatus, licensetype, licensestartdate, licenseenddate, businessactivity, premiseaddress, premiseindc, entityname, entitytradename, primaryactivityflag, categoryservicetype, daterefreshedon, ward, neighborhoodcluster, latitude, longitude, globalid, objectid) FROM 'data/processed/restaurant_license_candidates.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

COMMIT; -- End of the operation

-- Validate the load.
SELECT COUNT(*) AS loaded_rows
FROM staging.restaurant_license_candidates;

-- Preview several imported records.
SELECT
    staging_id,
    entitytradename,
    premiseaddress,
    ward
FROM staging.restaurant_license_candidates
ORDER BY staging_id
LIMIT 5;