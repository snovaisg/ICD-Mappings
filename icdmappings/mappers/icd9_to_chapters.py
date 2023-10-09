from typing import List,Union
import os
from collections.abc import Iterable
from .mapper_interface import MapperInterface
import bisect
import csv
import importlib.resources
from icdmappings import data_files

class ICD9toChapters(MapperInterface):
        """
        Maps icd9 diagnostic codes to icd9 chapters.
        
        source of mapping: https://icd.codes/icd9cm
        """
        def __init__(self):
            self.filename = "icd9-CM-code-chapter-en=PT.csv"
            self._setup()

        def _setup(self):
            self.bins, self.char_mapping = self._parse_file(self.filename)
        
        def _map_single(self, icd9code : str) -> str:
            """
            Maps a single ICD9 code in string format to its corresponding chapter.

            Parameters
            ----------
            icd9code : str
                ICD9 code to be mapped.

            Returns
            -------
            chapter : str
                Corresponding icd9 chapter or None if mapping is unsuccessful.
            """

            if not icd9code: # empty string or None
                return None

            if not isinstance(icd9code, str): # has to be string
                return None
            
            if icd9code[0] in ['E','V']:
                return self.char_mapping[icd9code[0]]
            else: # numerical code
                try:
                    code3digits = int(icd9code[:3])
                    bin = self._get_bin(code3digits,self.bins)
                    if bin is not None:
                        return str(bin)
                    return None
                except:
                    return None


        def map(self, icd9code : Union[str, Iterable]) -> Union[str, Iterable]:
            """
            Maps an ICD9 code or an Iterable of ICD9 codes to their corresponding chapters.

            Parameters
            ----------
            code : str | Iterable

            Returns
            -------
            chapter : str | Iterable
                Corresponding icd9 chapter(s) or None when mapping is unsuccessful.
            """
            if isinstance(icd9code,str):
                return self._map_single(icd9code)
            
            elif isinstance(icd9code, Iterable):
                return [self._map_single(code) for code in icd9code]

        def _get_bin(self, number : Union[int, Iterable], bins : List):
            if isinstance(number,int):
                return bisect.bisect(bins, number)
            elif isinstance(number,Iterable):
                return [bisect.bisect(bins, num) if isinstance(num,int) else None for num in number]
            return None
            

        def _parse_file(self, filename : str):
            """
            Preprocessing of bins to optimize assignment speed during mapping.
            1. Separate chapters into numeric codes or alpha codes (There are two chapters considered alpha because they start with "E" or "V")
            2. Create self.bins, which contains starting code ranges of each chapter
            """

            with importlib.resources.open_text(data_files, filename) as csvfile:
                reader = csv.reader(csvfile, quotechar="'")
                headers = next(reader)

                bins = list()

                for row in reader:
                    code_range = row[1]

                    if code_range[0] in ['E','V']:
                        continue

                    start,end = code_range.split('-')

                    bins.append(int(start))
                bins.append(int(end)+1)
            
            char_mapping = {'E':'19','V':'18'}
            return bins, char_mapping