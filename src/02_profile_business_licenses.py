from collections import Counter #For counting ocurrences
from pathlib import Path #For filesystem locations

import pandas as pd #For tabular data


# file uses the route of the current file, .resolve converts that location
# into an absolute path, and, parents[1] brings us one directory back
PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILE = ( #Brings the source file using the PROJECT_ROOT as the base
    PROJECT_ROOT
    / "data"
    / "raw"
    / "business_licenses"
    / "Basic_Business_License.csv"
)

CANDIDATE_OUTPUT_FILE = ( # Assigns the directory and file of the output database
    PROJECT_ROOT
    / "data"
    / "processed"
    / "restaurant_license_candidates.csv"
)

REPORT_FILE = ( # Assigns the directory and file of the output reports
    PROJECT_ROOT
    / "docs"
    / "business_license_profile.txt"
)

# Process 50,000 records at a time instead of loading the full CSV
CHUNK_SIZE = 50_000

# Read only fields relevant to the project
# Owner, billing and registered-agent information is deliberately excluded.
COLUMNS_TO_READ = [
    "CUSTOMERNUMBER",
    "LICENSESTATUS",
    "LICENSETYPE",
    "LICENSESTARTDATE",
    "LICENSEENDDATE",
    "BUSINESSACTIVITY",
    "PREMISEADDRESS",
    "PREMISEINDC",
    "ENTITYNAME",
    "ENTITYTRADENAME",
    "PRIMARYACTIVITYFLAG",
    "CATEGORYSERVICETYPE",
    "DATAREFRESHEDON",
    "WARD",
    "NEIGHBORHOODCLUSTER",
    "LATITUDE",
    "LONGITUDE",
    "GLOBALID",
    "OBJECTID",
]


def normalize_values(series: pd.Series) -> pd.Series:
    """
    Normalize text so that comparisons are consistent.
    (series: pd.Series) means that the function expects pandas Series. One Dataframe column
    pd.Series means that the function will return another series
    """

    return (
        series.astype("string") #converts column to string
        .fillna("")  #represents missing values "" as "NA" 
        .str.strip() #removes the whitespace
        .str.upper() #text goes uppercase
        .str.replace(r"\s+", " ", regex=True) #replaces double spaces with just one
    )


def update_counts(counter: Counter, series: pd.Series) -> None:
    """
    Add the frequencies from one CSV chunk to a running counter.
    Receives a Counter that already exists and a DataFrame column from the current chunk
    It returns nothing, since it modifies directly
    """

    values = normalize_values(series) #uses the function prior created to normalize values
    values = values.replace("", "<MISSING>") #replaces all empty values with <MISSING>

    #creates a dictionary with the value of the column and the total count
    counter.update(values.value_counts().to_dict())


def add_counter_section(
    report: list[str], #A list of strings, a line for each line of text
    title: str,
    counter: Counter,
    limit: int | None = None,
) -> None:
    """Add a formatted frequency-count section to the report."""

    report.append("") #Blank line at the end of the report
    report.append(title) #Adds the title

    #returning values from most frequent to the least frequent
    for value, count in counter.most_common(limit): #most_common manages the frequency
        report.append(f"  {value}: {count:,}")  #:, manages comas on big numbers


