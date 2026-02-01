from collections.abc import Iterable
from .mapper_interface import MapperInterface
import csv
from typing import Union
import importlib_resources
from icdmappings.data_files import pediatric_ccc


class ICD10toCCCSubcategory(MapperInterface):
    """
    Maps ICD-10 codes to CCC (Complex Chronic Conditions) subcategories.

    Source of mapping: Pediatric Complex Chronic Conditions Classification System
    """
    def __init__(self):
        self.filename = "ccc_mappings.csv"
        self._setup()

    def _setup(self):
        self.mapping = self._parse_file(self.filename)

    def _map_single(self, code: str):
        if isinstance(code, str):
            code = code.replace('.', '')
        return self.mapping.get(code)

    def map(self, code: Union[str, Iterable]) -> Union[str, Iterable]:
        """
        Given an ICD-10 code, returns the corresponding CCC subcategory.

        Parameters
        ----------
        code : str | Iterable
            ICD-10 code(s)

        Returns:
            CCC subcategory or None when the mapping is not possible
        """
        if isinstance(code, str):
            return self._map_single(code)
        elif isinstance(code, Iterable):
            return [self._map_single(c) for c in code]

    def _parse_file(self, filename: str):
        mapping = {}
        with importlib_resources.files(pediatric_ccc).joinpath(filename).open() as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                icd_code = str(row[0])          # ICD_Code
                icd_version = int(row[5])       # ICD9_ICD10 (9=ICD9, 0=ICD10)
                ccc_subcategory = row[4]        # CCC_Subcategory
                if icd_version == 0:            # Filter for ICD-10 only
                    mapping[icd_code] = ccc_subcategory
        return mapping
