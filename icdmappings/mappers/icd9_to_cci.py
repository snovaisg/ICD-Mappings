import pandas as pd
import numpy as np
from typing import List
import os
from collections.abc import Iterable
import re


class ICD9toCCI:
        """
        Maps icd9 diagnostic codes to chronic or not chronic (that is the question).
        
        source of mapping: https://www.hcup-us.ahrq.gov/toolssoftware/chronic/chronic.jsp
        """
        def __init__(self):
            self.path2file = "data_sources/cci2015.csv"

            self.icd9_to_cci = None # will be filled by self._setup() {icd9code:cci,...icd9code:cci}
            self._setup()


        def _setup(self):
            filepath = os.path.join(
                os.path.dirname(
                os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))),
                  self.path2file
            )

            # creates self.chapters_num, self.chapters_char, self.bins
            self.icd9_to_cci = self._parse_file(filepath)


        def map(self,
                icd9code : str | Iterable
                ):
                """
                Given an icd9 code, returns the corresponding Chronic value (True for chronic, and False for not-chronic)

                Parameters
                ----------

                code : str | pd.Series
                    icd9 code

                Returns:
                    -1: code is not recognizable
                    True: When the code is chronic
                    False: when the code is not chronic
                """
                def lookup_single(icd9code : str):
                    try:
                        return self.icd9_to_cci[icd9code]
                    except:
                        return None
                if isinstance(icd9code, str):
                    return lookup_single(icd9code)
                elif isinstance(icd9code, Iterable):
                    mapping =  [lookup_single(c) for c in icd9code]
                    
                    if isinstance(icd9code, np.ndarray):
                        mapping = np.array(mapping)

                    elif isinstance(icd9code, pd.Series):
                        mapping = pd.Series(mapping, index=icd9code.index)
                    return mapping
                
                raise TypeError(f'Wrong input type. Expecting str or Iterable. Got {type(icd9code)}')


        def _parse_file(self, filepath : str):
            df = pd.read_csv(filepath,usecols=[0,2])
            df.columns = [col.replace("'","") for col in df.columns]
            df['ICD-9-CM CODE'] = df['ICD-9-CM CODE'].str.replace("'","").str.strip()
            df['CATEGORY DESCRIPTION'] = df['CATEGORY DESCRIPTION'].str.replace("'","").str.strip()
            df = df.rename(columns={'CATEGORY DESCRIPTION':'CHRONIC'})
            df['CHRONIC'] = df['CHRONIC'].map({'0':False,'1':True})

            return df.set_index('ICD-9-CM CODE')['CHRONIC'].to_dict()
        