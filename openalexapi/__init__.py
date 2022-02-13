from typing import Optional

import requests
from pydantic import BaseModel

from openalexapi.work import Work


class OpenAlex(BaseModel):
    """This models the OpenAlex HTTP API
    OpenAlex has 2 pools for clients.
    Supplying your email will get you into the polite pool.
    :parameter=email
    """
    email: Optional[str]
    base_url = "https://api.openalex.org/"

    def get_single_work(self, id) -> Optional[Work]:
        """This models the single work entity endpoint

        :parameter id can be and OpenAlex ID e.g. "W123" or a namespace ID like "doi:10.123"
        see https://docs.openalex.org/api/get-single-entities#namespace-id-format"""
        if self.email is None:
            print("OpenAlex has 2 pools for clients. "
                  "Please be nice and supply your email as the first argument "
                  "when calling this class to get into the polite pool. This way "
                  "OpenAlex can contact you if needed.")
        url = self.base_url + "works/" + id
        headers = {
            "Accept": "application/json",
            "User-Agent": f"OpenAlexAPI https://github.com/dpriskorn/OpenAlexAPI mailto:{self.email}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return Work(**response.json())
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Got {response.status_code} from OpenAlex")
