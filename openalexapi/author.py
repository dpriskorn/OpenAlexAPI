from typing import Optional

from basetype import OpenAlexBaseType


class Author(OpenAlexBaseType):
    display_name: Optional[str]
    orcid: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def orcid_url(self):
        return self.orcid

    @property
    def orcid_id(self):
        return self.orcid.replace("https://orcid.org/", "")
