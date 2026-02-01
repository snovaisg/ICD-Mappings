# Pediatric Complex Chronic Conditions (CCC) Data

## Source

This data is from the **Complex Chronic Conditions Classification System Version 3** provided by the Children's Hospital Association.

**Source URL:** https://www.childrenshospitals.org/content/analytics/toolkit/complex-chronic-conditions

## Original File

The original data file is:
- `FINAL V3 with Rev Code List 02282023.xlsx`

## Processing

The Excel file was converted to CSV format for use by the mappers. This conversion:
1. Reads all rows from the Excel file's active sheet
2. Writes them to a CSV file with standard comma-separated formatting
3. Preserves all 8 columns: `ICD_Code`, `ICD_Code_Description`, `DX_PR`, `CCC_Category`, `CCC_Subcategory`, `ICD9_ICD10`, `Tech_Dep`, `Transplant`

The `ICD9_ICD10` column indicates the ICD version:
- `9` = ICD-9 code
- `0` = ICD-10 code

## Reproducibility

To regenerate the CSV file from the original Excel file, run the following Python script:

```python
import openpyxl
import csv

# Load the Excel workbook
workbook = openpyxl.load_workbook('FINAL V3 with Rev Code List 02282023.xlsx')
sheet = workbook.active

# Write to CSV
with open('ccc_mappings.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in sheet.iter_rows(values_only=True):
        writer.writerow(row)

print('CSV file created successfully')
print('Rows written:', sheet.max_row)
```

**Requirements:** `openpyxl` (available as a dev dependency in this project)

```bash
poetry install
poetry run python <script_name>.py
```

## Data Statistics

- **Total rows:** 6,815 (excluding header)
- **ICD-9 codes:** 1,813
- **ICD-10 codes:** 5,002
- **CCC Categories:** 15 unique values
- **CCC Subcategories:** 64 unique values
