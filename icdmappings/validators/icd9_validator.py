from .icd_validator_interface import ICDValidatorInterface
from typing import List, Union
import os
from collections.abc import Iterable
import importlib.resources
from icdmappings import data_files
from icdmappings.data_files import ICD_9_CM_v32_master_descriptions


class ICD9Validator(ICDValidatorInterface):
        """
        Checks if a code is icd9-cm version 32 compliant.
        """
        
        def __init__(self):
            self.diagnostics_filename = 'CMS32_DESC_LONG_DX.txt'
            self.procedures_filename = 'CMS32_DESC_LONG_SG.txt'
            self._setup()
        
        def _setup(self):
            self.diagnostics = self._parse_file(self.diagnostics_filename)
            self.procedures = self._parse_file(self.procedures_filename)
            pass
        

        def validate_diagnostics(self, 
                                codes : Union[str,Iterable],
                                ) -> Union[bool, Iterable]:
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
                               codes : Union[str, Iterable],
                              ) -> Union[bool, Iterable]:
            
            if codes is None:
                return None
            if isinstance(codes,str):
                return codes in self.procedures.keys()
            elif isinstance(codes,Iterable):
                valid = [code in self.procedures.keys() if code is not None else None for code in codes]
                return valid
            raise TypeError('Expects a string or iterable of strings as codes.')

        def _parse_file(self,filename : str):
            """Parses a data file of icd9 codes. and returns a dictionary of codes and descriptions.

            Args:
                f (str): file path to read from.

            Returns:
                data[code]: description
            """
            data = dict()
            with importlib.resources.open_text(ICD_9_CM_v32_master_descriptions, filename,encoding='latin-1') as f:
                for line in f:
                    code,desc = line.split(sep=' ', maxsplit=1)
                    data[code] = desc.strip()
            return data