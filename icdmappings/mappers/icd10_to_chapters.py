from __future__ import annotations

from collections.abc import Iterable
from typing import Union

import importlib_resources
import json

from icdmappings import data_files

from .mapper_interface import MapperInterface
from .utils.icd10_lookup_utils import (
    ICD10LookupTable,
    build_lookup_from_range_descriptions,
    map_by_range_lookup,
)


class ICD10toChapters(MapperInterface):
    """Map ICD-10 CM diagnostic codes to ICD-10 chapters."""

    def __init__(self) -> None:
        """Initialize the chapter mapper and load lookup data."""
        self.filename = "icd10cmchapters.json"
        self._setup()

    def _setup(self) -> None:
        """Build in-memory chapter lookup data."""
        self.chapter_lookup = self._parse_file(self.filename)

    def _map_single(self, icd10code: str) -> str | None:
        """Map one ICD-10 CM code to its ICD-10 chapter bucket.

        Args:
            icd10code: ICD-10 CM diagnostic code.
        """
        return map_by_range_lookup(icd10code, self.chapter_lookup)

    def map(self, icd10code: Union[str, Iterable]) -> Union[str, Iterable]:
        """Map one or many ICD-10 CM codes to ICD-10 chapter buckets.

        Args:
            icd10code: ICD-10 CM code or iterable of ICD-10 CM codes.
        """
        if isinstance(icd10code, str):
            return self._map_single(icd10code)
        if isinstance(icd10code, Iterable):
            return [self._map_single(code) for code in icd10code]

        return None

    def _parse_file(self, filename: str) -> ICD10LookupTable:
        """Parse ICD-10 chapter lookup data into a compact range table.

        Args:
            filename: JSON filename containing ICD-10 chapter ranges.
        """
        with importlib_resources.files(data_files).joinpath(filename).open() as jsonfile:
            raw_lookup = json.load(jsonfile)

        return build_lookup_from_range_descriptions(raw_lookup=raw_lookup)
