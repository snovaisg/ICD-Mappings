from .mapper_interface import MapperInterface
from collections.abc import Iterable
from typing import Union

class ICD9toLEVEL3(MapperInterface):
    """
    Maps diagnostic ICD-9 codes to the first 3 digits only
    """
    
    def __init__(self):
        super().__init__()
        pass

    def _map_single(self,icd9code : str) -> str:

        if not icd9code: # empty string or None
            return None

        if isinstance(icd9code,str):
            return icd9code[:3]
        

    def map(self, icd9code : Union[str, Iterable]) -> Union[str, Iterable]:
        
        if isinstance(icd9code,str):
            return self._map_single(icd9code)
        
        elif isinstance(icd9code,Iterable):
            return [self._map_single(code) for code in icd9code]
        
        return None