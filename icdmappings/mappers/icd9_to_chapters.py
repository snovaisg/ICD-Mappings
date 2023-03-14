import pandas as pd
import numpy as np

from typing import List
import os
from collections.abc import Iterable
import re
from .mapper_interface import MapperInterface

class ICD9toChapters(MapperInterface):
        """
        Maps icd9 diagnostic codes to icd9 chapters.
        
        source of mapping: https://icd.codes/icd9cm
        """
        def __init__(self):
            self.path2file = "data_sources/icd9-CM-code-chapter-en=PT.csv"
            self._setup()

        def _setup(self):
            filepath = os.path.join(
                os.path.dirname(
                os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))),
                  self.path2file
            )

            # creates self.chapters_num, self.chapters_char, self.bins
            self._parse_file(filepath)


        def map(self, icd9code : str | Iterable):
            """
            
            
            Parameters
            ----------
            
            code : str | Iterable

            Returns
            -------
            
            chapter : str | Iterable
                Corresponding icd9 chapter or None if mapping is unsuccessful.
            """

            def single_lookup(code_):

                def char_lookup(code_):
                    """
                    When the code starts by a char, it's either E or V
                    """
                    if code_[0] == 'E':
                        return "19"
                    elif code_[0] == 'V':
                        return "18"
                    return None

                def int_lookup(code_: str):
                    level_3_code = int(code_[:3])
                    pos = np.digitize(level_3_code,self.bins)
                    chapter = self.chapters_num.Chapter.iloc[pos-1]
                    return str(chapter)

                if code_[0] in ['E','V']:
                    return char_lookup(code_)
                
                return int_lookup(code_)

            def batch_lookup(icd9codes : Iterable):

                if not isinstance(icd9codes,pd.Series):
                    icd9codes = pd.Series(icd9codes)
                
                # to sort everything at the end
                original_order = icd9codes.index.copy()
                
                mask_is_alpha = icd9codes.apply(lambda x: (x[0] == 'E') | (x[0] == 'V') if not pd.isna(x) else False)
                codes_nan = icd9codes[pd.isna(icd9codes)]

                codes_char = (icd9codes
                              .loc[mask_is_alpha]
                              .copy()
                              .apply(lambda x:x[0]) # only need first character to identify chapter
                             )
                
                codes_num = (icd9codes
                             .loc[~icd9codes.index.isin(codes_char.index.tolist() + codes_nan.index.tolist())]
                             .copy()
                             .apply(lambda x: x[:3]) # only need first 3 characters to identify chapter
                             .astype(int)
                            )
                
                
                # get chapters of numeric codes
                num_chapters = (pd.Series(data=np.digitize(codes_num,self.bins),
                                          index=codes_num.index)
                               )
                
                
                char_chapters = codes_char.apply(single_lookup)
                result = (pd.concat([num_chapters,char_chapters,codes_nan],axis='rows') # merge chapters of numerical & alpha codes
                          .loc[original_order] # get original order
                          .astype(str)
                          .tolist()
                         )
                
                if isinstance(icd9codes, np.ndarray):
                    result = np.array(result)
                elif isinstance(icd9codes, pd.Series):
                    result = pd.Series(result,index=original_order)

                return result
            

            if isinstance(icd9code,str):
                return single_lookup(icd9code)
            elif isinstance(icd9code,Iterable):
                if not all([isinstance(code,str) for code in icd9code]):
                    raise TypeError(f'All icd9 codes in iterable must be str (or None)')
                return batch_lookup(icd9code)
            raise TypeError(f'Expecting code to be either str or Iterable.')

        def _parse_file(self,filepath : str):
            """
            Some preprocessing to optimize assignment speed later using np.digitize
            1. Separate chapters into numeric codes or alpha codes (There are two chapters considered alpha because they start with "E" or "V")
            2. Create self.bins, which contains starting code ranges of each chapter
            """
            
            self.chapters = pd.read_csv(filepath)

            # preprocess chapters dataframe: split into alpha vs numeric
            self.chapters['start_range'] = self.chapters['Code Range'].apply(lambda x: x.split('-')[0])

            chapters_char = (self.chapters
                           .loc[self.chapters.start_range
                                .apply(lambda x: len(re.findall(r'^(E|V)',x)) > 0),
                                ['Chapter','Description','Code Range']
                               ]
                          )
            # only need the first letter
            chapters_char.loc[:,'Code Range'] = chapters_char['Code Range'].apply(lambda x: x[0])

            chapters_num = (self.chapters
                          .loc[~self.chapters.index.isin(chapters_char.index)]
                          .astype({'start_range':int}).copy()
                         )

            bins = chapters_num.start_range.tolist()

            # need to add last interval
            bins.append(bins[-1]+205)

            self.bins = bins
            self.chapters_num = chapters_num
            self.chapters_char = chapters_char