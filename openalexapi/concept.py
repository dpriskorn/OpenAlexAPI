from typing import Optional

from basetype import OpenAlexBaseType


class Concept(OpenAlexBaseType):
    wikidata: Optional[str]
    display_name: Optional[str]
    level: Optional[int]
    score: Optional[float]

    class Config:
        arbitrary_types_allowed = True

    @property
    def wikidata_id(self):
        return self.wikidata.replace("https://www.wikidata.org/wiki/", "")

    @property
    def wikidata_wiki_url(self):
        return self.wikidata
