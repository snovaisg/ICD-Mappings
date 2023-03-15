from .mappers import * 
from .validators import ICD9Validator
from collections.abc import Iterable
class Mapper():

    def __init__(self):

        # mappers
        self.icd9_to_cci = ICD9toCCI()
        self.icd9_to_level3 = ICD9toLEVEL3()
        self.icd9_to_ccs = ICD9toCCS()
        self.icd9_to_chapters = ICD9toChapters()
        self.icd9_to_icd10 = ICD9toICD10()
        self.icd10_to_icd9 = ICD10toICD9()

        self._internal_mapping = {
            'icd9tocci': self.icd9_to_cci,
            'icd9tolevel3': self.icd9_to_level3,
            'icd9toccs': self.icd9_to_ccs,
            'icd9tochapter': self.icd9_to_chapters,
            'icd9toicd10': self.icd9_to_icd10,
            'icd10toicd9': self.icd10_to_icd9
        }

        # validators

        self.icd9_validator = ICD9Validator()

        self._internal_validators = {
            'icd9': self.icd9_validator
        }


    def show_mappers(self):
        return list(self._internal_mapping.keys())
    
    def show_validators(self):
        return list(self._internal_validators.keys())
    
    def validate_diagnostics(self, category : str, codes : str | Iterable):

        validator = self._get_validator(category)
        
        return validator.validate_diagnostics(codes)
    
    def validate_procedures(self, category : str, codes : str | Iterable):

        validator = self._get_validator(category)
        
        return validator.validate_procedures(codes)

    def _get_validator(self, category : str):
        validator = self._internal_validators.get(category)

        if validator is None:
            raise ValueError(f"Category must be one of the following {str(self._internal_validators.keys())}")
        return validator

    def map(self, 
            codes : str | Iterable,
            mapper : str):
        
        mapper = self._internal_mapping.get(mapper)

        if mapper is None:
            raise ValueError(f"Mapper {mapper} not found. Please choose one from: {str(self.show_mappers())}.")
        
        mapping = mapper.map(codes)
        
        return mapping