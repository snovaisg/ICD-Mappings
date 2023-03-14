# ICDMappings

This tool helps woking with ICD codes. It maps between ICD versions (such as between ICD9 and ICD10) but also maps to other codings such as ICD9 to CCS (reducing the universe of diagnostics to just 283 categories), CCI (which classifies a diagnostic code into either chronic or non-chronic).

The main class **Mapper** maps:
- [ICD9<->ICD10](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): ICD9-CM and ICD10-CM (in both directions).
- [ICD9->CCS](): ICD9-CM to CCS (Clinical Classification Software) codes;
- [ICD9->ICD9Chapters](https://icd.codes/icd9cm): ICD9-CM diagnostic codes to the 19 Chapters;
- [ICD9->CCI](https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp) ICD9-CM diagnostics to CCI (Chronic Condition Indicator). True of False depending on whether a diagnostic is chronic or not;
- ICD9->ICD9_3: Gets the 3rd level of an ICD9-CM diagnostic code;


Supports mapping either a `single code` at a time, or an `iterable of codes` (range, list, np.array, pd.Series, etc...).

----

> :warning: **Warning:** When ICD9 or ICD10 is mentioned, it refers to the American version aka ICD9-CM / ICD10-CM.

# Usage

```python
# imports
import pandas as pd
from icdmappings import Mapper

# init
mapper = Mapper()

# check available mappers
mapper.show_mappers()
>>> ['icd9toccs', 'icd9toicd10', 'icd10toicd9', 'icd9tochapter', 'icd9tolevel3', 'icd9tocci']

# check available validators
mapper.show_validators()
>>> ['icd9'] # going to add icd10 later

# let's map some codse

icd9_codes = ['29410', '5362', 'NOT_A_CODE', '3669']

# icd9 to ccs
mapper.map('icd9toccs',icd9_codes)
>>> ['653', '141', None, '86']

# icd9 to icd10
mapper.map('icd9toicd10',icd9_codes)
>>> ['F0280', 'R111000', None, 'H269']

# Also works with pandas

data = pd.DataFrame(data=['29410','5362','NOT_A_CODE','3669'],
                    columns=['ICD9_CODE']
                   )
data
>>>      ICD9_CODE
>>> 0        29410
>>> 1         5362
>>> 2   NOT_A_CODE
>>> 3         3669

# icd9 to ccs
data['ccs'] = mapper.map('icd9toccs',data['ICD9_CODE'])
data
>>>     ICD9_CODE    ccs
>>> 0       29410    653
>>> 1        5362    141
>>> 2  NOT_A_CODE   None
>>> 3        3669     86

# icd9 to icd10
data['ICD10'] = mapper.map('icd9to10',data['ICD9_CODE'])
data
>>>     ICD9_CODE    ccs  ICD10
>>> 0       29410    653  F0280
>>> 1        5362    141  R1110
>>> 2  NOT_A_CODE   None  None
>>> 3        3669     86  H269
```

# Feature requests

Feel free to sugest feature requests under `Issues`, such as turning this into a script in case your pipeline does not use python.


# Acknowledgments

[Tekaichi](https://github.com/Tekaichi) for building the initial version of the icd9->ccs pipeline
