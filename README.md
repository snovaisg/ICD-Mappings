# ICD-Mappings

[![Downloads](https://pepy.tech/badge/icd-mappings)](https://pepy.tech/project/icd-mappings)
![PyPI](https://img.shields.io/pypi/v/icd-mappings)
![Supported python versions](https://img.shields.io/pypi/pyversions/icd-mappings)

This python tool enables a variety of mappings of ICD codes (International Classification of Diseases) to different medical concepts **with a single line of code**. 

Latest data refresh: ICD-10 chapter and block mappings were fetched from the latest available code ranges on `2026-04-27`.

# Supported Mappings

From `ICD-9 CM` diagnostic codes to:
- [ICD-10 CM](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): International Classification of Diseases version 10 Clinical Modification.
- [ICD-9 Chapters](https://icd.codes/icd9cm): 19 Chapters of ICD-9-CM.
- [CCS](https://hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp): Clinical Classification Software. All 14k ICD-9-CM diagnostic codes can be mapped into just 283 clinical categories.
- [CCI](https://hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp): Chronic Condition Indicator. True or False whether the diagnostic is chronic; parent-code inference is enabled by default for `target='cci'` and can be disabled with `allow_parent_inference=False`.
- [CCC Category](https://www.childrenshospitals.org/content/analytics/toolkit/complex-chronic-conditions): Pediatric Complex Chronic Conditions Classification System v3 - Category (15 categories).
- [CCC Subcategory](https://www.childrenshospitals.org/content/analytics/toolkit/complex-chronic-conditions): Pediatric Complex Chronic Conditions Classification System v3 - Subcategory (64 subcategories).

From `ICD-10 CM` diagnostic codes to:
- [ICD-9 CM](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): International Classification of Diseases version 9 Clinical Modification
- [ICD-10 CM Chapters](https://www.aapc.com/codes/icd-10-codes-range/): 22 Chapters of ICD-10 CM. Extraction date `2026-04-27`
- [ICD-10 CM Blocks](https://www.aapc.com/codes/icd-10-codes-range/): 226 Blocks of ICD-10 CM. Extraction date `2026-04-27`
- [CCS(R)](https://hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp): Clinical Classification Software (Refined). All the 70k ICD-10-CM diagnostic codes can be mapped into just 530 clinical categories.
- [CCI(R)](https://hcup-us.ahrq.gov/toolssoftware/chronic_icd10/chronic_icd10.jsp): Chronic Condition Indicator (Refined). True or False whether the diagnostic is chronic; parent-code inference is enabled by default for `target='ccir'` and can be disabled with `allow_parent_inference=False`.
- [CCC Category](https://www.childrenshospitals.org/content/analytics/toolkit/complex-chronic-conditions): Pediatric Complex Chronic Conditions Classification System v3 - Category (15 categories).
- [CCC Subcategory](https://www.childrenshospitals.org/content/analytics/toolkit/complex-chronic-conditions): Pediatric Complex Chronic Conditions Classification System v3 - Subcategory (64 subcategories).

# Installation

`pip install icd-mappings`

# Usage
Below are some examples on how to use this tool for both the `Mapper` and `Validator` classes

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

# For CCI, allow_parent_inference is True by default and maps truncated parent codes only when all mapped children agree.
mapper.map('567', source='icd9', target='cci')
>>> False

# You can explicitly disable parent-code inference.
mapper.map('567', source='icd9', target='cci', allow_parent_inference=False)
>>> None

# icd9 to icd10
mapper.map(icd9codes, source='icd9', target='icd10')
>>> ['F0280', 'R111000', None, 'H269']

# icd10 to chapters and blocks
icd10codes = ['F0280', 'R111000', 'NOT_A_CODE', 'H269', 'H27.8']
mapper.map(icd10codes, source='icd10', target='chapter')
>>> ['5', '18', None, '7', '7']

mapper.map(icd10codes, source='icd10', target='block')
>>> ['F00-F09', 'R10-R19', None, 'H25-H28', 'H25-H28']

# allow_parent_inference is True by default for CCIR and maps truncated parent codes only when all mapped children agree.
mapper.map('H81.0', source='icd10', target='ccir')
>>> True

# You can explicitly disable parent-code inference.
mapper.map('H81.0', source='icd10', target='ccir', allow_parent_inference=False)
>>> None


# Pediatric Complex Chronic Conditions (CCC)
icd9codes = ['135', '179', '243']
mapper.map(icd9codes, source='icd9', target='ccc_category')
>>> ['hemato_immu', 'malignancy', 'metabolic']

mapper.map(icd9codes, source='icd9', target='ccc_subcategory')
>>> ['Sarcoidosis', 'Neoplasms', 'Endocrine disorders']

# And many more... You can check all available mappers this way
mapper.show_mappers()
>>> From icd9 to:
>>>         - cci
>>>         - ccs
>>>         - chapter
>>>         - icd10
>>>         - ccc_category
>>>         - ccc_subcategory
>>> From icd10 to:
>>>         - icd9
>>>         - block
>>>         - chapter
>>>         - ccsr
>>>         - ccir
>>>         - ccc_category
>>>         - ccc_subcategory
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

Feel free to request a new functionality or report a bug by creating a [new issue](https://github.com/snovaisg/ICD-Mappings/issues/new).


# Acknowledgments

[Miguel Cardoso](https://github.com/msdbcardoso) for building the initial version of the icd9->ccs pipeline

# Supporting the Project

If this tool adds value to your use case, give it a star in its [github page](https://github.com/snovaisg/ICD-Mappings). Also, feedback is welcome in the [issues page](https://github.com/snovaisg/ICD-Mappings/issues).