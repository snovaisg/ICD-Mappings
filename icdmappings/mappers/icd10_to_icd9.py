import pandas as pd
import numpy as np
import os
from collections.abc import Iterable
from .mapper_interface import MapperInterface



class ICD10toICD9(MapperInterface):
    """
    Maps icd10 codes to icd9.
    
    
    Source of mapping: https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings
    """
    def __init__(self):
        self.path2file = "data_sources/icd10cmtoicd9gem.csv"
        self._setup()

    def _setup(self):
        filepath = os.path.join(
            os.path.dirname(
            os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))),
                self.path2file
        )
        
        self.icd10_to_icd9 = self._parse_file(filepath)

    def map(self,
            icd10code : str | Iterable
            ):
        """
        Given an icd10 code, returns the corresponding icd9 code.

        Parameters
        ----------

        code : str | Iterable
            icd10 code

        Returns:
            icd9 code or np.nan when the mapping is not possible
        """
        def lookup_single(icd10code : str):
            try:
                return self.icd10_to_icd9[icd10code]
            except:
                return None
            
        if isinstance(icd10code, str):
            return lookup_single(icd10code)

        elif isinstance(icd10code, Iterable):
            mapping = [ lookup_single(c) for c in icd10code ]

            if isinstance(icd10code, np.ndarray):
                mapping =  np.array(mapping)
            elif isinstance(icd10code, pd.Series):
                mapping =  pd.Series(mapping, index=icd10code.index)
            
            return mapping
        
        raise TypeError(f'Wrong input type. Expecting str or pd.Series. Got {type(icd10code)}')    


    def _parse_file(self, filepath : str):
        df = pd.read_csv(filepath, dtype={'icd10cm':str,'icd9cm':str})

        df.loc[df.no_map == 1,'icd9cm'] = "-1"

        mappings = dict()

        records = df.set_index('icd10cm')['icd9cm'].to_dict()

        mappings.update(records) # currently, rewrites with the last mapping when there are multiple mappings for the same icd9 code

        return mappings