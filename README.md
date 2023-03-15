# ICDMappings

This tool helps working with ICD codes. It maps between ICD versions (such as between ICD9 and ICD10). Also maps to other codings such as CCS (Computer Software Classification), and CCI (Chronic Condition Indicator).

List of all mappers:
- [ICD9<->ICD10](https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings): ICD9-CM and ICD10-CM (in both directions).
- [ICD9->CCS](): ICD9-CM to CCS (Clinical Classification Software) codes;
- [ICD9->ICD9Chapters](https://icd.codes/icd9cm): ICD9-CM diagnostic codes to the 19 Chapters;
- [ICD9->CCI](https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp) ICD9-CM diagnostics to CCI (Chronic Condition Indicator). True of False depending on whether a diagnostic is chronic or not;
- ICD9->Level3: Gets the 3rd level of an ICD9-CM diagnostic code;


Supports mapping either a `single code` at a time, or an `iterable of codes` (range, list, np.array, pd.Series, etc...).

----

> :warning: **Warning:** When ICD9 or ICD10 is mentioned, it refers to the American version aka ICD9-CM / ICD10-CM.

# Usage

```python
from icdmappings import Mapper

mapper = Mapper()

icd9code = '29410'
mapper.map(icd9code, 'icd9toccs')
>>> '653'

# Can also map any Iterable of codes
icd9codes = ['29410', '5362', 'NOT_A_CODE', '3669']

# icd9 to ccs
mapper.map(icd9codes, mapper='icd9toccs')
>>> ['653', '141', None, '86']

# icd9 to icd10
mapper.map(icd9codes, mapper='icd9toicd10')
>>> ['F0280', 'R111000', None, 'H269']

# You can also check available mappers
mapper.show_mappers()
>>> ['icd9toccs', 'icd9toicd10', 'icd10toicd9', 'icd9tochapter', 'icd9tolevel3', 'icd9tocci']
```

# Feature requests

Feel free to sugest feature requests under `Issues`, such as turning this into a script in case your pipeline does not use python.


# Acknowledgments

[Tekaichi](https://github.com/Tekaichi) for building the initial version of the icd9->ccs pipeline
