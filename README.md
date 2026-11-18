# DC Dining Intelligence

DC Dining Intelligence is an end-to-end data analytics and geospatial
project examining the distribution of restaurants across Washington, D.C.
The project combines public D.C. business-license data, geographic
boundaries, PostgreSQL, PostGIS, Python and interactive visualization.

Project Objective:
•	Build an interactive map that helps Washington D.C. users compare restaurants using guests feedback from multiple sources, explore where the highly rated restaurants are in the city and what are the best items on the menu in each of the restaurants.
•	Create this product demonstrating an end-to-end analytical workflow, including factors like source evaluation, API ingestion, entity matching, SQL Data Modeling, statistical scoring, geospatial analysis and interactive visualization.

## Project Questions

1. Which active D.C. restaurant licenses can be identified reliably?
2. Where are restaurants concentrated across wards and neighborhood clusters?
3. How complete and consistent are the geographic fields in the source data?
4. How can ratings from approved external platforms be compared responsibly?
5. How can review count and rating uncertainty be incorporated into a fair score?

## Data Sources
- Basic Business Licenses: All Basic Business Licenses issued by DLCP (Department of Licensing and Consumer Protection of District of Columbia), including historical license records that may currently be inactive. The dataset includes the most up to date contact and business activity information. Found on Open Data DC 
https://opendata.dc.gov/datasets/85bf98d3915f412c8a4de706f2d13513_0/explore
- Neighborhood Clusters: https://opendata.dc.gov/datasets/neighborhood-clusters/explore?location=38.893798%2C-77.014470%2C11
- Ward Clusters:  https://opendata.dc.gov/datasets/DCGIS::wards-from-2022

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

The first thing done for this project was to inspect the raw data so that the fields of each dataset could be later filtered, cleaned, organized and managed properly, for that reason, the file 01_inspect_sources.py was created. In this code we create two different functions that inspect each file corresponding to .csv and .zip, creating as a result the file source_inspection.txt that contains the size, number of columns, the number of rows inspected (which was set to 100), the name and the datatype that each column holds in a .csv file. For the .zip we inspected the extension of each file to be able to understand if they will be useful in PostGIS and GeoPandas when creating the final product.

As a result, we initially have the following characteristics in the files to work with:
- 40 Business License columns
- 46 neighborhood clusters
- 8 wards with demographic information
- Latitude and longitude for licenses
- Polygon geometry exists in the ZIP files
- Personal owner/agent, and other fields that can be excluded

### Business-license profiling

The Business License dataset is processed in 50,000-row chunks. Records are selected as initial restaurant candidates when license is active, the business is a restaurant and it has a premise in DC. which codingwise translates into:

- `LICENSESTATUS = ACTIVE`
- `BUSINESSACTIVITY = RESTAURANT`
- `PREMISEINDC = YES`

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

## Business Identification

Creating SQL queries we verify there is a GLOBALID and OBJECTID for every record in the list. 

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