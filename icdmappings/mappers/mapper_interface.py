from abc import ABC, abstractclassmethod
from typing import List, Union
from collections.abc import Iterable

class MapperInterface(ABC):
    """
    Abstract class for mapping classes.
    """

    def __init__(self):
        pass
    
    @abstractclassmethod
    def map(self, 
            codes : Union[str, Iterable],
            ) -> Union[str, Iterable]:
        """
        Maps input codes to target encoding. 
        If unsuccessful mapping, returns None.
        """
        pass