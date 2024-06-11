from .mappers import * 
from .validators import *
from collections.abc import Iterable
from typing import Union
class Mapper():

    def __init__(self):

        # mappers
        self.icd9_to_cci = ICD9toCCI()
        self.icd9_to_ccs = ICD9toCCS()
        self.icd9_to_chapters = ICD9toChapters()
        self.icd9_to_icd10 = ICD9toICD10()
        self.icd10_to_icd9 = ICD10toICD9()
        self.icd10_to_blocks = ICD10toBlocks()
        self.icd10_to_chapters = ICD10toChapters()
        self.icd10_to_ccsr = ICD10toCCSR()
        self.icd10_to_ccir = ICD10toCCIR()

        self._internal_mapping = {
                'icd9':{'cci':self.icd9_to_cci,
                        'ccs':self.icd9_to_ccs,
                        'chapter':self.icd9_to_chapters,
                        'icd10':self.icd9_to_icd10
                        },
                'icd10':{'icd9':self.icd10_to_icd9,
                         'block':self.icd10_to_blocks,
                         'chapter':self.icd10_to_chapters,
                         'ccsr':self.icd10_to_ccsr,
                         'ccir': self.icd10_to_ccir
                         }
                        }

    def show_mappers(self):
        print('Here are the available mappers\n')
        for _from in self._internal_mapping:
            print('From ' + _from + ' to:')
            for _to in self._internal_mapping[_from]:
                print('\t- ' + _to)
    
    def validate_diagnostics(self, codes : Union[str,Iterable], category : str):

        validator = self._get_validator(category)
        
        return validator.validate_diagnostics(codes)
    
    def validate_procedures(self, codes : Union[str,Iterable], category : str):

        validator = self._get_validator(category)
        
        return validator.validate_procedures(codes)

    def _get_validator(self, category : str):
        validator = self._internal_validators.get(category)

        if validator is None:
            raise ValueError(f"Category must be one of the following {str(self._internal_validators.keys())}")
        return validator

    def map(self, 
            codes : Union[str, Iterable],
            source : str,
            target : str):
    
        _source = self._internal_mapping.get(source)
    
        if _source is None:
            raise ValueError(f'There\'s no mapper that starts from {source} codes. Available starting codes are: {str(list(self._internal_mapping.keys()))}. Use .show_mappers() for more info.')
        
        mapper = _source.get(target)
    
        if mapper is None:
            raise ValueError(f'There\'s no mapper that maps from {source} to {target}. Available mappers can only map from {source} to {str(list(_source.keys()))}. Use .show_mappers() for more info.')
        
        mapping = mapper.map(codes)
        
        return mapping

class Validator():
    """
    This class is for validating codes.
    """

    def __init__(self):
        self.icd9_validator = ICD9Validator()
        self.icd10_validator = ICD10Validator()

        self._internal_validators = {
            'icd9_diagnostic': (self.icd9_validator, 'diagnostic'),
            'icd9_procedure': (self.icd9_validator, 'procedure'),
            'icd10_diagnostic': (self.icd10_validator, 'diagnostic'),
            'icd10_procedure': (self.icd10_validator, 'procedure')
        }

    def show_validators(self):
        return list(self._internal_validators.keys())
    
    def validate(self, codes : Union[str,Iterable], expects : str):

        validator, _type = self._internal_validators.get(expects)

        match _type:

            case 'diagnostic':
                return validator.validate_diagnostics(codes)
            case 'procedure':
                return validator.validate_procedures(codes)