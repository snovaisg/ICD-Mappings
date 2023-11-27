from abc import ABC, abstractclassmethod
from collections.abc import Iterable
from typing import Union

class ICDValidatorInterface(ABC):
    """
    Abstract class for mapping classes.
    """

    def __init__(self):
        pass

    
    
    @abstractclassmethod
    def validate_diagnostics(self, 
            codes : Union[str, Iterable],
            ) -> Union[bool, Iterable]:
        """
        Returns True of False if the code is a valid diagnostic code.
        """
        pass

    @abstractclassmethod
    def validate_procedures(self, 
            codes : Union[str, Iterable],
            ) -> Union[bool, Iterable]:
        """
        Returns True of False if the code is a valid procedure code.
        """
        pass