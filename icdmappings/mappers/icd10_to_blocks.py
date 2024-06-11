from typing import Union
from collections.abc import Iterable
from .mapper_interface import MapperInterface
import json
import importlib.resources
from icdmappings.data_files import ICD10_CM_Blocks

class ICD10toBlocks(MapperInterface):
        """
        Maps ICD-10 CM diagnostic codes to ICD-10 blocks.
        
        source of mapping: https://icd.who.int/browse10/2010/en
        """
        def __init__(self):
            self.filename = "block_lookup.json"
            self._setup()

        def _setup(self):
            self.block_lookup = self._parse_file(self.filename)
        
        def _map_single(self, icd10code : str) -> str:
            """
            Maps a single ICD-10 CM code in string format to its corresponding block.

            Parameters
            ----------
            icd10code : str
                ICD-10 CM code to be mapped.

            Returns
            -------
            block : str
                Corresponding icd10 block or None if mapping is unsuccessful.
            """

            if not isinstance(icd10code, str): # has to be string
                return None
            

            letter = icd10code[0]

            if letter not in self.block_lookup:
                return None
            
            if len(icd10code) < 3:
                return None
            try:
                num = int(icd10code[1:3])
            except:
                return None
            
            for candidate_block in self.block_lookup[letter]:
                # use python's bisect to check if number is within bounds
                if num >= candidate_block['range'][0] and num <= candidate_block['range'][1]:
                    return candidate_block['block']
            
            return None



        def map(self, icd10code : Union[str, Iterable]) -> Union[str, Iterable]:
            """
            Maps an ICD-10 CM code or an Iterable of ICD-10 CM codes to their corresponding blocks.

            Parameters
            ----------
            code : str | Iterable

            Returns
            -------
            block : str | Iterable
                Corresponding icd10 block(s) or None when mapping is unsuccessful.
            """

            if isinstance(icd10code, str):
                return self._map_single(icd10code)
            elif isinstance(icd10code, Iterable):
                return[self._map_single(code) for code in icd10code]
            
            return None
          
            

        def _parse_file(self, filename : str):
            """
            Preprocessing of bins to optimize assignment speed during mapping.
            1. Separate blocks into numeric codes or alpha codes (There are two blocks considered alpha because they start with "E" or "V")
            2. Create self.bins, which contains starting code ranges of each block
            """

            with importlib.resources.open_text(ICD10_CM_Blocks, filename) as jsonfile:
                block_lookup = json.load(jsonfile)

            return block_lookup