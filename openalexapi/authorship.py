from typing import Optional, List

from pydantic import BaseModel

from author import Author
from institution import Institution


class Authorship(BaseModel):
    author_position: str
    author: Optional[Author]
    institutions: Optional[List[Institution]]
    raw_affiliation_string: Optional[str]