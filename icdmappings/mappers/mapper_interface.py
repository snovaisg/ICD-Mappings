from abc import ABC, abstractclassmethod
from typing import List
from collections.abc import Iterable

class MapperInterface(ABC):
    """
    Abstract class for mapping classes.
    """

    def __init__(self):
        pass
    
    @abstractclassmethod
    def map(self, 
            codes : str | Iterable,
            ) -> str | Iterable:
        """
        Maps input codes to target encoding. 
        If unsuccessful mapping, returns None.
        """
        pass