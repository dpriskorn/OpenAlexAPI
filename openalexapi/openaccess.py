from purl import URL
from pydantic import BaseModel


class OpenAccess(BaseModel):
    is_oa: bool
    oa_status: str
    oa_url: str

    class Config:
        arbitrary_types_allowed = True

    @property
    def oa_url(self):
        return URL(self.oa_url)