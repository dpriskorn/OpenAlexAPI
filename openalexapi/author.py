from typing import Optional, List

from openalexapi.dehydrated_author import DehydratedAuthor
from openalexapi.ids import AuthorIds
from openalexapi.institution import Institution
from openalexapi.concept import Concept
from openalexapi.year import Year


class Author(DehydratedAuthor):
    display_name_alternatives: Optional[List[str]]
    works_count: Optional[int]
    cited_by_count: Optional[int]
    ids: Optional[AuthorIds]
    last_known_institutions: Optional[Institution]
    x_concepts: Optional[List[Concept]]
    counts_by_year: Optional[List[Year]]
    works_api_url: Optional[str]
    updated_date: Optional[str]
    created_date: Optional[str]


    class Config:
        arbitrary_types_allowed = True

    @property
    def orcid_url(self):
        return self.orcid

    @property
    def orcid_id(self):
        if self.orcid is not None:
            return self.orcid.replace("https://orcid.org/", "")
        else:
            return None
