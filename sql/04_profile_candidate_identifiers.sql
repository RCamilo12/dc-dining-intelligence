-- Profile OBJECTID completeness and uniqueness.
SELECT
    COUNT(*) AS total_rows, --Total count

    COUNT( --Present Identifiers
        NULLIF(BTRIM(objectid), '') --BTRIM removes spaces from beginning and end and Missing values into NULL
    ) AS objectid_present,  

    COUNT(*) - COUNT( -- Counting the missing values (Total count - Present Identifiers)
        NULLIF(BTRIM(objectid), '') --BTRIM removes spaces from beginning and end and Missing values into NULL
    ) AS objectid_missing,

    COUNT( -- Counting non missing OBJECTID values or Distinct Identifiers
        DISTINCT NULLIF(BTRIM(objectid), '') --BTRIM removes spaces from beginning and end and Missing values into NULL
    ) AS distinct_objectids,

    COUNT( -- Counting duplicates (Present Identifiers - Distinct Identifiers)
        NULLIF(BTRIM(objectid), '') --BTRIM removes spaces from beginning and end and Missing values into NULL
    ) - COUNT(
        DISTINCT NULLIF(BTRIM(objectid), '') 
    ) AS duplicate_objectid_occurrences

FROM staging.restaurant_license_candidates;

--Profile GLOBALID
SELECT
    COUNT(*) AS total_rows,

    COUNT(
        NULLIF(BTRIM(globalid), '')
    ) AS globalid_present,

    COUNT(*) - COUNT(
        NULLIF(BTRIM(globalid), '')
    ) AS globalid_missing,

    COUNT(
        DISTINCT NULLIF(BTRIM(globalid), '')
    ) AS distinct_globalids,
    
    COUNT(
        NULLIF(BTRIM(globalid), '')
    ) - COUNT(
        DISTINCT NULLIF(BTRIM(globalid), '')
    ) AS duplicate_globalid_ocurrences

FROM staging.restaurant_license_candidates;

--Profile CUSTOMERNUMBER
SELECT
    COUNT(*) AS total_rows,

    COUNT(
        NULLIF(BTRIM(customernumber), '')
    ) AS customernumber_present,

    COUNT(*) - COUNT(
        NULLIF(BTRIM(customernumber), '')
    ) AS customernumber_missing,

    COUNT(
        DISTINCT NULLIF(BTRIM(customernumber), '')
    ) AS distinct_customernumbers,
    
    COUNT(
        NULLIF(BTRIM(customernumber), '')
    ) - COUNT(
        DISTINCT NULLIF(BTRIM(customernumber), '')
    ) AS duplicate_customernumber_ocurrences

FROM staging.restaurant_license_candidates;

-- Examine customer numbers associated with multiple license records.
SELECT
    NULLIF(BTRIM(customernumber), '') AS customer_number,
    COUNT(*) AS license_record_count,

    COUNT(
        DISTINCT NULLIF(BTRIM(entitytradename), '')
    ) AS distinct_trade_names,

    COUNT(
        DISTINCT NULLIF(BTRIM(premiseaddress), '')
    ) AS distinct_addresses

FROM staging.restaurant_license_candidates

WHERE NULLIF(BTRIM(customernumber), '') IS NOT NULL -- Filtering the row

GROUP BY NULLIF(BTRIM(customernumber), '') -- Places all the customers with the same number into one group

HAVING COUNT(*) > 1 -- Keeps only the duplicates or the ones that have more than one ocurrence

ORDER BY
    license_record_count DESC,
    customer_number

LIMIT 25;