"""
Copyright 2022 Dennis Priskorn
"""
from typing import Optional, List

from openalexapi.basetype import OpenAlexBaseType
from openalexapi.ids import Ids
from openalexapi.institution import DehydratedInstitution
from openalexapi.year import Year
from openalexapi.concept import DehydratedConcept

class Author(OpenAlexBaseType):
    display_name: Optional[str]
    orcid: Optional[str]
    display_name_alternatives: Optional[List[str]]
    works_count: Optional[int]
    cited_by_count: Optional[int]
    ids: Optional[Ids]
    last_known_institution: Optional[DehydratedInstitution]
    counts_by_year: Optional[List[Year]]
    works_api_url: Optional[str]
    updated_date: Optional[str]
    created_date: Optional[str]
    x_concepts: Optional[List[DehydratedConcept]]
    
    class Config:
        arbitrary_types_allowed = True

    @property
    def orcid_url(self):
        return self.orcid

    @property
    def orcid_id(self):
        return self.orcid.replace("https://orcid.org/", "")

class DehydratedAuthor(OpenAlexBaseType):
    display_name: Optional[str]
    orcid: Optional[str]
    
    @property
    def orcid_url(self):
        return self.orcid

    @property
    def orcid_id(self):
        return self.orcid.replace("https://orcid.org/", "")