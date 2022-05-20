import logging
from typing import Optional, List

import backoff  # type: ignore
import requests
from pydantic import BaseModel, EmailStr

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

    # TODO: Adapt this to support multiple namespaces
    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_multiple_works(self, ids: List[str]) -> List[Work]:
        """Fetches multiple works by OpenAlex IDs. Note this does not support
        alternative namespaces.

        :parameter ids is a list of OpenAlex ID strings
        """
        if len(ids) == 0:
            raise ValueError("ids cannot be empty")
        if self.email is None:
            print("OpenAlex has 2 pools for clients. "
                  "Please be nice and supply your email as the first argument "
                  "when calling this class to get into the polite pool. This way "
                  "OpenAlex can contact you if needed.")
        headers = {
            "Accept": "application/json",
            "User-Agent": f"OpenAlexAPI https://github.com/dpriskorn/OpenAlexAPI mailto:{self.email}"
        }
        ids = [s.replace("https://openalex.org/", "") for s in ids]
        works = []
        # Limit of 50 is imposed by OpenAlex API
        for i in range(0, len(ids), 50):
            url_ids = '|'.join(ids[i:i+50])
            url = self.base_url + f"works?filter=openalex_id:{url_ids}&per_page=50"
            logger.debug(f"Fetching works {i} through {i+50}")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                works += [Work(**w) for w in response.json()['results']]
            elif response.status_code == 403:
                raise ValueError("Got error 403. Are you using OpenAlex IDs?")
            else:
                raise ValueError(f"Got {response.status_code} from OpenAlex")
        return works

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_related_works(self, work: Work) -> List[Work]:
        """Fetches works related to the given work.

        :parameter work is OpenAlex Work
        """
        return self.get_multiple_works(work.related_works)

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_referenced_works(self, work: Work) -> List[Work]:
        """Fetches all works referenced by the given work.

        :parameter work is OpenAlex Work
        """
        return self.get_multiple_works(work.referenced_works)

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_cited_by_works(self, work: Work, limit: int = None) -> List[Work]:
        """Fetches all works that cite the given work, up to some limit.

        :parameter work is OpenAlex Work
        :parameter limit is the maximum number of works to return
        """
        if self.email is None:
            print("OpenAlex has 2 pools for clients. "
                  "Please be nice and supply your email as the first argument "
                  "when calling this class to get into the polite pool. This way "
                  "OpenAlex can contact you if needed.")
        headers = {
            "Accept": "application/json",
            "User-Agent": f"OpenAlexAPI https://github.com/dpriskorn/OpenAlexAPI mailto:{self.email}"
        }
        per_page = 200 if limit is None else min(200, limit)
        works = []
        cursor = '*'
        while cursor:
            url = f"{work.cited_by_api_url}&per_page={per_page}&cursor={cursor}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                works += [Work(**w) for w in response.json()['results']]
                cursor = response.json()['meta']['next_cursor']
            else:
                raise ValueError(f"Got {response.status_code} from OpenAlex")
            if limit and len(works) >= limit:
                break
        return works[:limit]
