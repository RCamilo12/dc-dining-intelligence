"""
Checks the raw data downloaded, inspecting the size of the files, the type of file  
(csv or zip), if csv it checks the column names and the datatypes.
"""

from pathlib import Path #bringing Path allows to operate the files
import zipfile #bringing zipfile helps to operate the zipfiles

import pandas as pd #Pandas is for tabulation 

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"

def inspect_csv(file_path: Path) -> None: #None means the function does not return a result
    """Inspect the CSV without loading the whole file into the memory"""

    sample = pd.read_csv(
        file_path, #Reading the csv into our code
        nrows=100, #We are only reading 100 rows
        low_memory=False, #Naking sure we internally dont overuse memory
        encoding="utf-8-sig" #Reading characters in a normal format
    )

    print(f"Number of columns: {len(sample.columns)}") #Brings the number of columns from the dataframe
    print(f"Sample rows inspected: {len(sample):,}")
    print("Preliminary columns and data types:")

    for column, data_type in sample.dtypes.items(): #Creates a pair for each column with its own time
        print(f" - {column}: {data_type}")

def inspect_zip(file_path:Path) -> None:
    """List the files contained in a ZIP file
    Basically checking what I have for the shapefiles"""
    print("ZIP contents:")

    with zipfile.ZipFile(file_path) as archive: #Opening the archive, with closes it when finished
        for member in archive.infolist(): #infolist will return information about each file inside
            size_kb = member.file_size/ 1024 #We convert bytes into kb
            print(f" - {member.filename} ({size_kb:,.1f} KB)") #And then we print both values, name and size
            #, will include thousands separators
            #.1 will bring one decimal number

            
def main() -> None:

    files = sorted(path 
                   for path in RAW_DATA_DIRECTORY.rglob("*") #globally locates any filename or directory
                   if path.is_file()) #Keeps just the files

    if not files: #Handling when files are not found
        print("No files found on data/raw.")
        return

    for file_path in files: #We loop on each file
        size_mb = file_path.stat().st_size / (1024 * 1024) #And we calculate each of their sizes 

        print("\n" + "=" * 80) #Just printing a like of "=" to make my life easier
        relative_path = file_path.relative_to(PROJECT_ROOT) #So we do not show our path in the computer
        print(f"File: {relative_path}")
        print(f"Size: {size_mb:,.2f} MB") #Prints the size of the current file

        try: #Inspecting for corrupted files
            if file_path.suffix.lower() == ".csv": #lower standarizes "csv", no uppercase issues
                inspect_csv(file_path) #Calls the created function and inspects the file

            elif file_path.suffix.lower() == ".zip": #same with "zip", no uppercase issues
                            inspect_zip(file_path) #Calls the created function and inspects

            else:
                 print(f"No inspection rule for {file_path.suffix}")

        except Exception as error:
             print(f"Could not inspect this file: {error}")

if __name__ == "__main__": #Runs main when the file is run directly
     main()