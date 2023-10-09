import os
from collections.abc import Iterable
from .mapper_interface import MapperInterface
import csv
from typing import Union
import importlib.resources
from icdmappings import data_files


class ICD9toICD10(MapperInterface):
    """
    Maps icd9 codes into icd10.
    
    Source of mapping: https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings
    """
    def __init__(self):
        self.filename = "icd9toicd10cmgem.csv"
        self._setup()

    def _setup(self):
        self.icd9_to_icd10 = self._parse_file(self.filename)

    def _map_single(self, icd9code : str):
            
        return self.icd9_to_icd10.get(icd9code)

    def map(self, icd9code : Union[str, Iterable]) -> Union[str, Iterable]:
            """
            Given an icd9 code, returns the corresponding icd10 code.

            Parameters
            ----------

            code : str | pd.Series
                icd9 code

            Returns:
                icd10 code or None when the mapping is not possible
            """
            
            if isinstance(icd9code, str):
                return  self._map_single(icd9code)
            
            elif isinstance(icd9code, Iterable):
                return [self._map_single(c) for c in icd9code]

    def _parse_file(self, filename : str):

        mapping = {}

        with importlib.resources.open_text(data_files, filename) as csvfile:
            reader = csv.reader(csvfile, quotechar='"')
            headers = next(reader)

            for row in reader:
                icd9, icd10 = row[0], row[1]

                mapping[icd9] = icd10
        return mapping

