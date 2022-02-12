from typing import Optional, List, Dict

from purl import URL
from pydantic import BaseModel, conint, constr

from openalexapi.venue import Venue

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


class OpenAccess(BaseModel):
    is_oa: bool
    oa_status: str
    oa_url: str

    class Config:
        arbitrary_types_allowed = True

    @property
    def oa_url(self):
        return URL(self.oa_url)


class OpenAlexAuthorId(BaseModel):
    pass


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


class Institution(BaseModel):
    id: Optional[str]
    display_name: Optional[str]
    ror: Optional[str]
    country_code: Optional[constr(max_length=2, min_length=2)]
    type: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def id(self):
        return URL(self.id)

    @property
    def ror(self):
        return URL(self.ror)


class Authorship(BaseModel):
    author_position: str
    author: Optional[Author]
    institutions: Optional[List[Institution]]
    raw_affiliation_string: Optional[str]


class Concept(BaseModel):
    id: Optional[str]
    wikidata: Optional[str]
    display_name: Optional[str]
    level: Optional[int]
    score: Optional[float]

    class Config:
        arbitrary_types_allowed = True

    @property
    def id(self):
        return URL(self.id)

    @property
    def wikidata_id(self):
        return self.wikidata.replace("https://www.wikidata.org/wiki/", "")

    @property
    def wikidata_wiki_url(self):
        return URL(self.wikidata)


class Mesh(BaseModel):
    pass


class Year(BaseModel):
    year: conint(le=2023, ge=0)
    cited_by_count: int


class Biblio(BaseModel):
    volume: Optional[str]
    issue: Optional[str]
    first_page: Optional[str]
    last_page: Optional[str]


class Work(BaseModel):
    ids: Ids
    display_name: Optional[str]
    title: Optional[str]
    publication_year: Optional[conint(le=2023, ge=0)]
    publication_date: Optional[str]
    type: Optional[str]
    host_venue: Optional[Venue]
    open_access: Optional[OpenAccess]
    authorships: Optional[List[Authorship]]
    cited_by_count: Optional[int]
    is_retracted: Optional[bool]
    is_paratext: Optional[bool]
    concepts: Optional[List[Concept]]
    mesh: Optional[List[Mesh]]
    alternate_host_venues: Optional[List[Venue]]
    referenced_works: Optional[List[str]]
    related_works: Optional[List[str]]
    abstract_inverted_index: Optional[Dict[str, List[int]]]
    counts_by_year: Optional[List[Year]]
    cited_by_api_url: Optional[str]
    biblio: Optional[Biblio]

    class Config:
        arbitrary_types_allowed = True

    @property
    def cited_by_api_url(self):
        return URL(self.cited_by_api_url)
