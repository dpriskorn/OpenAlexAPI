"""
Copyright 2022 Dennis Priskorn
"""
from typing import Optional, List

from openalexapi.basetype import OpenAlexBaseType
from openalexapi.year import Year
from openalexapi.enums import VersionType
from openalexapi.concept import DehydratedConcept




class Venue(OpenAlexBaseType):
    issn_l: Optional[str]  # What is this?
    issn: Optional[List[str]]
    display_name: Optional[str]
    publisher: Optional[str]
    type: Optional[str]
    url: Optional[str]
    is_oa: Optional[bool]
    version: Optional[str]
    license: Optional[str]
    works_count: Optional[int]
    cited_by_count: Optional[int]
    counts_by_year: Optional[List[Year]]
    works_api_url: Optional[str]
    updated_date: Optional[str]
    created_date: Optional[str]
    is_in_doaj: Optional[bool]
    x_concepts: Optional[List[DehydratedConcept]] 


class DehydratedVenue(OpenAlexBaseType):
    issn_l: Optional[str]
    issn: Optional[str]
    display_name: Optional[str]
    publisher: Optional[str]
    
class HostVenue(DehydratedVenue):
    url: Optional[str]
    is_oa: Optional[bool]
    version: Optional[VersionType]
    license: Optional[str]
    