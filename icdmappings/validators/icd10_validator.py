from .icd_validator_interface import ICDValidatorInterface
from typing import List, Union
import os
from collections.abc import Iterable
import importlib.resources
from icdmappings import data_files
from icdmappings.data_files import ICD_10_CM_2024_release



class ICD10Validator(ICDValidatorInterface):
        """
        Validates if a code is icd10-cm.
        """
        
        def __init__(self):
            self.diagnostics_filename = 'icd10cm-codes-2024.txt'
            self.procedures_filename = 'icd10pcs-codes-2024.txt'
            self._setup()
        
        def _setup(self):
            result = self._parse_files(self.diagnostics_filename, self.procedures_filename)
            self.diagnostics = result['diagnostics']
            self.procedures = result['procedures']

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


        def _parse_files(self,
                         filename_diagnostics : str,
                         filename_procedures : str
                        ):
            """Parses a data file of icd9 codes. and returns a dictionary of codes and descriptions.

            Args:
                f (str): file path to read from.

            Returns:
                data[code]: description
            """

            diagnostics_data = dict()
            with importlib.resources.open_text(ICD_10_CM_2024_release, filename_diagnostics, encoding='latin-1') as f:
                for line in f:
                    tokens = line.split(sep=' ')
                    code = tokens[0]
                    desc = ' '.join(tokens[1:])
                    diagnostics_data[code] = desc.strip()
            
            procedures_data = dict()
            with importlib.resources.open_text(ICD_10_CM_2024_release, filename_procedures, encoding='latin-1') as f:
                for line in f:
                    tokens = line.split(sep=' ')
                    code = tokens[0]
                    desc = ' '.join(tokens[1:])
                    procedures_data[code] = desc.strip()

            return {'diagnostics': diagnostics_data, 'procedures': procedures_data}