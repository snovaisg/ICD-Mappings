# ICD-Codes-Grouper
 
This repo allows you to convert from ICD9 to any of the following encodings: **ccs**, **icd9_level_3**, **icd9_chapters**,**cci** 

# Sources

[CCS](https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp) aggregates all icd9 codes into just 272 diagnostic groups.

[ICD9 Chapters](https://icd.codes/icd9cm) aggregates all icd9 codes into just 19 chapters.

**ICD9 level 3** is the 3rd level of the hierarchy of any ICD9 code (first 3 digits).

[CCI](https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp) classifies each icd9 code into Chronic vs Non-chronic condition.


# Usage

```python
# imports
import pandas as pd
from ICDCodesGrouper import ICDCodesGrouper

# init
codes_grouper = ICDCodesGrouper(ccs_path='grouper_data/CCS-SingleDiagnosisGrouper.txt',
                                icd9_chapter_path='grouper_data/icd9-CM-code-chapter-en=PT.csv',
                                cci_path='grouper_data/cci2015.csv'
                               )

# usage (let's do icd9 to ccs)
icd9_codes = ["29410","5362","34290","3669"]
data = pd.DataFrame(icd9_codes,columns=['ICD9_CODE'])

data
>>>   ICD9_CODE
>>> 0     29410
>>> 1      5362
>>> 2     34290
>>> 3      3669

data['ccs'] = codes_grouper.ccs.lookup(data['ICD9_CODE'])

data
>>>   ICD9_CODE  ccs
>>> 0     29410  653
>>> 1      5362  141
>>> 2     34290   82
>>> 3      3669   86

# Now for all available groups
groups = codes_grouper.get_available_groupers()

for g in groups:
    data[g] = codes_grouper.lookup(g,data['ICD9_CODE'])

data
>>>   ICD9_CODE  ccs  icd9chapters icd9_level3    cci
>>> 0     29410  653             5         294   True
>>> 1      5362  141             9         536  False
>>> 2     34290   82             6         342   True
>>> 3      3669   86             6         366   True
```
