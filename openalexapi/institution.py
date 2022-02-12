from typing import Optional

from purl import URL
from pydantic import BaseModel, constr


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