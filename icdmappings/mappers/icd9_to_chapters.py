from typing import List
import os
from collections.abc import Iterable
from .mapper_interface import MapperInterface
import bisect
import csv

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
            self.bins, self.char_mapping = self._parse_file(filepath)

        
        def _map_single(self,icd9code : str):

            if not isinstance(icd9code,str):
                return None

            if icd9code[0] in ['E','V']:
                return self.char_mapping[icd9code[0]]
            else:
                try:
                    code3digits = int(icd9code[:3])
                    bin = self._get_bin(code3digits,self.bins)
                    if bin is not None:
                        return str(bin)
                    return None
                except:
                    return None


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
            if isinstance(icd9code,str):
                return self._map_single(icd9code)
            elif isinstance(icd9code, Iterable):
                return [self._map_single(code) for code in icd9code]
            raise TypeError(f'Wrong input type. Expecting str or Iterable. Got {type(icd9code)}')
                    

        def _get_bin(self, number : int | Iterable, bins : List):
            if isinstance(number,int):
                return bisect.bisect(bins, number)
            elif isinstance(number,Iterable):
                return [bisect.bisect(bins, num) if isinstance(num,int) else None for num in number]
            return None
            

        def _parse_file(self,filepath : str):
            """
            Some preprocessing to optimize assignment speed later using np.digitize
            1. Separate chapters into numeric codes or alpha codes (There are two chapters considered alpha because they start with "E" or "V")
            2. Create self.bins, which contains starting code ranges of each chapter
            """

            with open(filepath) as csvfile:
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