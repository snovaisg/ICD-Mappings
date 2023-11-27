from typing import List, Union
import os
from collections.abc import Iterable
import csv
import importlib.resources
from icdmappings import data_files

class ICD10toCCIR:
        """
        Classifies ICD10 diagnostic codes into chronic (True) or not chronic (False).
        
        source of mapping: https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp
        """
        def __init__(self):
            self.filename = "CCIR_v2023-1.csv"
            self.icd10_to_ccir = self._parse_file(self.filename) # {icd10code:cci,...icd10code:cci}

        def _map_single(self, icd10code : str) -> str:
             return self.icd10_to_ccir.get(icd10code)


        def map(self, icd10code : Union[str, Iterable]) -> Union[str, Iterable]:
            """
            Given an icd10 code, returns the corresponding Chronic classification
            (True for chronic, and False for not-chronic)

            Parameters
            ----------
            icd10code : str or Iterable
                icd9 code or iterable of icd10 codes in string format.

            Returns
            -------
            True: When the code is chronic
            False: when the code is not chronic
            None: code is not recognizable
            """

            if isinstance(icd10code, str):
                return self._map_single(icd10code)
            elif isinstance(icd10code, Iterable):
                return [self._map_single(c) for c in icd10code]


        def _parse_file(self, filename : str):
            with importlib.resources.open_text(data_files, filename) as csvfile:
                reader = csv.reader(csvfile, quotechar="'")
                headers = next(reader)
                more_headers = next(reader)
                and_more_headers = next(reader)

                # 9 means not determined
                ccir_to_bool = {'1':True, '0':False, '9': None}

                mapping = {}

                for row in reader:
                    icd10_code = row[0].strip()
                    ccir = ccir_to_bool[row[-1]]
                    mapping[icd10_code] = ccir

            return mapping