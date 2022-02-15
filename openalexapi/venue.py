from typing import Optional, List

from openalexapi.basetype import OpenAlexBaseType


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
