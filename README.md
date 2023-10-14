# ICD-Mappings
This python tool enables a variety of mappings between ICD diagnostic codes (International Classification of Diseases) **with a single line of code**. 

# Supported Mappings

From `ICD-9 CM` diagnostic codes to:
- [ICD-10 CM](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): International Classification of Diseases version 10 Clinical Modification.
- [CCS](https://hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp): Clinical Classification Software. Has a universe of just 283 diagnostic categories.
- [CCI](https://hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp): Chronic Condition Indicator. True or False whether the diagnostic is chronic.
- [ICD-9 Chapters](https://icd.codes/icd9cm): 19 Chapters of ICD-9 CM.

From `ICD-10 CM` diagnostic codes to:
- [ICD-9 CM](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): International Classification of Diseases version 9 Clinical Modification
- [ICD-10 CM Chapters](https://icd.who.int/browse10/2010/en): 22 Chapters of ICD-10 CM.

# Installation

`pip install icd-mappings`

# Usage

```python
from icdmappings import Mapper

mapper = Mapper()

# Make sure your codes don't include '.' separators 
icd9code = '29410' 
mapper.map(icd9code, source='icd9', target='ccs')
>>> '653'

# Can map any Iterable of codes (list, numpy array, pandas Series, you name it)
icd9codes = ['29410', '5362', 'NOT_A_CODE', '3669']
mapper.map(icd9codes, source='icd9', target='ccs')
>>> ['653', '141', None, '86']

# classify ICD-9 diagnostics into chronic or not-chronic
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
>>> From icd10 to:
>>>        - icd9
>>>        - chapter
```

# Feature requests

Feel free to request a new feature [here](https://github.com/snovaisg/ICD-Mappings/issues).


# Acknowledgments

[Tekaichi](https://github.com/Tekaichi) for building the initial version of the icd9->ccs pipeline
