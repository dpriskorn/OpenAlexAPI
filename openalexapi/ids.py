from typing import Optional

from pydantic import BaseModel


class BaseIds(BaseModel):
    openalex: Optional[str]
    mag: Optional[int]  # Microsoft Academics Graph

    class Config:
        arbitrary_types_allowed = True

    @property
    def openalex_id(self):
        if self.openalex is not None:
            return self.openalex.replace("https://openalex.org/", "")
        else:
            return None

    @property
    def openalex_url(self):
        return self.openalex


class AuthorIds(BaseIds):
    orcid: Optional[str]
    twitter: Optional[str]
    wikipedia: Optional[str]
    scopus: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def orcid_id(self):
        if self.orcid is not None:
            return self.orcid.replace("https://orcid.org/", "")
        else:
            return None

    @property
    def orcid_url(self):
        return self.orcid


class WorkIds(BaseIds):
    doi: Optional[str]
    pmid: Optional[str]

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
