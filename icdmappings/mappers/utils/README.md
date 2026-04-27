# Utils

## `icd10_lookup_utils`

### Purpose
`icd10_lookup_utils.py` centralizes the shared ICD-10 range lookup logic used by both:
- `ICD10toBlocks`
- `ICD10toChapters`

It exists to avoid duplicated parsing/mapping code, keep behavior consistent across mappers, and make each mapper only responsible for choosing its input file.

### Core Types
- `ICD10Range(start, end, bucket)`: one numeric interval and its output label.
- `ICD10LookupTable`: `dict[str, list[ICD10Range]]`, keyed by ICD-10 first letter.
- A single letter key can contain multiple ranges.
- Example: `"D"` can include both `ICD10Range(0, 49, "C00-D49 | ...")` and `ICD10Range(50, 89, "D50-D89 | ...")`.

### Processing Sequence
The lookup flow is executed in this order:

1. **Load raw range map in mapper**
   - Mapper `_parse_file(...)` loads JSON and calls:
   - `build_lookup_from_range_descriptions(raw_lookup)`

2. **Parse each range key**
   - `build_lookup_from_range_descriptions(...)` splits each key (for example `V00-X58`) into start/end tokens.
   - Example split: `V00-X58` -> `start_code='V00'`, `end_code='X58'`.
   - It parses numeric bounds with `parse_range_bound(...)`, which supports both block and chapter endpoint formats.
   - Supported endpoint styles include values like `A00`, `O9A`, `QA0`, and dotted forms like `D3A.8` (bound parsing uses the first 3 characters, e.g. `D3A`).
   - Example numeric bounds: `V00` -> `0`, `X58` -> `58`.

3. **Expand across letter span**
   - `letter_span(start_letter, end_letter)` returns all letters in the inclusive interval.
   - `build_lookup_from_range_descriptions(...)` expands each range into per-letter `ICD10Range(start, end, bucket)` entries.
   - Example expansion for `V00-X58`:
   - `V` gets `0..99`, `W` gets `0..99`, `X` gets `0..58`.
   - All three point to bucket `V00-X58 | ...`.

4. **Lookup at map time**
   - Mapper calls `map_by_range_lookup(code, lookup)`.
   - `map_by_range_lookup(...)` runs:
   - `normalize_icd10_code(code)` to clean the input code
   - `extract_category_number(code)` to derive the numeric category
   - range match against prebuilt per-letter intervals

5. **Return final bucket**
   - On match, the method returns the bucket label in the format:
   - `<range> | <description>`
   - If no match is found, it returns `None`.

### Mapping Examples
Examples below show the final output format produced by `map_by_range_lookup(...)`.

#### From block source (`icd10cmblocks.json`)
- `A0105` -> `A00-A09 | Intestinal infectious diseases`
- `F320` -> `F30-F39 | Mood [affective] disorders`
- `H269` -> `H25-H28 | Disorders of lens`

#### From chapter source (`icd10cmchapters.json`)
- `A0105` -> `A00-B99 | Certain infectious and parasitic diseases`
- `M84651K` -> `M00-M99 | Diseases of the musculoskeletal system and connective tissue`
- `T25519D` -> `S00-T88 | Injury, poisoning and certain other consequences of external causes`
