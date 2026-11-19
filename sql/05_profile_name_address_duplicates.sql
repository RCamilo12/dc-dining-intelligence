-- Normalize restaurant names and addresses, then find repeated combinations without altering the tables
WITH normalized_candidates AS ( -- WITH creates a temporary result for the query
    SELECT
        staging_id,
        objectid,
        globalid,
        entitytradename,
        entityname,
        premiseaddress,

        -- Prefer the public trade name; use the legal entity name if missing.
        NULLIF(
            UPPER(
                REGEXP_REPLACE( -- Just used to replace repeated spaces for just one
                    BTRIM(
                        COALESCE( -- Uses the first available non missing value
                            NULLIF(BTRIM(entitytradename), ''), -- Public trade name column
                            NULLIF(BTRIM(entityname), '') -- Entity name if the public trade is missing
                        )
                    ),
                    '[[:space:]]+',
                    ' ',
                    'g'
                )
            ),
            ''
        ) AS normalized_name,

        -- Standardize capitalization and repeated spaces in the address.
        NULLIF(
            UPPER(
                REGEXP_REPLACE( -- Deleting repeated spaces in the address 
                    BTRIM(premiseaddress),
                    '[[:space:]]+',
                    ' ',
                    'g'
                )
            ),
            ''
        ) AS normalized_address

    FROM staging.restaurant_license_candidates
)

SELECT
    normalized_name,
    normalized_address,
    COUNT(*) AS license_record_count

FROM normalized_candidates

WHERE normalized_name IS NOT NULL
  AND normalized_address IS NOT NULL

GROUP BY
    normalized_name,
    normalized_address

HAVING COUNT(*) > 1 --Showing duplicates or just records that appear more than once

ORDER BY
    license_record_count DESC,
    normalized_name,
    normalized_address

LIMIT 50;