"""
Copyright 2022 Dennis Priskorn
"""
from pydantic import BaseModel, conint
from typing import Optional


class Year(BaseModel):
    year: conint(le=2023, ge=0)
    cited_by_count: int
    works_count: Optional[int]
