from abc import ABC, abstractclassmethod
import numpy as np
import pandas as pd
from typing import List

class MapperInterface(ABC):
    """
    Abstract class for mapping classes.
    """

    def __init__(self):
        self._supported_inputs = [str,list,pd.Series,np.ndarray]
    
    @abstractclassmethod
    def map(self, 
            codes : str | List | pd.Series | np.ndarray,
            ) -> str | List | pd.Series | np.ndarray | None:
        """
        Maps input codes to target encoding. 
        If unsuccessful mapping, returns None.
        """
        pass