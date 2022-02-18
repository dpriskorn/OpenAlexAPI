import logging
from typing import Optional

import backoff  # type: ignore
import requests
from pydantic import BaseModel

from openalexapi.work import Work

logger = logging.getLogger(__name__)


class OpenAlex(BaseModel):
    """This models the OpenAlex HTTP API
    OpenAlex has 2 pools for clients.
    Supplying your email will get you into the polite pool.
    :parameter=email
    """
    email: Optional[EmailStr]
    base_url = "https://api.openalex.org/"

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_single_work(self, id: str) -> Optional[Work]:
        """This models the single work entity endpoint

        :parameter id can be and OpenAlex ID e.g. "W123" or a namespace ID like "doi:10.123"
        see https://docs.openalex.org/api/get-single-entities#namespace-id-format"""
        if id is None:
            raise ValueError("id was None")
        if self.email is None:
            print("OpenAlex has 2 pools for clients. "
                  "Please be nice and supply your email as the first argument "
                  "when calling this class to get into the polite pool. This way "
                  "OpenAlex can contact you if needed.")
        url = self.base_url + "works/" + id
        logger.debug(f"Fetching {url}")
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