def main() -> None: #MAIN PROGRAM
    """Profile the license file and extract active restaurant candidates."""

    if not SOURCE_FILE.exists(): #Handles the case where we do not find the file needed
        raise FileNotFoundError(
            f"Business License file was not found:\n{SOURCE_FILE}"
        )

    total_rows = 0 #initial state
    restaurant_chunks = [] #restaurants candidates per chunk

    #Counts to accumulate frequency across the file
    license_status_counts = Counter()
    business_activity_counts = Counter()
    premise_in_dc_counts = Counter()

    #Reading the csv file from the source and returning the chunk size amount of registers
    #Specifying dtype="string" preserves identifiers exactly as provided.
    csv_reader = pd.read_csv(
        SOURCE_FILE,
        usecols=COLUMNS_TO_READ, #Only loads the selected columns
        dtype="string", #loads them as text
        chunksize=CHUNK_SIZE, #50K rows each dataframe
        encoding="utf-8-sig",
    )

    for chunk_number, chunk in enumerate(csv_reader, start=1):
        total_rows += len(chunk) #returns number of rows in current chunk

        # Accumulate full-dataset frequency counts.
        update_counts(
            license_status_counts,
            chunk["LICENSESTATUS"],
        )

        update_counts(
            business_activity_counts,
            chunk["BUSINESSACTIVITY"],
        )

        update_counts(
            premise_in_dc_counts,
            chunk["PREMISEINDC"],
        )

        # Normalize only for comparison. Original values remain unchanged.
        normalized_status = normalize_values(
            chunk["LICENSESTATUS"]
        )

        normalized_activity = normalize_values(
            chunk["BUSINESSACTIVITY"]
        )

        normalized_premise = normalize_values(
            chunk["PREMISEINDC"]
        )

        # A record must satisfy all three of the following conditions
        restaurant_mask = (
            normalized_status.eq("ACTIVE")
            & normalized_activity.eq("RESTAURANT")
            & normalized_premise.eq("YES")
        )

        #Creating a new dataframe with the filtered rows totally independent
        restaurant_chunks.append(
            chunk.loc[restaurant_mask].copy() 
        )

        restaurants_found = int(restaurant_mask.sum()) #we sum the amount of restaurants

        print( #Quick report about the progress done in the program
            f"Processed chunk {chunk_number}: "
            f"{len(chunk):,} rows; "
            f"{restaurants_found:,} candidates found; "
            f"{total_rows:,} total rows processed"
        )

    restaurant_candidates = pd.concat( #combining the chunks
        restaurant_chunks,
        ignore_index=True,
    )

    # Save the filtered records
    CANDIDATE_OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    restaurant_candidates.to_csv( #converting the candidates into a csv
        CANDIDATE_OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    #Convert coordinates only for validation.
    #Invalid text becomes a missing value instead of crashing the script.
    latitude = pd.to_numeric(
        restaurant_candidates["LATITUDE"],
        errors="coerce", #makes valid values into numbers
    )

    longitude = pd.to_numeric(
        restaurant_candidates["LONGITUDE"],
        errors="coerce",
    )

    complete_coordinates = int(
        (latitude.notna() & longitude.notna()).sum() #making sure we have both coordinates
    )

    #Candidate countes for restaurants
    candidate_primary_counts = Counter()
    candidate_ward_counts = Counter()
    candidate_cluster_counts = Counter()

    update_counts( #updating the counts
        candidate_primary_counts,
        restaurant_candidates["PRIMARYACTIVITYFLAG"],
    )

    update_counts(
        candidate_ward_counts,
        restaurant_candidates["WARD"],
    )

    update_counts(
        candidate_cluster_counts,
        restaurant_candidates["NEIGHBORHOODCLUSTER"],
    )

    important_fields = [ #important for map displaying
        "ENTITYTRADENAME",
        "ENTITYNAME",
        "PREMISEADDRESS",
        "LATITUDE",
        "LONGITUDE",
        "GLOBALID",
        "OBJECTID",
    ]

    missing_counts = { #checks how many values are we missing from the important fields
        column: int(
            normalize_values(restaurant_candidates[column])
            .eq("")
            .sum()
        )
        for column in important_fields
    }

    #BUILDING THE REPORT
    report = [
        "DC Dining Intelligence — Business License Profile",
        "=================================================",
        f"Source: {SOURCE_FILE.name}", #Source file
        f"Chunk size: {CHUNK_SIZE:,}", #Chunk size
        f"Total source rows: {total_rows:,}", #Source rows on chunk
        (
            "Active Restaurant records with a D.C. premise: "
            f"{len(restaurant_candidates):,}"
        ),
        (
            "Candidates with complete latitude and longitude: "
            f"{complete_coordinates:,}"
        ),
        "",
        "Missing values among restaurant candidates",
    ]

    for column, count in missing_counts.items():
        report.append(f"  {column}: {count:,}") #reports the missing values

    add_counter_section(
        report,
        "License status — all source records",
        license_status_counts,
    )

    add_counter_section(
        report,
        "Premise-in-DC values — all source records",
        premise_in_dc_counts,
    )

    add_counter_section(
        report,
        "Primary-activity flags — restaurant candidates",
        candidate_primary_counts,
    )

    add_counter_section(
        report,
        "Top 25 business activities — all source records",
        business_activity_counts,
        limit=25,
    )

    add_counter_section(
        report,
        "Restaurant candidates by ward",
        candidate_ward_counts,
    )

    add_counter_section(
        report,
        "Restaurant candidates by neighborhood cluster",
        candidate_cluster_counts,
    )

    report_text = "\n".join(report) #coverts the list into a text

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_FILE.write_text(
        report_text,
        encoding="utf-8",
    )

    print()
    print(report_text)
    print()
    print(
        "Candidate data saved to: "
        f"{CANDIDATE_OUTPUT_FILE.relative_to(PROJECT_ROOT)}"
    )
    print(
        "Profile report saved to: "
        f"{REPORT_FILE.relative_to(PROJECT_ROOT)}"
    )


if __name__ == "__main__":
    main()