from typing import Optional

from purl import URL
from pydantic import BaseModel


class Author(BaseModel):
    id: Optional[str]
    display_name: Optional[str]
    orcid: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def id(self):
        return URL(self.id)

    @property
    def orcid_url(self):
        return URL(self.orcid)

    @property
    def orcid_id(self):
        return self.orcid.replace("https://doi.org/")