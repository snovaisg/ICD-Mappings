from .mapper_interface import MapperInterface
import pandas as pd 
import numpy as np
from typing import List

class ICD9toLEVEL3(MapperInterface):
        """
        maps diagnostic icd9 codes to the first 3 levels
        """
        
        def __init__(self):
            super().__init__()
            pass

        def map(self, codes : str | List | pd.Series | np.ndarray):
            
            if isinstance(codes,str):
                new_codes = codes[:3]
            
            elif isinstance(codes,(list,np.ndarray)):
                new_codes = [code[:3] if isinstance(code,str) else None for code in codes]

                if isinstance(codes,np.ndarray):
                    new_codes = np.array(new_codes)
            
            elif isinstance(codes,pd.Series):

                new_codes = codes.apply(lambda code: code[:3] if isinstance(code,str) else None)
            
            else:
                 new_codes = None

            return new_codes