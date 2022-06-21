# ICD-Mappings
 
The class **ICDMappings** maps with a couple lines of code:
- icd9 to icd10;
- icd10 to icd9;
- icd9 to CCS;
- icd9 to icd9 chapters;
- icd9 to chronic vs not-chronic;

Supports mapping either a `single code` at a time, or a `pandas series` of codes!

# Current Supported Mappings

[ICD9->10->9](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings) maps between icd9 and icd10 codes (in both directions).

[CCS](https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp) aggregates all icd9 codes into just 272 diagnostic groups.

[ICD9 Chapters](https://icd.codes/icd9cm) aggregates all icd9 codes into just 19 chapters.

**ICD9 level 3** is the 3rd level of the hierarchy of any ICD9 code (first 3 digits). So it also reduces granuality by a lot.

[CCI](https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp) classifies each icd9 code into Chronic vs Not-chronic condition.


# Usage

**Playground.ipynb** contains a toy usage of the ICDMappings class, but we will also leave here an independent example:

```python
# imports
import pandas as pd
from ICDMappings import ICDMappings

# init
icdmap = ICDMappings()

# get some data
icd9_codes = ["29410","5362","34290","3669"]
data = pd.DataFrame(icd9_codes,columns=['ICD9_CODE'])
data
>>>   ICD9_CODE
>>> 0     29410
>>> 1      5362
>>> 2     34290
>>> 3      3669

# check available groupers
icdmap.get_available_groupers()
>>> ['icd9toccs', 'icd9to10', 'icd10to9', 'icd9tochapter', 'icd9_level3', 'icd9tocci']

# let's do the first one: icd9 to ccs
data['ccs'] = icdmap.icd9toccs.lookup(data['ICD9_CODE'])
data
>>>   ICD9_CODE  ccs
>>> 0     29410  653
>>> 1      5362  141
>>> 2     34290   82
>>> 3      3669   86

# now icd9 to icd10
data['ICD10'] = icdmap.icd9to10.lookup(data['ICD9_CODE'])
data
>>>   ICD9_CODE  ccs  ICD10
>>> 0     29410  653  F0280
>>> 1      5362  141  R1110
>>> 2     34290   82  G8190
>>> 3      3669   86  H269
```
