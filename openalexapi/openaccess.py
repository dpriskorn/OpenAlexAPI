from typing import Optional

from purl import URL
from pydantic import BaseModel


class OpenAccess(BaseModel):
    is_oa: bool
    oa_status: Optional[str]
    oa_url: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def oa_url(self):
        return URL(self.oa_url)