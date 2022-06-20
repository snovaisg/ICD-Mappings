# +
import pandas as pd
import numpy as np
import re

class ICDCodesGrouper(object):
    """
    Class containing several icd9 grouping subclasses.
    all grouper subclasses implement the method "lookup".
    
    <lookup> can accept as input:
    1- a single icd9 code as string
    2- a pd.Series of icd9 codes
    
    and outputs a mapping to the corresponding icd9 group.
    
    
    Examples
    --------
    
    >>> codes = pd.Series([5849,E8497,2720])
    
    >>> grouper = ICDCodesGrouper(ccs_path=<ccs_path>,
                                  icd9_chapter_path=<icd9_chapter_path>,
                                  cci_path=<cci_path>
                                  )
    >>> grouper.check_avaliable_groupers()
    ['ccs', 'icd9chapters','icd9_level3','cci']
    
    >>> grouper.lookup('ccs',codes)
    0     157
    1    2621
    2      53
    dtype: int64
    
    >>> grouper.lookup('icd9chapters',codes)
    0    10
    1    19
    2     3
    dtype: int64
    """
    
    def __init__(self, ccs_path, icd9_chapter_path, cci_path):
        """
        Parameters
        ----------
        settings : Class
            Class with filepaths accessible though: settings.ccs_path, settings.icd9_chapter_path, etc..
            contains auxiliary data paths of grouping methods
        """
        
        self.ccs = self.CCSSingleDiagnosis(ccs_path)
        self.icd9chapters = self.ICD9_CM_Chapters(icd9_chapter_path)
        self.icd9_level3 = self.ICD9_LEVEL3()
        self.cci = self.CCI(cci_path)
        
        self.groupers = {'ccs':self.ccs,
                         'icd9chapters':self.icd9chapters,
                         'icd9_level3':self.icd9_level3,
                         'cci':self.cci}
    
    def get_available_groupers(self):
        return [i for i in self.groupers]
    
    def lookup(self,grouper: str,code):
        """
        
        Parameters
        ----------
        grouper : str
            grouper must exist in self.check_avaliable_groupers
        code : str | pd.Series
            icd9 code or pd.Series of codes
        """
        if grouper not in self.groupers:
            raise ValueError(f'Expecting one of the following \
                            groupers: {self.check_avaliable_groupers()},\
                            got instead {grouper}')
        
        return self.groupers[grouper].lookup(code)
    
    class ICD9_LEVEL3:
        """
        maps icd9 codes to the first 3 levels
        """
        
        def __init(self):
            pass
        
        def lookup(self,code):
            if type(code) == pd.Series:
                code_level3 = code.astype(str).apply(lambda code:code[:3])
                assert code_level3.apply(len).unique()[0] == 3,f'Oops. Got {code_level3.apply(len).unique()}'
            else:
                code_level3 = str(code)[:3]
                assert len(code_level3) == 3,f'Oops. Got {code_level3}'
            return code_level3
                
    
    class CCSSingleDiagnosis:
        """
        Maps icd9 codes to CCS groups
        """
        def __init__(self,file = None):

            if file is None:
                file = 'CCS-SingleDiagnosisGrouper.txt'
            file = open(file,"r")
            content = file.read()
            file.close()
            lookup = {}
            groups = re.findall('(\d+\s+[A-Z].*(\n.+)+)',content)
            for group in groups:
                parsed = group[0].split()
                for code in parsed[2:]:
                    lookup[code] = int(parsed[0])
            self._lookup_table = lookup

        def lookup(self,code):
            """
            Given an icd9 code, returns the corresponding ccs code.
            
            Parameters
            ----------
            
            code : str | pd.Series
                icd9 code
            
            Returns:
              np.nan: code doesn't match
              >0: corresponding ccs code
            """
            
            def lookup_single(code : str):
                try:
                    return self._lookup_table[code]
                except:
                    return np.nan
            
            if type(code) == pd.Series:
                return code.apply(lookup_single)
            elif type(code) == 'str':
                return lookup_single(code)
            else:
                raise ValueError(f'Wrong input type. Expecting str or pd.Series. Got {type(code)}')
                
    class CCI:
        def __init__(self,cci_path):
            self.cci_path = cci_path

            self.data = self._read_and_process()
            self._lookup_table = self.data.set_index('ICD-9-CM CODE')['CHRONIC'].to_dict()


        def lookup(self,code):
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
                def lookup_single(code : str):
                    try:
                        return self._lookup_table[code]
                    except:
                        return np.nan
                if type(code) == pd.Series:
                    return code.apply(lookup_single)
                elif type(code) == 'str':
                    return lookup_single(code)
                else:
                    raise ValueError(f'Wrong input type. Expecting str or pd.Series. Got {type(code)}')


        def _read_and_process(self):
            df = pd.read_csv('grouper_data/cci2015.csv',usecols=[0,2])
            df.columns = [col.replace("'","") for col in df.columns]
            df['ICD-9-CM CODE'] = df['ICD-9-CM CODE'].str.replace("'","").str.strip()
            df['CATEGORY DESCRIPTION'] = df['CATEGORY DESCRIPTION'].str.replace("'","").str.strip()
            df = df.rename(columns={'CATEGORY DESCRIPTION':'CHRONIC'})
            df['CHRONIC'] = df['CHRONIC'].map({'0':False,'1':True})

            return df
        
    class ICD9_CM_Chapters:
        """
        Maps icd9 codes to icd9 chapters
        """
        def __init__(self,filepath):
            # creates self.chapters_num & self.chapters_char & self.bins
            self.__preprocess_chapters(filepath)

        def lookup(self,code):
            """
            
            
            Parameters
            ----------
            
            code : str | pd.Series

            Returns
            -------
            
            chapter : str | pd.Series
                Corresponding icd9 chapter
            """

            def single_lookup(code_):

                def char_lookup(code_):
                    """
                    When the code starts by a char, it's either E or V
                    """
                    if code_[0] == 'E':
                        return 19
                    elif code_[0] == 'V':
                        return 18
                    return 0

                def int_lookup(code_: str):
                    level_3_code = int(code_[:3])
                    pos = np.digitize(level_3_code,self.bins)
                    chapter = self.chapters_num.Chapter.iloc[pos-1]
                    return chapter

                if code_[0] in ['E','V']:
                    return char_lookup(code_)
                
                return int_lookup(code_)

            def batch_lookup(codes : pd.Series):
                
                # to sort everything at the end
                original_order = codes.index.copy()
                
                mask_is_alpha = codes.apply(lambda x: (x[0] == 'E') | (x[0] == 'V') if not pd.isna(x) else False)
                codes_char = (codes
                              .loc[mask_is_alpha]
                              .copy()
                              .apply(lambda x:x[0]) # only need first character to identify chapter
                             )
                
                codes_nan = codes[pd.isna(codes)]
                codes_num = (codes
                             .loc[~codes.index.isin(codes_char.index.tolist() + codes_nan.index.tolist())]
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
                         )
                return result
            
            if type(code) not in [str,pd.Series]:
                return -1

            if type(code) == str:
                return single_lookup(code)
            elif type(code) == pd.Series:
                return batch_lookup(code)
            else:
                raise ValueError(f'Expecting code to be either str or pd.Series. Got {type(code)}')

        def __preprocess_chapters(self,filepath):
            """
            Some preprocessing to optimize assignment speed later using np.digitize
            1. Separate chapters into numeric codes or alpha codes (There are two chapters considered alpha because they start with "E" or "V")
            2. Create self.bins, which contains starting code ranges of each chapter
            """
            
            self.chapters = pd.read_csv(filepath)

            # preprocess chapters dataframe: split into alpha vs numeric
            self.chapters['start_range'] = self.chapters['Code Range'].apply(lambda x: x[:x.find('-')])

            chapters_char = (self.chapters
                           .loc[self.chapters.start_range
                                .apply(lambda x: len(re.findall('^(E|V)',x)) > 0),
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
