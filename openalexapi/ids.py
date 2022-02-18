from typing import Optional

from pydantic import BaseModel


class Ids(BaseModel):
    doi: Optional[str]  # DOI
    pmid: Optional[str]  # PubMed ID
    mag: Optional[str]  # Microsoft Academic Graph
    issn_l: Optional[str]  # What is this?

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
        return self.doi

    @property
    def pmid_id(self):
        if self.pmid is not None:
            return self.pmid.replace("https://pubmed.ncbi.nlm.nih.gov/", "")
        else:
            return None

    @property
    def pmid_url(self):
        return self.pmid
