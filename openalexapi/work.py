from typing import Optional, List, Dict

from purl import URL
from pydantic import BaseModel, conint, constr

from openalexapi.venue import Venue


class Ids:
    doi: Optional[URL]
    pmid: Optional[str]
    mag: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class OpenAccess:
    is_oa: bool
    oa_status: str
    oa_url: URL

    class Config:
        arbitrary_types_allowed = True


class OpenAlexAuthorId:
    pass


class Author:
    id: Optional[URL]
    display_name: Optional[str]
    orcid: Optional[URL]

    class Config:
        arbitrary_types_allowed = True


class Institution:
    id: Optional[URL]
    display_name: Optional[str]
    ror: Optional[URL]
    country_code: Optional[constr(max_length=2, min_length=2)]
    type: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class Authorship:
    author_position: str
    author: Optional[Author]
    institutions: Optional[List[Institution]]
    raw_affiliation_string: Optional[str]


class Concept:
    id: Optional[URL]
    wikidata: Optional[URL]
    display_name: Optional[str]
    level: Optional[int]
    score: Optional[float]

    class Config:
        arbitrary_types_allowed = True


class Mesh:
    pass


class Year:
    year: conint(le=2023, ge=0)
    cited_by_count: int


class Biblio:
    volume: str
    issue: str
    first_page: str
    last_page: str


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
    referenced_works: Optional[List[URL]]
    related_works: Optional[List[URL]]
    abstract_inverted_index: Optional[Dict[str, List[int]]]
    counts_by_year: Optional[List[Year]]
    cited_by_api_url: Optional[URL]
    biblio: Optional[Biblio]

    class Config:
        arbitrary_types_allowed = True
