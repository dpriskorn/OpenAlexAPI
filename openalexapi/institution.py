"""
Copyright 2022 Dennis Priskorn
"""
from typing import Optional, List

from pydantic import constr

from openalexapi.basetype import OpenAlexBaseType
from openalexapi.ids import Ids
from openalexapi.year import Year
from openalexapi.geo import Geo
from openalexapi.enums import InstitutionType, InstitutionalRelationship
from openalexapi.concept import DehydratedConcept

class Institution(OpenAlexBaseType):
    id: Optional[str]
    display_name: Optional[str]
    display_name_alternatives: Optional[List[str]]
    ids: Optional[Ids]
    ror: Optional[str]
    country_code: Optional[constr(max_length=2, min_length=2)]
    type: Optional[InstitutionType]
    works_count: Optional[int]
    cited_by_count: Optional[int]
    counts_by_year: Optional[List[Year]]
    works_api_url: Optional[str]
    updated_date: Optional[str]
    created_date: Optional[str]
    homepage_url: Optional[str]
    image_url: Optional[str]
    image_thumbnail_url: Optional[str]
    display_name_acronyms: Optional[List[str]]
    relationship: Optional[InstitutionalRelationship]
    geo: Optional[Geo]
    x_concepts: Optional[List[DehydratedConcept]]
    
class DehydratedInstitution(OpenAlexBaseType):
    display_name: Optional[str]
    ror: Optional[str]
    country_code: Optional[constr(max_length=2, min_length=2)]
    type: Optional[InstitutionType]

