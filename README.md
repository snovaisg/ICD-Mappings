# ICD-Mappings
This python tool enables a variety of mappings of ICD codes (International Classification of Diseases) to different medical concepts **with a single line of code**. 

# Supported Mappings

From `ICD-9 CM` diagnostic codes to:
- [ICD-10 CM](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): International Classification of Diseases version 10 Clinical Modification.
- [ICD-9 Chapters](https://icd.codes/icd9cm): 19 Chapters of ICD-9-CM.
- [CCS](https://hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp): Clinical Classification Software. All 14k ICD-9-CM diagnostic codes can be mapped into just 283 clinical categories.
- [CCI](https://hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp): Chronic Condition Indicator. True or False whether the diagnostic is chronic.

From `ICD-10 CM` diagnostic codes to:
- [ICD-9 CM](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): International Classification of Diseases version 9 Clinical Modification
- [ICD-10 CM Chapters](https://icd.who.int/browse10/2010/en): 22 Chapters of ICD-10 CM.
- [CCS(R)](https://hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp): Clinical Classification Software (Refined). All the 70k ICD-10-CM diagnostic codes can be mapped into just 530 clinical categories.
- [CCI(R)](https://hcup-us.ahrq.gov/toolssoftware/chronic_icd10/chronic_icd10.jsp): Chronic Condition Indicator (Refined). True or False Whether the diagnostic is chronic.

# Installation

`pip install icd-mappings`

# Usage
Below are some examples on how to use this tool.

## Mapper
This class allows you to map between ontologies.

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
>>>        - chapter
>>>        - ccs
>>>        - cci
>>> From icd10 to:
>>>        - icd9
>>>        - chapter
>>>        - ccsr
>>>        - ccir
```
## Validator
This class helps you validate codes for a given ontology. Currently supports ICD9 and ICD10 codes.

```python

from icdmappings import Validator

validator = Validator()

icd9code = '3591'

validator.validate(icd9code, expects='icd9_diagnostic')
>>> True

icd9codes = ['3591','NOT_A_CODE', '00321']
validator.validate(icd9codes, expects='icd9_diagnostic')
>>> [True, False, True]

# can also check procedure codes
icd9codes = ['3582', '5731', 'NOT_A_CODE']
validator.validate(icd9codes, expects='icd9_procedure')
>>> [True, True, False]

# likewise for ICD10

icd10code = 'B530'
validator.validate(icd10code, expects='icd10_diagnostic')
>>> True
```
# Feature requests

Feel free to request a new functionality or report a bug by creating a [new issue](https://github.com/snovaisg/ICD-Mappings/issues).


# Acknowledgments

[Tekaichi](https://github.com/Tekaichi) for building the initial version of the icd9->ccs pipeline
