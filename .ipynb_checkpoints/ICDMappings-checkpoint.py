# +
import pandas as pd
import numpy as np
import re

class ICDMappings(object):
    """
    This Class containing several icd mappings subclasses that allow conversion between icd9->10 and vice-versa, icd9->ccs, etc..
    
    all subclasses implement the method "lookup" which maps the corresponding code to the target coding.
    
    <lookup> can accept as input:
    1- a single code as a string
    2- a pd.Series of codes
    
    and outputs a mapping to the corresponding target coding.
    
    
    Examples
    --------
    
    >>> codes = pd.Series([5849,E8497,2720])
    
    >>> icdmapping = ICDMappings() # uses default filepaths of the mappings
    
    >>> icdmapping.check_avaliable_groupers()
    ['ccs', 'icd9chapters','icd9_level3','cci']
    
    >>> icdmapping.lookup('ccs',codes)
    0     157
    1    2621
    2      53
    dtype: int64
    
    >>> icdmapping.lookup('icd9chapters',codes)
    0    10
    1    19
    2     3
    dtype: int64
    """
    
    def __init__(self, 
                 icd9toccs_path=None, 
                 icd10to9_path=None, 
                 icd9to10_path=None, 
                 icd9tochapter_path=None, 
                 icd9tocci_path=None):
        """
        Parameters
        ----------
        settings : Class
            Class with filepaths accessible though: settings.ccs_path, settings.icd9_chapter_path, etc..
            contains auxiliary data paths of grouping methods
        """
        
        # default paths in case they aren't specified in init
        self.default_icd9toccs_path= 'icd_mappings/CCS-SingleDiagnosisGrouper.txt'
        self.default_icd9tochapter_path = 'icd_mappings/icd9-CM-code-chapter-en=PT.csv'
        self.default_icd9to10_path = 'icd_mappings/icd9toicd10cmgem.csv'
        self.default_icd10to9_path = 'icd_mappings/icd10cmtoicd9gem.csv'
        self.default_icd9tocci_path = 'icd_mappings/cci2015.csv'
        
        icd9toccs_path = self.default_icd9toccs_path if icd9toccs_path is None else icd9toccs_path
        icd9to10_path = self.default_icd9to10_path if icd9to10_path is None else icd9to10_path
        icd10to9_path = self.default_icd10to9_path if icd10to9_path is None else icd10to9_path
        icd9tochapter_path = self.default_icd9tochapter_path if icd9tochapter_path is None else icd9tochapter_path
        icd9tocci_path = self.default_icd9tocci_path if icd9tocci_path is None else icd9tocci_path
        
        # init converter classes
        self.icd9toccs = self.ICD9toCCS(icd9toccs_path)
        self.icd9to10 = self.ICD9to10(icd9to10_path)
        self.icd10to9 = self.ICD10to9(icd10to9_path)
        self.icd9tochapter = self.ICD9toChapters(icd9tochapter_path)
        self.icd9_level3 = self.ICD9_LEVEL3()
        self.icd9tocci = self.ICD9toCCI(icd9tocci_path)
        
        self.groupers = {'icd9toccs':self.icd9toccs,
                         'icd9to10':self.icd9to10,
                         'icd10to9':self.icd10to9,
                         'icd9tochapter':self.icd9tochapter,
                         'icd9_level3':self.icd9_level3,
                         'icd9tocci':self.icd9tocci}
    
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
                
    
    class ICD9toCCS:
        """
        Maps icd9 codes to CCS groups
        """
        def __init__(self,file):

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
                
    class ICD9toCCI:
        def __init__(self,icd9tocci_path):
            self.icd9tocci_path = icd9tocci_path

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
            df = pd.read_csv(self.icd9tocci_path,usecols=[0,2])
            df.columns = [col.replace("'","") for col in df.columns]
            df['ICD-9-CM CODE'] = df['ICD-9-CM CODE'].str.replace("'","").str.strip()
            df['CATEGORY DESCRIPTION'] = df['CATEGORY DESCRIPTION'].str.replace("'","").str.strip()
            df = df.rename(columns={'CATEGORY DESCRIPTION':'CHRONIC'})
            df['CHRONIC'] = df['CHRONIC'].map({'0':False,'1':True})

            return df
        
    class ICD9toChapters:
        """
        Maps icd9 codes to icd9 chapters
        """
        def __init__(self,icd9toChapters_path):
            # creates self.chapters_num & self.chapters_char & self.bins
            self.__preprocess_chapters(icd9toChapters_path)

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
    
    class ICD10to9:
        """
        Mapping taken from: https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings
        """
        def __init__(self, icd10to9_path):
            self.icd10to9_path = icd10to9_path

            self.data = self._read_and_process()
            self._lookup_table = self.data.set_index('icd10cm')['icd9cm'].to_dict()

        def lookup(self,code):
                    """
                    Given an icd10 code, returns the corresponding icd9 code.

                    Parameters
                    ----------

                    code : str | pd.Series
                        icd10 code

                    Returns:
                        icd9 code or np.nan when the mapping is not possible
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
            df = pd.read_csv(self.icd10to9_path)

            df.loc[df.no_map == 1,'icd9cm'] = np.nan

            return df




    class ICD9to10:
        """
        Mapping taken from: https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings
        """
        def __init__(self, icd9to10_path):
            self.icd9to10_path = icd9to10_path

            self.data = self._read_and_process()
            self._lookup_table = self.data.set_index('icd9cm')['icd10cm'].to_dict()

        def lookup(self,code):
                    """
                    Given an icd9 code, returns the corresponding icd10 code.

                    Parameters
                    ----------

                    code : str | pd.Series
                        icd9 code

                    Returns:
                        icd10 code or np.nan when the mapping is not possible
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
            df = pd.read_csv(self.icd9to10_path)

            df.loc[df.no_map == 1,'icd10cm'] = np.nan

            return df