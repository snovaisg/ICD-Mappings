from .icd_validator_interface import ICDValidatorInterface
from typing import List, Union
import os
from collections.abc import Iterable
import importlib.resources
from icdmappings import data_files
from icdmappings.data_files import ICD_9_CM_v32_master_descriptions


class ICD9Validator(ICDValidatorInterface):
        """
        Validates if a code is icd9-cm version 32 compliant.
        """
        
        def __init__(self):
            self.diagnostics_filename = 'CMS32_DESC_LONG_DX.txt'
            self.procedures_filename = 'CMS32_DESC_LONG_SG.txt'
            self._setup()
        
        def _setup(self):
            self.diagnostics = self._parse_file(self.diagnostics_filename)
            self.procedures = self._parse_file(self.procedures_filename)
            pass

        def _validate_single_diagnostic(self, code: str):
            return code in self.diagnostics.keys()
        
        def _validate_single_procedure(self, code: str):
            return code in self.procedures.keys()
        
        def validate_diagnostics(self, 
                     code : Union[str,Iterable],
                     ) -> Union[bool, Iterable]:
            """Validates if a diagnostic code or iterable of diagnostic codes are valid.
            If iterable is numpy or pd.Series, returns the same type. ALL other iterables are returned as List.

            Parameters
            ----------
            code: str or Iterable

            Returns
            -------
            True when the code is a valid code
            False when the code is not a valid code
            """

            if isinstance(code, str):
                return self._validate_single_diagnostic(code)
            elif isinstance(code, Iterable):
                return [self._validate_single_diagnostic(c) for c in code]
            return False
        
        def validate_procedures(self, 
                     code : Union[str,Iterable],
                     ) -> Union[bool, Iterable]:
            """Validates if a procedure code or iterable of procedure codes are valid.
            If iterable is numpy or pd.Series, returns the same type. ALL other iterables are returned as List.

            Parameters
            ----------
            code: str or Iterable

            Returns
            -------
            True when the code is a valid code
            False when the code is not a valid code
            """

            if isinstance(code, str):
                return self._validate_single_procedure(code)
            elif isinstance(code, Iterable):
                return [self._validate_single_procedure(c) for c in code]
            return False


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