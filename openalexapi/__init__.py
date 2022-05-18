import logging
from typing import Optional, TypeVar, Type

import backoff  # type: ignore
import requests
from pydantic import BaseModel

from openalexapi.author import Author
from openalexapi.work import Work

logger = logging.getLogger(__name__)

T = TypeVar('T', Author, Work)

class OpenAlex(BaseModel):
    """This models the OpenAlex HTTP API
    OpenAlex has 2 pools for clients.
    Supplying your email will get you into the polite pool.
    :parameter=email
    """
    email: Optional[str]
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
        return self.get_single_entity(id, Work, "works/")

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_single_author(self, id: str) -> Optional[Author]:
        """This models the single author entity endpoint

        :parameter id can be an OpenAlex ID e.g. "A123" or a namespace ID
        see https://docs.openalex.org/api/get-single-entities#namespace-id-format"""
        return self.get_single_entity(id, Author, "authors/")

    def get_single_entity(self, id: str, entity: Type[T], endpoint: str) -> Optional[T]:
        """This models the single entity endpoint

        :parameter id can be an OpenAlex ID e.g. "A123" or a namespace ID
        :parameter entity is the class type
        :parameter endpoint is the endpoint e.g. "works/"""""
        if id is None:
            raise ValueError("id was None")
        if self.email is None:
            print("OpenAlex has 2 pools for clients. "
                  "Please be nice and supply your email as the first argument "
                  "when calling this class to get into the polite pool. This way "
                  "OpenAlex can contact you if needed.")
        url = self.base_url + endpoint + id
        logger.debug(f"Fetching {url}")
        headers = {
            "Accept": "application/json",
            "User-Agent": f"OpenAlexAPI https://github.com/dpriskorn/OpenAlexAPI mailto:{self.email}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return entity(**response.json())
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Got {response.status_code} from OpenAlex")
