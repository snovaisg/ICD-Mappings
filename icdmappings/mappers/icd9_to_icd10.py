import os
from collections.abc import Iterable
from .mapper_interface import MapperInterface
import csv


class ICD9toICD10(MapperInterface):
    """
    Maps icd9 codes into icd10.
    
    
    Source of mapping: https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings
    """
    def __init__(self):
        self.path2file = "data_sources/icd9toicd10cmgem.csv"
        self._setup()

    def _setup(self):
        filepath = os.path.join(
            os.path.dirname(
            os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))),
                self.path2file
        )

        # creates self.chapters_num, self.chapters_char, self.bins
        self.icd9_to_icd10 = self._parse_file(filepath)

    def map(self,icd9code : str | Iterable):
            """
            Given an icd9 code, returns the corresponding icd10 code.

            Parameters
            ----------

            code : str | pd.Series
                icd9 code

            Returns:
                icd10 code or None when the mapping is not possible
            """
            def map_single(code : str):
                try:
                    return self.icd9_to_icd10[code]
                except:
                    return None
            
            if isinstance(icd9code, str):
                return  map_single(icd9code)
            elif isinstance(icd9code, Iterable):
                return [ map_single(c) for c in icd9code ]
            
            raise TypeError(f'Wrong input type. Expecting str or Iterable. Got {type(icd9code)}')


    def _parse_file(self, filepath : str):

        mapping = {}

        with open(filepath) as csvfile:
            reader = csv.reader(csvfile, quotechar='"')
            headers = next(reader)

            for row in reader:
                icd9, icd10 = row[0], row[1]

                mapping[icd9] = icd10
        return mapping

