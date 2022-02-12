from typing import Optional

from purl import URL
from pydantic import BaseModel


class Ids(BaseModel):
    doi: Optional[str]
    pmid: Optional[str]
    mag: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def doi_id(self):
        return self.doi.replace("https://doi.org/", "")

    @property
    def doi_url(self):
        return URL(self.doi)

    @property
    def pmid_id(self):
        return self.pmid.replace("https://pubmed.ncbi.nlm.nih.gov/", "")

    @property
    def pmid_url(self):
        return URL(self.pmid)