-- Create the staging table for restaurant-license candidates.
CREATE TABLE IF NOT EXISTS staging.restaurant_license_candidates (
    staging_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customernumber text,
    licensestatus text,
    licensetype text,
    licensestartdate text,
    licenseenddate text,
    businessactivity text,
    premiseaddress text,
    premiseindc text,
    entityname text,
    entitytradename text,
    primaryactivityflag text,
    categoryservicetype text,
    daterefreshedon text,
    ward text,
    neighborhoodcluster text,
    latitude text,
    longitude text,
    globalid text,
    objectid text,

    loaded_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.restaurant_license_candidates IS
    'Restaurant-license candidates extracted from the DC Basic Business License dataset.';