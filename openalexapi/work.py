from typing import Optional, List, Dict

from pydantic import conint

from basetype import OpenAlexBaseType
from openalexapi.authorship import Authorship
from openalexapi.biblio import Biblio
from openalexapi.concept import Concept
from openalexapi.enums import WorkType
from openalexapi.ids import Ids
from openalexapi.mesh import Mesh
from openalexapi.openaccess import OpenAccess
from openalexapi.venue import Venue
from openalexapi.year import Year


class Work(OpenAlexBaseType):
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
    referenced_works: Optional[List[str]]  # this is urls like https://openalex.org/W123
    related_works: Optional[List[str]]  # this is urls like https://openalex.org/W123
    abstract_inverted_index: Optional[Dict[str, List[int]]]
    counts_by_year: Optional[List[Year]]
    cited_by_api_url: Optional[str]
    biblio: Optional[Biblio]
