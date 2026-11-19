# DC Dining Intelligence — Project Journal

This journal documents my technical decisions, learning process,
experiments, errors and conclusions while building DC Dining Intelligence.

## Milestone 1 — Development Environment

### Objective

Create a local environment capable of Python, SQL and geospatial analysis.

### Tools Installed

- Visual Studio Code
- Python
- PostgreSQL
- PostGIS
- Git

### Concepts Learned

- SQL is a language, while PostgreSQL is a database system.
- PostGIS extends PostgreSQL with spatial types and operations.
- VS Code connects to PostgreSQL but does not replace the database server.
- A Python virtual environment isolates project dependencies.

### Problems Encountered

- PostgreSQL initially rejected the saved password.
- `psql` was not initially available through the Windows PATH.
- Command-line commands and SQL queries must be executed in different interfaces.

## Milestone 2 — Source Inspection

### Objective

Inspect the downloaded files without loading or modifying the complete datasets.

### Concepts Learned

- `Path` provides operating-system-independent file handling.
- `nrows` allows limited CSV inspection.
- A shapefile consists of multiple companion files.
- Raw data should remain unchanged.
- Personal fields should be excluded when they are not analytically necessary.

### Files Inspected

- Basic Business Licenses
- Neighborhood Clusters
- Wards from 2022

### Problems Encountered

- The ZIP inspection initially used the wrong `ZipInfo` attribute.
- The sample-row message was accidentally indented inside a loop.
- PowerShell initially saved the report using UTF-16.

### Resolution

- Changed the ZIP attribute to `member.file_size`.
- Corrected Python indentation.
- Saved the report explicitly as UTF-8.

---

## Milestone 3 — Business License Profiling

### Objective

Profile the complete license source and extract active D.C. restaurant candidates.

### Design Decisions

- Read 50,000 rows at a time.
- Import selected columns as strings.
- Exclude owner, billing and registered-agent fields.
- Normalize filter values without modifying the original source values.

### Population Definition

A candidate record must satisfy:

- `LICENSESTATUS = ACTIVE`
- `BUSINESSACTIVITY = RESTAURANT`
- `PREMISEINDC = YES`

### Findings

- Total source records: 277,626
- Restaurant-activity records: 9,263
- Active D.C. restaurant candidates: 2,236
- Complete coordinates: 2,105
- Missing coordinates: 131

### Questions Raised

- Which source identifier is stable and unique?
- Do multiple licenses represent the same restaurant?
- Should secondary Restaurant activities remain in scope?
- Why are some wards represented as `WARD 2` while others are `2`?
- Are the 131 missing clusters the same records as the 131 missing coordinates?

## Milestone 4 - Duplicate Records

I do not expect repeated restaurant names or addresses. I think that since this came from a government 
source the whole database should be updated frequently. A repeated combination in names would mean that 
a restaurant has more than one location in the city, however if that is the case the address should be the
difference. A repeat in the address would mean that the restaurant has more than one business activity but 
that should have been filtered on our .py profiling process   

### Next Step

EXAMINE THE RESULTS OF THE DUPLICATES AND TAKE DECISIONS INTO WHAT TO DO WITH THEM