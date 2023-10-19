# ICD-Mappings
This python tool enables a variety of mappings of ICD codes (International Classification of Diseases) to different medical concepts **with a single line of code**. 

# Supported Mappings

From `ICD-9 CM` diagnostic codes to:
- [ICD-10 CM](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): International Classification of Diseases version 10 Clinical Modification.
- [CCS](https://hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp): Clinical Classification Software. Has a universe of just 283 diagnostic categories.
- [CCI](https://hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp): Chronic Condition Indicator. True or False whether the diagnostic is chronic.
- [ICD-9 Chapters](https://icd.codes/icd9cm): 19 Chapters of ICD-9 CM.

From `ICD-10 CM` diagnostic codes to:
- [ICD-9 CM](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): International Classification of Diseases version 9 Clinical Modification
- [ICD-10 CM Chapters](https://icd.who.int/browse10/2010/en): 22 Chapters of ICD-10 CM.
- [CCS(R)](https://hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp): Clinical Classification Software (Refined). All the 70k ICD-10-CM diagnostic codes can be mapped into just 530 clinical categories.

# Installation

`pip install icd-mappings`

# Usage

```python
from icdmappings import Mapper

mapper = Mapper()

icd9code = '29410' 
mapper.map(icd9code, source='icd9', target='ccs')
>>> '653'

# you can pass any Iterable of codes (list, numpy array, pandas Series, you name it)
icd9codes = ['29410', '5362', 'NOT_A_CODE', '3669']
mapper.map(icd9codes, source='icd9', target='ccs')
>>> ['653', '141', None, '86']

# which of these diagnostics are chronic?
mapper.map(icd9codes, source='icd9', target='cci')
>>> [True, False, None, True]

# icd9 to icd10
mapper.map(icd9codes, source='icd9', target='icd10')
>>> ['F0280', 'R111000', None, 'H269']

# And many more... You can check all available mappers this way
mapper.show_mappers()
>>> From icd9 to:
>>>        - icd10
>>>        - ccs
>>>        - cci
>>>        - chapter
>>> From icd10 to:
>>>        - icd9
>>>        - chapter
>>>        - ccsr
```

# Feature requests

Feel free to request a new functionality or report a bug by creating a [new issue](https://github.com/snovaisg/ICD-Mappings/issues).


# Acknowledgments

[Tekaichi](https://github.com/Tekaichi) for building the initial version of the icd9->ccs pipeline
