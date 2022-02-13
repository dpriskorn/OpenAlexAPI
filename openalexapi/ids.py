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
        if self.doi is not None:
            return self.doi.replace("https://doi.org/", "")
        else:
            return None

    @property
    def doi_url(self):
        if self.doi is not None:
            return URL(self.doi)
        else:
            return None

    @property
    def pmid_id(self):
        if self.pmid is not None:
            return self.pmid.replace("https://pubmed.ncbi.nlm.nih.gov/", "")
        else:
            return None

    @property
    def pmid_url(self):
        if self.pmid is not None:
            return URL(self.pmid)
        else:
            return None
