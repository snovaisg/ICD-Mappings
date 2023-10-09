from typing import List, Union
import os
from collections.abc import Iterable
import re
from .mapper_interface import MapperInterface
import importlib.resources
from icdmappings import data_files

class ICD9toCCS(MapperInterface):
        """
        Maps icd9 codes to CCS groups
        
        source of mapping: https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp
        """
        def __init__(self):
            self.filename = "CCS-SingleDiagnosisGrouper.txt"
            self._setup()


        def _setup(self):
            # {ccs:[icd9,...],..., ccs:[icd9,...]}
            self.ccs_to_icd9 = self._parse_file(self.filename)

            # (inverse mapping): {icd9:ccs,..., icd9:ccs}
            self.icd9_to_ccs = self.ccs_to_icd9 = {self.ccs_to_icd9[ccs][i]:ccs for ccs in self.ccs_to_icd9 for i in range(len(self.ccs_to_icd9[ccs]))} 
        
        def _parse_file(self, filename : str):
            with importlib.resources.open_text(data_files, filename) as f:
                content = f.read()
            return self._get_codes(content)
        
        def _map_single(self, icd9code : str) -> str:
            return self.icd9_to_ccs.get(icd9code)

        def map(self,icd9code: Union[str, Iterable]) -> Union[str, Iterable]:
            """
            Given an icd9 code, returns the corresponding CCS code.
            If input is Iterable returns a list of codes. 
            
            Parameters
            ----------
            
            code : str | Iterable
                icd9 code
            
            Returns:
                ccs code or None when the mapping is not possible
            """
            
            if isinstance(icd9code, str):
                return self._map_single(icd9code)
            
            elif isinstance(icd9code, Iterable):
                return[self._map_single(code) for code in icd9code]
            
            return None

        def _get_codes(self, content : str):
            """
            Parses the file and returns a dictionary with the following structure:
            {ccs_code:[icd9_codes],...,ccs_code:[icd9_codes]}

            """

            groups = re.findall(r'(\d+\s+[A-Z].*(\n.+)+)',content)
            """
            Unfortunately we need this function because this regex isn't perfect

            Rules:
            # ccs code is always first element
            # always ignore empty strings
            # while in the first line, gotta wait for a \n inside a string
            # after the first \n we have icd9 codes.
            # some icd9 codes will have \n as they are the last code before a newline and the next ccs code
            # some strings may be just \n without any text attached



            Returns
            -------

            data : dict
                {ccs_code:[icd9_codes],...,ccs_code:[icd9_codes}
            """


            data = {}

            for group in groups:

                group = group[0]
                tokens = group.split(' ')
                ccs_code = None

                is_first_tok =True # first token is a ccs code
                is_first_line = True #ignore all tokens in the first line (except the first which is a ccs code)

                for tok in tokens:
                    if is_first_tok: # first token is always the ccs code
                        ccs_code = tok
                        data[ccs_code] = []

                        is_first_tok = False
                        continue

                    if tok == '': #ignore empty strings resulted from .split
                        continue

                    if '\n' in tok:

                        if tok == '\n':
                            if is_first_line: #We are not in the first line anymore
                                is_first_line=False
                            continue
                        else:
                            if is_first_line: #We are not in the first line anymore
                                is_first_line=False
                                continue 
                            else:
                                tok = tok.replace('\n','') # code with a \n attached. clean it

                    elif is_first_line: # Ignore everything in the first line
                        continue

                    # this token wasn't ignored in the previous steps. save it as a icd9 code
                    data[ccs_code].append(tok)
            return data