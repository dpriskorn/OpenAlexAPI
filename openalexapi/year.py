from pydantic import BaseModel, conint


class Year(BaseModel):
    year: conint(le=2023, ge=0)
    cited_by_count: int
