# ICD-Mappings
This tool enables a variety of mappings between ICD codes (International Classification of Diseases) **with a single line of code**. 

It can map different ICD versions (such as between ICD9 and ICD10). Also maps to other codings such as CCS (Computer Software Classification), and classifies diagnostic codes into chronic or not with CCI (Chronic Condition Indicator).

# Installation

`pip install icd-mappings`

# Usage

```python
from icdmappings import Mapper

mapper = Mapper()

icd9code = '29410'
mapper.map(icd9code, source='icd9', target='ccs')
>>> '653'

# Can map any Iterable of codes (list, numpy array, pandas Series, you name it)
icd9codes = ['29410', '5362', 'NOT_A_CODE', '3669']
mapper.map(icd9codes, source='icd9', target='ccs')
>>> ['653', '141', None, '86']

# classify icd9 into chronic or not-chronic conditions
mapper.map(icd9codes, source='icd9', target='cci')
>>> [True, False, None, True]

# icd9 to icd10
mapper.map(icd9codes, source='icd9', target='icd10')
>>> ['F0280', 'R111000', None, 'H269']

# You can also check available mappers
mapper.show_mappers()
>>> Here are the available mappers
>>>
>>> From icd9 to:
>>>        - icd10
>>>        - ccs
>>>        - cci
>>>        - chapter
>>>        - level3
>>> From icd10 to:
>>>        - icd9
```

# Mappers

List of all mappers:
- [ICD9<->ICD10](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): ICD9-CM and ICD10-CM (in both directions).
- [ICD9->CCS](): ICD9-CM to CCS (Clinical Classification Software) codes;
- [ICD9->ICD9Chapters](https://icd.codes/icd9cm): ICD9-CM diagnostic codes to the 19 Chapters;
- [ICD9->CCI](https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp) ICD9-CM diagnostics to CCI (Chronic Condition Indicator). True of False depending on whether a diagnostic is chronic or not;
- ICD9->Level3: Gets the 3rd level of an ICD9-CM diagnostic code;
- ICD9Level3->CCS: Maps the 3rd level of an ICD9 code into the corresponding CCS code. Why? Sometimes codes in a database do not have the full length by default (poor quality of recording), so it can be useful to translate directly from the 3rd level to CCS. Some collisions happen (one icd9level3 could map to one of multiple ccs's) and at the moment we simply choose one of the compatible CCS codes.


Supports mapping either a `single code` at a time, or an `iterable of codes` (range, list, numpy array, pandas Series, etc...).


> :warning: When ICD9 or ICD10 is mentioned, it always refers to the American version aka ICD9-CM / ICD10-CM.

# Feature requests

Feel free to request a new feature [here](https://github.com/snovaisg/ICD-Mappings/issues).


# Acknowledgments

[Tekaichi](https://github.com/Tekaichi) for building the initial version of the icd9->ccs pipeline
