from __future__ import annotations

from collections.abc import Mapping
from string import ascii_uppercase
from typing import Dict, List, NamedTuple


class ICD10Range(NamedTuple):
    """Represent one numeric ICD-10 interval and its output label."""

    start: int
    end: int
    bucket: str


ICD10FirstLetter = str
ICD10LookupTable = Dict[ICD10FirstLetter, List[ICD10Range]]
# Example: {"D": [ICD10Range(0, 49, "C00-D49 | Neoplasms"), 
#                 ICD10Range(50, 89, "D50-D89 | Diseases of the blood...")
#                 ], ...}


def normalize_icd10_code(code: object) -> str | None:
    """Normalize an ICD-10 code candidate for lookup.

    Args:
        code: Raw ICD-10 code candidate.
    """
    if not isinstance(code, str):
        return None

    normalized = code.strip().upper().replace(".", "")
    if not normalized:
        return None

    return normalized


def extract_category_number(code: str) -> int | None:
    """Extract the 2-digit category number used in range lookups.

    Args:
        code: Dotless uppercase ICD-10 code.
    """
    if len(code) < 3 or not code[0].isalpha() or not code[1].isdigit():
        return None

    third = code[2]
    if third.isdigit():
        return int(code[1:3])
    if third.isalpha():
        return int(code[1]) * 10

    return None


def map_by_range_lookup(code: object, lookup: ICD10LookupTable) -> str | None:
    """Map one ICD-10 code candidate to its bucket using parsed ranges.

    Args:
        code: Raw ICD-10 code candidate.
        lookup: Letter-indexed ICD-10 lookup table.
    """
    normalized = normalize_icd10_code(code)
    if normalized is None:
        return None

    category = extract_category_number(normalized)
    if category is None:
        return None

    first_letter: ICD10FirstLetter = normalized[0]

    for entry in lookup.get(first_letter, ()):
        if entry.start <= category <= entry.end:
            return entry.bucket

    return None


def letter_span(start_letter: str, end_letter: str) -> list[str]:
    """Return the inclusive uppercase letter span between two letters.

    Args:
        start_letter: First letter in the range.
        end_letter: Last letter in the range.

    Example:
        letter_span("V", "X") -> ["V", "W", "X"] (used by ranges like V01-X59).
    """
    start_idx = ascii_uppercase.index(start_letter)
    end_idx = ascii_uppercase.index(end_letter)
    return list(ascii_uppercase[start_idx : end_idx + 1])


def parse_range_bound(token: str, *, is_end: bool) -> int:
    """Parse range endpoints used by ICD-10 block/chapter lookup files.

    Args:
        token: Range endpoint token such as A00, O9A, QA0, or D3A.8.
        is_end: Whether the token belongs to the range end.
    """
    if len(token) < 3:
        raise ValueError(f"Invalid ICD-10 range token: {token}")

    second = token[1]
    third = token[2]

    if second.isdigit() and third.isdigit():
        return int(second + third)
    if second.isdigit() and third.isalpha():
        return int(second) * 10
    if second.isalpha() and third.isdigit():
        return 99 if is_end else 0

    raise ValueError(f"Invalid ICD-10 range token: {token}")


def build_lookup_from_range_descriptions(
    raw_lookup: Mapping[str, str],
) -> ICD10LookupTable:
    """Build a letter-indexed lookup table from range-to-description mappings.

    Args:
        raw_lookup: Raw JSON mapping from range keys to descriptions.
    """
    parsed: ICD10LookupTable = {}

    for range_key, description in raw_lookup.items():
        start_code, end_code = range_key.split("-", 1)
        start_letter, end_letter = start_code[0], end_code[0]
        start_num = parse_range_bound(start_code, is_end=False)
        end_num = parse_range_bound(end_code, is_end=True)
        bucket = f"{range_key} | {description}"

        for letter in letter_span(start_letter, end_letter):
            if letter == start_letter == end_letter:
                lo, hi = start_num, end_num
            elif letter == start_letter:
                lo, hi = start_num, 99
            elif letter == end_letter:
                lo, hi = 0, end_num
            else:
                lo, hi = 0, 99

            parsed.setdefault(letter, []).append(ICD10Range(start=lo, end=hi, bucket=bucket))

    return parsed
