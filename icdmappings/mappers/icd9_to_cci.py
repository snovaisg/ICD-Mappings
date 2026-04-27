from __future__ import annotations

from typing import Union
from collections.abc import Iterable
import csv
import importlib_resources
from icdmappings import data_files

class ICD9toCCI:
    """
    Classifies ICD-9-CM diagnostic codes into chronic (True) or not chronic (False).

    source of mapping: https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp
    """

    def __init__(self):
        self.filename = "cci2015.csv"
        self.icd9_to_cci = self._parse_file(self.filename)
        self.icd9_to_cci_inferred_parents = self._build_inferred_parents(self.icd9_to_cci)

    def _normalize_code(self, icd9code: str) -> str:
        """
        Normalizes an ICD-9-CM code for lookup.
        icd9code: Raw ICD-9-CM code string, with or without dots.
        Example: Useful when users input dotted codes like "567.9".
        """
        return icd9code.replace(".", "")

    def _map_single(self, icd9code: str, allow_parent_inference: bool = True) -> Union[bool, None]:
        """
        Maps one ICD-9-CM code to its CCI classification.
        icd9code: ICD-9-CM diagnostic code in string format.
        allow_parent_inference: Whether to fallback to inferred parent-code mappings.
        Example: Useful for truncated codes such as "567" when children are consistent.
        """
        if not isinstance(icd9code, str):
            return None

        normalized_code = self._normalize_code(icd9code)
        if normalized_code in self.icd9_to_cci:
            return self.icd9_to_cci[normalized_code]

        if allow_parent_inference:
            return self.icd9_to_cci_inferred_parents.get(normalized_code)

        return None

    def map(
        self, icd9code: Union[str, Iterable], allow_parent_inference: bool = True
    ) -> Union[bool, list[Union[bool, None]], None]:
        """
        Maps ICD-9-CM code(s) to chronic classification.
        icd9code: ICD-9-CM code string or iterable of codes.
        allow_parent_inference: Whether to infer missing parent codes from consistent children.
        Example: Useful for category-level inputs that are not directly billable.
        """
        if isinstance(icd9code, str):
            return self._map_single(icd9code, allow_parent_inference=allow_parent_inference)
        if isinstance(icd9code, Iterable):
            return [self._map_single(c, allow_parent_inference=allow_parent_inference) for c in icd9code]

        return None

    def _parse_file(self, filename: str) -> dict[str, bool]:
        """
        Parses the raw CCI CSV into an exact-code lookup.
        filename: Package data file name for CCI mappings.
        Example: Useful when loading CCI once at mapper initialization.
        """
        with importlib_resources.files(data_files).joinpath(filename).open() as csvfile:
            reader = csv.reader(csvfile, quotechar="'")
            next(reader)

            cci_to_bool = {"1": True, "0": False}
            mapping: dict[str, bool] = {}

            for row in reader:
                icd9_code = row[0].strip()
                cci = cci_to_bool[row[2]]
                mapping[icd9_code] = cci

        return mapping

    def _build_inferred_parents(self, mapping: dict[str, bool]) -> dict[str, bool]:
        """
        Builds inferred parent-code mappings when descendants are consistent.
        mapping: Exact ICD-9-CM to CCI lookup from the source file.
        Example: Useful for inferring "567" from descendants like "5670/5671/...".
        """
        prefix_values: dict[str, set[bool]] = {}

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
            if len(values) == 1:
                inferred_parents[prefix] = next(iter(values))

        return inferred_parents
