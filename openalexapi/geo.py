"""
Copyright 2022 Dennis Priskorn
"""
from typing import Optional

from pydantic import BaseModel, constr


class Geo(BaseModel):
    city: str
    geonames_city_id: str
    region: str
    country_code: Optional[constr(max_length=2, min_length=2)]
    country: str
    latitude: float
    longitude: float
    #TODO: international currenlty undocumented
    