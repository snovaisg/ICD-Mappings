from __future__ import annotations

from typing import Optional, Union
from collections.abc import Iterable
import csv
import importlib_resources
from icdmappings import data_files

class ICD10toCCIR:
    """
    Classifies ICD-10-CM diagnostic codes into chronic (True) or not chronic (False).

    source of mapping: https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp
    """

    def __init__(self):
        self.filename = "CCIR_v2023-1.csv"
        self.icd10_to_ccir = self._parse_file(self.filename)
        self.icd10_to_ccir_inferred_parents = self._build_inferred_parents(self.icd10_to_ccir)

    def _normalize_code(self, icd10code: str) -> str:
        """
        Normalizes an ICD-10-CM code for lookup.
        icd10code: Raw code string, with or without dots.
        Example: Useful when users input dotted codes like "H81.0".
        """
        return icd10code.replace(".", "")

    def _map_single(self, icd10code: str, allow_parent_inference: bool = True) -> Optional[bool]:
        """
        Maps one ICD-10-CM code to its CCIR classification.
        icd10code: ICD-10-CM diagnostic code in string format.
        allow_parent_inference: Whether to fallback to inferred parent code mappings.
        Example: Useful for truncated codes such as "H81.0" when children are consistent.
        """
        if not isinstance(icd10code, str):
            return None

        normalized_code = self._normalize_code(icd10code)

        if normalized_code in self.icd10_to_ccir:
            return self.icd10_to_ccir[normalized_code]

        if allow_parent_inference:
            return self.icd10_to_ccir_inferred_parents.get(normalized_code)

        return None

    def map(
        self, icd10code: Union[str, Iterable], allow_parent_inference: bool = True
    ) -> Union[Optional[bool], list[Optional[bool]], None]:
        """
        Maps ICD-10-CM code(s) to chronic classification.
        icd10code: ICD-10-CM code string or iterable of codes.
        allow_parent_inference: Whether to infer missing parent codes from consistent children.
        Example: Useful for category-level inputs that are not directly billable.
        """
        if isinstance(icd10code, str):
            return self._map_single(icd10code, allow_parent_inference=allow_parent_inference)
        if isinstance(icd10code, Iterable):
            return [self._map_single(c, allow_parent_inference=allow_parent_inference) for c in icd10code]

        return None

    def _parse_file(self, filename: str) -> dict[str, Optional[bool]]:
        """
        Parses the raw CCIR CSV into an exact-code lookup.
        filename: Package data file name for CCIR mappings.
        Example: Useful when loading CCIR once at mapper initialization.
        """
        with importlib_resources.files(data_files).joinpath(filename).open() as csvfile:
            reader = csv.reader(csvfile, quotechar="'")
            next(reader)
            next(reader)
            next(reader)

            # 9 means not determined.
            ccir_to_bool: dict[str, Optional[bool]] = {"1": True, "0": False, "9": None}
            mapping: dict[str, Optional[bool]] = {}

            for row in reader:
                icd10_code = row[0].strip()
                ccir = ccir_to_bool[row[-1]]
                mapping[icd10_code] = ccir

        return mapping

    def _build_inferred_parents(self, mapping: dict[str, Optional[bool]]) -> dict[str, bool]:
        """
        Builds inferred parent-code mappings when descendants are consistent.
        mapping: Exact ICD-10-CM to CCIR lookup from the source file.
        Example: Useful for inferring "H810" from descendants like "H8101/2/3/9".
        """
        prefix_values: dict[str, set[Optional[bool]]] = {}

        for code, value in mapping.items():
            for prefix_size in range(3, len(code)):
                prefix = code[:prefix_size]
                if prefix in mapping:
                    continue
                if prefix not in prefix_values:
                    prefix_values[prefix] = set()
                prefix_values[prefix].add(value)

        inferred_parents: dict[str, bool] = {}
        for prefix, values in prefix_values.items():
            known_values = {classification for classification in values if classification is not None}
            if len(known_values) == 1:
                inferred_parents[prefix] = known_values.pop()

        return inferred_parents
