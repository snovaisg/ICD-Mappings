from abc import ABC, abstractclassmethod
import numpy as np
import pandas as pd
from typing import List

class ICDValidatorInterface(ABC):
    """
    Abstract class for mapping classes.
    """

    def __init__(self):
        pass
    
    @abstractclassmethod
    def validate_diagnostics(self, 
            codes : str | List | pd.Series | np.ndarray,
            ) -> bool | List | pd.Series | np.ndarray:
        """
        Returns True of False if the code is a valid diagnostic code.
        """
        pass

    @abstractclassmethod
    def validate_procedures(self, 
            codes : str | List | pd.Series | np.ndarray,
            ) -> bool | List | pd.Series | np.ndarray:
        """
        Returns True of False if the code is a valid procedure code.
        """
        pass