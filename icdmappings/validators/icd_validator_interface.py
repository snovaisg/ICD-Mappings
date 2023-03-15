from abc import ABC, abstractclassmethod
from collections.abc import Iterable

class ICDValidatorInterface(ABC):
    """
    Abstract class for mapping classes.
    """

    def __init__(self):
        pass
    
    @abstractclassmethod
    def validate_diagnostics(self, 
            codes : str | Iterable,
            ) -> bool | Iterable:
        """
        Returns True of False if the code is a valid diagnostic code.
        """
        pass

    @abstractclassmethod
    def validate_procedures(self, 
            codes : str | Iterable,
            ) -> bool | Iterable:
        """
        Returns True of False if the code is a valid procedure code.
        """
        pass