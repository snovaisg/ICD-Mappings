from typing import Union
from collections.abc import Iterable
from .mapper_interface import MapperInterface
import json
import importlib.resources
from icdmappings.data_files import ICD10_CM_CCSR

class ICD10toCCSR(MapperInterface):
        """
        Maps ICD-10 CM diagnostic codes to CCS(R) chapters.
        
        source of mapping: https://hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp
        """
        def __init__(self):
            self.filename = "dx_cat1_mapping.json"
            self._setup()

        def _setup(self):
            self.ccsr_lookup = self._parse_file(self.filename)
        
        def _map_single(self, icd10code : str) -> str:
            """
            Maps a single ICD-10 CM code in string format to its 
            corresponding CCS(R) code (Category 1).

            Why map to Category 1 of CCS(R)? Some ICD10-CM codes can map to 
            several CCS(R) categories, when this happens it is because 
            the condition can be specified with greater detail (Categories 2-6).

            By default, for now, we will map to Category 1, which is probably 
            enough to satisfy most use cases.

            Parameters
            ----------
            icd10code : str
                ICD-10 CM code to be mapped.

            Returns
            -------
            ccsr : str
                Corresponding CCS(R) code (Category 1) or None if mapping is unsuccessful.
            """

            if not isinstance(icd10code, str): # has to be string
                return None
            
            return self.ccsr_lookup.get(icd10code)



        def map(self, icd10code : Union[str, Iterable]) -> Union[str, Iterable]:
            """
            Maps an ICD-10 CM code or an Iterable of ICD-10 CM codes to their corresponding chapters.

            Parameters
            ----------
            code : str | Iterable

            Returns
            -------
            chapter : str | Iterable
                Corresponding icd10 chapter(s) or None when mapping is unsuccessful.
            """

            if isinstance(icd10code, str):
                return self._map_single(icd10code)
            
            elif isinstance(icd10code, Iterable):
                return[self._map_single(code) for code in icd10code]
            
            return None
          
            

        def _parse_file(self, filename : str):
            """
            Preprocessing of bins to optimize assignment speed during mapping.
            1. Separate chapters into numeric codes or alpha codes (There are two chapters considered alpha because they start with "E" or "V")
            2. Create self.bins, which contains starting code ranges of each chapter
            """

            with importlib.resources.open_text(ICD10_CM_CCSR, filename) as jsonfile:
                ccsr_lookup = json.load(jsonfile)

            return ccsr_lookup