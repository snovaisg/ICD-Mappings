import os
from collections.abc import Iterable
from .mapper_interface import MapperInterface
import csv
from typing import Union
import importlib.resources
from icdmappings import data_files

class ICD10toICD9(MapperInterface):
    """
    Maps icd10 codes to icd9.
    
    Source of mapping: https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings
    """
    def __init__(self):
        self.filename = "icd10cmtoicd9gem.csv"
        self._setup()

    def _setup(self):
        self.icd10_to_icd9 = self._parse_file(self.filename)


    def _map_single(self, icd10code : str):
        return self.icd10_to_icd9.get(icd10code)

    def map(self, icd10code : Union[str, Iterable]) -> Union[str, Iterable]:
        """
        Given an icd10 code, returns the corresponding icd9 code.

        Parameters
        ----------

        code : str | Iterable
            icd10 code

        Returns:
            icd9 code or None when the mapping is not possible
        """
            
        if isinstance(icd10code, str):
            return self._map_single(icd10code)

        elif isinstance(icd10code, Iterable):
            return [self._map_single(c) for c in icd10code]
        
        return None


    def _parse_file(self, filename : str):

        mapping = {}

        with importlib.resources.open_text(data_files, filename) as csvfile:
            reader = csv.reader(csvfile, quotechar='"')
            headers = next(reader)

            for row in reader:
                icd10, icd9 = row[0].strip(), row[1].strip()

                mapping[icd10] = icd9
        return mapping