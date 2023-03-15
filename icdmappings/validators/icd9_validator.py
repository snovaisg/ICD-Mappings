from .icd_validator_interface import ICDValidatorInterface
from typing import List
import os
from collections.abc import Iterable

class ICD9Validator(ICDValidatorInterface):
        """
        Checks if a code is icd9-cm version 32 compliant.
        """
        
        def __init__(self):
            self.path2folder = "data_sources/ICD-9-CM-v32-master-descriptions"
            self._setup()
        
        def _setup(self):
             self.path2folder = os.path.join(
                 os.path.dirname(
                   os.path.dirname(
                   os.path.dirname(os.path.abspath(__file__)))
                 ), self.path2folder)
             self.diagnostics = self._parse_diagnostics()
             self.procedures = self._parse_procedures()
             pass
        

        def validate_diagnostics(self, 
                                codes : str | Iterable,
                                ) -> bool | Iterable:
            """validates if a code or iterable of codes are valid diagnostics.
            If iterable is numpy or pd.Series, returns the same type. ALl other iterables are returned as List.

            Args:
                codes (str | List | pd.Series | np.ndarray): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool | List | pd.Series | np.ndarray: _description_
            """
            if codes is None:
                return None
            if isinstance(codes,str):
                return codes in self.diagnostics.keys()
            elif isinstance(codes,Iterable):
                valid = [code in self.diagnostics.keys() if code is not None else None for code in codes]
                return valid
            raise TypeError('Expects a string or iterable of strings as codes.')
        
        def validate_procedures(self,
                               codes : str | Iterable,
                              ) -> bool | Iterable:
            
            if codes is None:
                return None
            if isinstance(codes,str):
                return codes in self.procedures.keys()
            elif isinstance(codes,Iterable):
                valid = [code in self.procedures.keys() if code is not None else None for code in codes]
                return valid
            raise TypeError('Expects a string or iterable of strings as codes.')
        
        def _parse_diagnostics(self):
            f = os.path.join(self.path2folder, f"CMS32_DESC_LONG_DX.txt")
            return self._parse_file(f)
        
        def _parse_procedures(self):
            f = os.path.join(self.path2folder, f"CMS32_DESC_LONG_SG.txt")
            return self._parse_file(f)

        def _parse_file(self,f):
            """Parses a data file of icd9 codes. and returns a dictionary of codes and descriptions.

            Args:
                f (str): file path to read from.

            Returns:
                data[code]: description
            """
            data = dict()
            with open(f,'r', encoding='latin-1') as f:
                for line in f:
                    code,desc = line.split(sep=' ', maxsplit=1)
                    data[code] = desc.strip()
            return data