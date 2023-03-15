from .mapper_interface import MapperInterface
from collections.abc import Iterable

class ICD9toLEVEL3(MapperInterface):
    """
    maps diagnostic icd9 codes to the first 3 levels
    """
    
    def __init__(self):
        super().__init__()
        pass

    def _map_single(self,icd9code : str):

        if isinstance(icd9code,str):
            return icd9code[:3]
        return None

    def map(self, icd9code : str | Iterable):
        
        if isinstance(icd9code,str):
            return self._map_single(icd9code)
        elif isinstance(icd9code,Iterable):
            return [ self._map_single(code) for code in icd9code ]
        TypeError(f'Wrong input type. Expecting str or Iterable. Got {type(icd9code)}')