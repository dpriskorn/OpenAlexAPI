from typing import Optional, List

from purl import URL
from pydantic import BaseModel


class Venue(BaseModel):
    id: Optional[str]
    issn_l: Optional[str]
    issn: Optional[List[str]]
    display_name: Optional[str]
    publisher: Optional[str]
    type: Optional[str]
    url: Optional[str]
    is_oa: Optional[bool]
    version: Optional[str]
    license: Optional[str]

    @property
    def id(self):
        return URL(self.id)

    @property
    def url(self):
        return URL(self.url)
