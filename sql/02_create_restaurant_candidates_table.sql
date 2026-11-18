-- Create the empty table for restaurant-license candidates.
CREATE TABLE IF NOT EXISTS staging.restaurant_license_candidates (
    staging_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, --staging_id becomes a row number to identify each register
    
    -- All of them created as text since we need the full import and not skip some malformed ones
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