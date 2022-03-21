from typing import Optional

from openalexapi.basetype import OpenAlexBaseType


class DehydratedAuthor(OpenAlexBaseType):
    display_name: Optional[str]
    orcid: Optional[str]
