from typing import Optional

from pydantic import BaseModel


class Biblio(BaseModel):
    volume: Optional[str]
    issue: Optional[str]
    first_page: Optional[str]
    last_page: Optional[str]