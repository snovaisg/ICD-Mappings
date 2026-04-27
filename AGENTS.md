# AGENTS.md

This document explains how to use `icd-mappings`, what mappings are available, and which source data file powers each mapping direction.

## Environment

This is a poetry environment. run commands with `poetry run <command>`.

## Development Guidelines

Add type hinting to the methods changed/added. For docstrings, keep each method description concise, include one sentence on the method purpose, add one line for each input arg explaining what it is, and when applicable include a brief example showing where the method is useful.

When creating a commit use conventional commit messages.

## Quick Start

```python
from icdmappings import Mapper, Validator

mapper = Mapper()
validator = Validator()
```

## Example Usage

```python
from icdmappings import Mapper

mapper = Mapper()

# ICD-9 -> ICD-10
mapper.map("29410", source="icd9", target="icd10")
# 'F0280'

# ICD-10 -> ICD-9
mapper.map("F0280", source="icd10", target="icd9")
# '29410'

# ICD-9 -> CCS
mapper.map(["29410", "5362", "NOT_A_CODE"], source="icd9", target="ccs")
# ['653', '141', None]

# ICD-10 -> chapter / block
mapper.map(["F0280", "R111000", "H269"], source="icd10", target="chapter")
# ['5', '18', '7']

mapper.map(["F0280", "R111000", "H269"], source="icd10", target="block")
# ['F00-F09', 'R10-R19', 'H25-H28']
```

```python
from icdmappings import Validator

validator = Validator()

validator.validate("3591", expects="icd9_diagnostic")
# True

validator.validate(["3582", "5731", "NOT_A_CODE"], expects="icd9_procedure")
# [True, True, False]

validator.validate("B530", expects="icd10_diagnostic")
# True
```

## Available Mapping Targets

From `source="icd9"`:
- `target="cci"`
- `target="ccs"`
- `target="chapter"`
- `target="icd10"`
- `target="ccc_category"`
- `target="ccc_subcategory"`

From `source="icd10"`:
- `target="icd9"`
- `target="block"`
- `target="chapter"`
- `target="ccsr"`
- `target="ccir"`
- `target="ccc_category"`
- `target="ccc_subcategory"`

## Source File for Each Mapping

When you ask for a conversion, this is the package data file used by the mapper:

| Source | Target | Mapper class | Mapper implementation (.py) | Source data file |
|---|---|---|---|---|
| `icd9` | `icd10` | `ICD9toICD10` | `icdmappings/mappers/icd9_to_icd10.py` | `icdmappings/data_files/icd9toicd10cmgem.csv` |
| `icd10` | `icd9` | `ICD10toICD9` | `icdmappings/mappers/icd10_to_icd9.py` | `icdmappings/data_files/icd10cmtoicd9gem.csv` |
| `icd9` | `ccs` | `ICD9toCCS` | `icdmappings/mappers/icd9_to_ccs.py` | `icdmappings/data_files/CCS-SingleDiagnosisGrouper.txt` |
| `icd9` | `cci` | `ICD9toCCI` | `icdmappings/mappers/icd9_to_cci.py` | `icdmappings/data_files/cci2015.csv` |
| `icd10` | `ccir` | `ICD10toCCIR` | `icdmappings/mappers/icd10_to_ccir.py` | `icdmappings/data_files/CCIR_v2023-1.csv` |
| `icd10` | `ccsr` | `ICD10toCCSR` | `icdmappings/mappers/icd10_to_ccsr.py` | `icdmappings/data_files/ICD10_CM_CCSR/dx_cat1_mapping.json` |
| `icd9` | `chapter` | `ICD9toChapters` | `icdmappings/mappers/icd9_to_chapters.py` | `icdmappings/data_files/icd9-CM-code-chapter-en=PT.csv` |
| `icd10` | `chapter` | `ICD10toChapters` | `icdmappings/mappers/icd10_to_chapters.py` | `icdmappings/data_files/ICD10_CM_Chapters/chapter_lookup.json` |
| `icd10` | `block` | `ICD10toBlocks` | `icdmappings/mappers/icd10_to_blocks.py` | `icdmappings/data_files/ICD10_CM_Blocks/block_lookup.json` |
| `icd9` | `ccc_category` | `ICD9toCCCCategory` | `icdmappings/mappers/icd9_to_ccc_category.py` | `icdmappings/data_files/pediatric_ccc/ccc_mappings.csv` (filtered to ICD-9 rows) |
| `icd9` | `ccc_subcategory` | `ICD9toCCCSubcategory` | `icdmappings/mappers/icd9_to_ccc_subcategory.py` | `icdmappings/data_files/pediatric_ccc/ccc_mappings.csv` (filtered to ICD-9 rows) |
| `icd10` | `ccc_category` | `ICD10toCCCCategory` | `icdmappings/mappers/icd10_to_ccc_category.py` | `icdmappings/data_files/pediatric_ccc/ccc_mappings.csv` (filtered to ICD-10 rows) |
| `icd10` | `ccc_subcategory` | `ICD10toCCCSubcategory` | `icdmappings/mappers/icd10_to_ccc_subcategory.py` | `icdmappings/data_files/pediatric_ccc/ccc_mappings.csv` (filtered to ICD-10 rows) |

## Validator Inputs

Supported `expects=` values for `Validator.validate(...)`:
- `icd9_diagnostic`
- `icd9_procedure`
- `icd10_diagnostic`
- `icd10_procedure`
