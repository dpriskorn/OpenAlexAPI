from typing import Optional

from purl import URL
from pydantic import BaseModel


class Concept(BaseModel):
    id: Optional[str]
    wikidata: Optional[str]
    display_name: Optional[str]
    level: Optional[int]
    score: Optional[float]

    class Config:
        arbitrary_types_allowed = True

    @property
    def id(self):
        return URL(self.id)

    @property
    def wikidata_id(self):
        return self.wikidata.replace("https://www.wikidata.org/wiki/", "")

    @property
    def wikidata_wiki_url(self):
        return URL(self.wikidata)