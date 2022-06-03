"""
Copyright 2022 Dennis Priskorn
"""
from typing import Optional, List

from openalexapi.basetype import OpenAlexBaseType
from openalexapi.ids import Ids
from openalexapi.year import Year


class DehydratedConcept(OpenAlexBaseType):
    wikidata: Optional[str]
    display_name: Optional[str]
    level: Optional[int]    

class Concept(OpenAlexBaseType):
    wikidata: Optional[str]
    display_name: Optional[str]
    level: Optional[int]
    score: Optional[float]
    description: Optional[str]
    works_count: Optional[int]
    cited_by_count: Optional[int]
    ids: Optional[Ids]
    image_url: Optional[str]
    image_thumbnail_url:Optional[str]
    score: Optional[float] #used for ancestors and related concepts
    #TODO: international
    ancestors: Optional[List[DehydratedConcept]]
    related_concepts: Optional[List[DehydratedConcept]]
    counts_by_year: Optional[List[Year]]
    works_api_url: Optional[str]
    updated_date: Optional[str]
    created_date: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def wikidata_id(self):
        return self.wikidata.replace("https://www.wikidata.org/wiki/", "")

    @property
    def wikidata_wiki_url(self):
        return self.wikidata
    
