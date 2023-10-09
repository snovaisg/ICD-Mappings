from typing import Union
from collections.abc import Iterable
import csv
from .mapper_interface import MapperInterface
import importlib.resources
from icdmappings import data_files

class ICD9Level3toCCI(MapperInterface):
    """
    Maps icd9_level3 codes (i.e. not the full code, only the first 3 digits) to ccs.
    
    TODO: add checker for eligible icd9 codes. For now just assumes the input is a 3rd level icd9 code without checking properly.
    """
    
    def __init__(self):
        self.filename = "cci2015.csv"
        self.icd9level3_to_cci = None # will be filled by self._setup() {icd9code_level3:cci, ..., icd9code_level3:cci}
        self._setup()

    def _setup(self):
        self.icd9level3_to_cci = self._parse_file(self.filename)
    
    def _map_single(self, icd9level3code : str):
        return self.icd9level3_to_cci.get(icd9level3code)
        
    def map(self, icd9code : Union[str, Iterable]) -> Union[str, Iterable]:
        """
        Given an icd9level3 code (first 3 digits only), returns the corresponding Chronic classification
        (True for chronic, and False for not-chronic)

        Parameters
        ----------
        code : str or Iterable
            icd9 code or iterable of icd9 codes in string format.

        Returns
        -------
        True: When the code is chronic
        False: when the code is not chronic
        None: code is not recognizable
        """

        if isinstance(icd9code, str):
            return self._map_single(icd9code)
        elif isinstance(icd9code, Iterable):
            return [self._map_single(c) for c in icd9code]
    
    def _parse_file(self, filename : str):
        with importlib.resources.open_text(data_files, filename) as csvfile:
            reader = csv.reader(csvfile, quotechar="'")
            headers = next(reader)

            cci_to_bool = {'1':True,'0':False}

            mapping = {}

            for row in reader:
                icd9_code = row[0].strip()
                icd9level3_code = icd9_code[:3]
                cci = cci_to_bool[row[2]]
                if icd9level3_code in mapping and cci != mapping[icd9level3_code]:
                    mapping[icd9level3_code] = None #there are multiple, go back to None
                mapping[icd9level3_code] = cci

        return mapping