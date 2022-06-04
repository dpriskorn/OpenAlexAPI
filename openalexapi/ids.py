"""
Copyright 2022 Dennis Priskorn
"""
from typing import Optional, List

from pydantic import BaseModel


class Ids(BaseModel):
    doi: Optional[str]
    pmid: Optional[str]
    mag: Optional[str]
    twitter: Optional[str]
    wikipedia: Optional[str]
    scopus: Optional[str]
    ror: Optional[str]
    grid: Optional[str]
    wikidata: Optional[str]
    umls_aui: Optional[List[str]]
    umls_cui: Optional[List[str]]
    issn_l: Optional[str]
    issn: Optional[str]
    orcid: Optional[str]
    
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

