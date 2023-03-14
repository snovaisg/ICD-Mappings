# ICDMappings

The main class **Mapper** maps:
- icd9 to icd10;
- icd10 to icd9;
- icd9 to CCS;
- icd9 to icd9_3 (3rd level);
- icd9 to icd9 chapters;
- icd9 to chronic vs not-chronic;

Supports mapping either a `single code` at a time, or an iterable of codes (range, list, np.array, pd.Series, etc...).

Important Note: when icd9 or icd10 is mentioned it refers to icd9-cm and icd10-cm.

It also validates whether an icd9 code is a valid procedure or diagnostic.

# Current Supported Mappings

[ICD9<->10](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings) maps between icd9 and icd10 codes (in both directions).

[CCS](https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp) maps icd9 codes into the 272 diagnostic groups of CCS.

[ICD9 Chapters](https://icd.codes/icd9cm) maps icd9 codes into the 19 icd9 chapters.

**ICD9 level 3** is the 3rd level of the hierarchy of any ICD9 code (first 3 digits).

[CCI](https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp) classifies each icd9 code into Chronic vs Not-chronic condition.

**ICD9 checker** helps to check if a code is an icd9 code or not. Uses only the latest version (2015) to check. Data is taken from [National Bureau of Economic Researh](https://www.nber.org/research/data/icd-9-cm-diagnosis-and-procedure-codes)


# Usage

```python
# imports
import pandas as pd
from icdmappings import Mapper

# init
mapepr = Mapper()

# check available mappers
mapper.show_mappers()
>>> ['icd9toccs', 'icd9toicd10', 'icd10toicd9', 'icd9tochapter', 'icd9tolevel3', 'icd9tocci']

# check available validators
mapper.show_validators()
>>> ['icd9'] # going to add icd10 later

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

# let's do a random one: icd9 to ccs
data['ccs'] = mapper.map('icd9toccs',data['ICD9_CODE'])
data
>>>   ICD9_CODE  ccs
>>> 0     29410  653
>>> 1      5362  141
>>> 2     34290   82
>>> 3      3669   86

# now icd9 to icd10
data['ICD10'] = mapper.map('icd9to10',data['ICD9_CODE'])
data
>>>   ICD9_CODE  ccs  ICD10
>>> 0     29410  653  F0280
>>> 1      5362  141  R1110
>>> 2     34290   82  G8190
>>> 3      3669   86  H269
```

# Feature requests

Feel free to sugest feature requests under `Issues`, such as turning this into a script in case your pipeline does not use python.


# Acknowledgments

[Tekaichi](https://github.com/Tekaichi) for building the initial version of the icd9->ccs pipeline
