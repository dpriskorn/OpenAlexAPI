from enum import Enum
from typing import Optional, List, Dict

from purl import URL
from pydantic import BaseModel, conint

from openalexapi.authorship import Authorship
from openalexapi.biblio import Biblio
from openalexapi.concept import Concept
from openalexapi.ids import Ids
from openalexapi.mesh import Mesh
from openalexapi.openaccess import OpenAccess
from openalexapi.venue import Venue
from openalexapi.year import Year


class WorkType(Enum):
    BOOK = "book"
    JOURNAL_ARTICLE = "journal-article"


class Work(BaseModel):
    ids: Ids
    display_name: Optional[str]
    title: Optional[str]
    publication_year: Optional[conint(le=2023, ge=0)]
    publication_date: Optional[str]
    type: Optional[WorkType]
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

    @property
    def cited_by_api_url(self):
        return URL(self.cited_by_api_url)

    # TODO decide whether to output referenced works as URL or str
