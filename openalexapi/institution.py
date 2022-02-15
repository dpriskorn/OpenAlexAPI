from typing import Optional

from pydantic import BaseModel, constr

from basetype import OpenAlexBaseType


class Institution(OpenAlexBaseType):
    id: Optional[str]
    display_name: Optional[str]
    ror: Optional[str]
    country_code: Optional[constr(max_length=2, min_length=2)]
    type: Optional[str]
