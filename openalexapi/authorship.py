from typing import Optional, List

from pydantic import BaseModel

from openalexapi.author import DehydratedAuthor
from openalexapi.institution import Institution


class Authorship(BaseModel):
    author_position: str
    author: Optional[DehydratedAuthor]
    institutions: Optional[List[Institution]]
    raw_affiliation_string: Optional[str]
