from typing import Optional, List

from purl import URL
from pydantic import BaseModel


class Venue(BaseModel):
    id: Optional[URL]
    issn_l: Optional[str]
    issn: Optional[List[str]]
    display_name: Optional[str]
    publisher: Optional[str]
    type: Optional[str]
    url: Optional[URL]
    is_oa: Optional[bool]
    version: Optional[str]
    license: Optional[str]

    class Config:
        arbitrary_types_allowed = True
