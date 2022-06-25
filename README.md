# ICDMappings
 
The class **ICDMappings** maps:
- icd9 to icd10;
- icd10 to icd9;
- icd9 to CCS;
- icd9_3 (3rd level) to CCS;
- icd9 to icd9 chapters;
- icd9 to chronic vs not-chronic;
- icd9 checker (checks if a code is in fact icd9);

Supports mapping either a `single code` at a time, or a `pandas series` of codes.

# Current Supported Mappings

[ICD9->10->9](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings) maps between icd9 and icd10 codes (in both directions).

[CCS](https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp) maps icd9 codes into the 272 diagnostic groups of CCS.

[ICD9 Chapters](https://icd.codes/icd9cm) maps icd9 codes into the 19 icd9 chapters.

**ICD9 level 3** is the 3rd level of the hierarchy of any ICD9 code (first 3 digits).

[CCI](https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp) classifies each icd9 code into Chronic vs Not-chronic condition.

**ICD9 checker** helps to check if a code is an icd9 code or not. Uses only the latest version (2015) to check. Data is taken from [National Bureau of Economic Researh](https://www.nber.org/research/data/icd-9-cm-diagnosis-and-procedure-codes)


# Usage

```python
# imports
import pandas as pd
from ICDMappings import ICDMappings

# init
icdmap = ICDMappings()

# create some data of icd9 codes
data = pd.DataFrame(data=["29410","5362","34290","3669"],
                    columns=['ICD9_CODE']
                   )
data
>>>   ICD9_CODE
>>> 0     29410
>>> 1      5362
>>> 2     34290
>>> 3      3669

# check available groupers
icdmap.get_available_groupers()
>>> ['icd9toccs', 'icd9_3toccs', 'icd9to10', 'icd10to9', 'icd9tochapter', 'icd9_level3', 'icd9tocci', 'icd9checker']

# let's do the first one: icd9 to ccs
data['ccs'] = icdmap.lookup('icd9toccs',data['ICD9_CODE'])
data
>>>   ICD9_CODE  ccs
>>> 0     29410  653
>>> 1      5362  141
>>> 2     34290   82
>>> 3      3669   86

# now icd9 to icd10
data['ICD10'] = icdmap.lookup('icd9to10',data['ICD9_CODE'])
data
>>>   ICD9_CODE  ccs  ICD10
>>> 0     29410  653  F0280
>>> 1      5362  141  R1110
>>> 2     34290   82  G8190
>>> 3      3669   86  H269
```

# Acknowledgments

[Tekaichi](https://github.com/Tekaichi) for building the icd9->ccs pipeline
