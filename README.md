# DC Dining Intelligence

DC Dining Intelligence is an end-to-end data analytics and geospatial
project examining the distribution of restaurants across Washington, D.C.

The project combines public D.C. business-license data, geographic
boundaries, PostgreSQL, PostGIS, Python and interactive visualization.
Its eventual goal is to create an interactive restaurant map that
compares guest-rating evidence and identifies geographic concentrations
of restaurants.

## Project Questions

1. Which active D.C. restaurant licenses can be identified reliably?
2. Where are restaurants concentrated across wards and neighborhood clusters?
3. How complete and consistent are the geographic fields in the source data?
4. How can ratings from approved external platforms be compared responsibly?
5. How can review count and rating uncertainty be incorporated into a fair score?

## Current Findings

The initial Business License profile found:

- 277,626 total business-license records
- 75,658 active license records
- 9,263 records with `BUSINESSACTIVITY = RESTAURANT`
- 2,236 active restaurant-license records with a D.C. premise
- 2,105 restaurant candidates with complete latitude and longitude
- 131 candidates missing coordinates
- 2,199 candidates where Restaurant is the primary activity
- 37 candidates where Restaurant is a secondary activity

These 2,236 records are restaurant-license candidates, not necessarily
2,236 unique restaurants. Deduplication and entity resolution have not
yet been completed.

## Data Sources

- D.C. Basic Business Licenses
- D.C. Neighborhood Clusters
- D.C. Wards from 2022

Raw data files are excluded from this repository. Instructions for
downloading and reproducing the data pipeline will be documented
separately.

## Technology

- Python
- pandas
- GeoPandas
- PostgreSQL
- PostGIS
- SQL
- Git and GitHub

## Project Structure

- `src/`: Python ingestion and profiling scripts
- `sql/`: Database creation, cleaning and analysis queries
- `docs/`: Project journal, profiling reports and methodology
- `data/raw/`: Original source files, excluded from Git
- `data/processed/`: Reproducible derived data, excluded from Git

## Methodology

### Source inspection

The source-inspection workflow identifies file formats, columns,
preliminary data types and shapefile components without modifying the
original files.

### Business-license profiling

The Business License dataset is processed in 50,000-row chunks. Records
are selected as initial restaurant candidates when:

- `LICENSESTATUS = ACTIVE`
- `BUSINESSACTIVITY = RESTAURANT`
- `PREMISEINDC = YES`

Chunked processing limits memory use while still profiling the complete
source dataset.

## Current Status

- [x] Create the local development environment
- [x] Install PostgreSQL and PostGIS
- [x] Inspect source files
- [x] Profile the Business License dataset
- [x] Extract initial restaurant-license candidates
- [ ] Analyze identifiers and duplicate records
- [ ] Load candidate records into PostgreSQL
- [ ] Import ward and neighborhood polygons
- [ ] Validate geography with spatial joins
- [ ] Build a deduplicated restaurant table
- [ ] Evaluate approved rating-data sources
- [ ] Build the interactive map

## Important Limitations

An active restaurant license does not necessarily prove that a
restaurant is currently open to the public. Multiple license records may
also represent the same restaurant.

External platform data will only be used when its licensing, storage,
analysis and display requirements permit the intended portfolio use.