"""
Copyright 2022 Dennis Priskorn
"""
import logging
from typing import Optional, List

import backoff  # type: ignore
import requests
from pydantic import BaseModel, EmailStr

from openalexapi.basetype import OpenAlexBaseType
from openalexapi.work import Work
from openalexapi.author import Author
from openalexapi.work import Concept
from openalexapi.venue import Venue
from openalexapi.institution import Institution

PAGE_LIMIT = 50 # Limit of 200 is imposed by OpenAlex API





logger = logging.getLogger(__name__)


class OpenAlex(BaseModel):
    """This models the OpenAlex HTTP API
    OpenAlex has 2 pools for clients.
    Supplying your email will get you into the polite pool.
    :parameter=email
    """
    email: Optional[EmailStr]
    base_url = "https://api.openalex.org/"
    
    def set_email(self,email: Optional[EmailStr]):
        self.email = email

    @backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError),
                      max_time=60,
                      on_backoff=print(f"Backing off"))
    def __get_single_entity(self, id: str, oatype: OpenAlexBaseType):
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
        url = self.base_url + oatype.__name__.lower() + 's/' + id
        logger.debug(f"Fetching {url}")
        headers = {
            "Accept": "application/json",
            "User-Agent": f"OpenAlexAPI https://github.com/dpriskorn/OpenAlexAPI mailto:{self.email}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return oatype(**response.json())
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Got {response.status_code} from OpenAlex")
    
    @backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError),
                      max_time=60,
                      on_backoff=print(f"Backing off"))
    def get_single_work(self, id: str) -> Optional[Work]:
        return self.__get_single_entity(id, Work)
    
    @backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError),
                      max_time=60,
                      on_backoff=print(f"Backing off"))
    def get_single_author(self, id: str) -> Optional[Author]:
        return self.__get_single_entity(id, Author)
    
    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_single_concept(self, id: str) -> Optional[Concept]:
        return self.__get_single_entity(id, Concept)

    @backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError),
                      max_time=60,
                      on_backoff=print(f"Backing off"))    
    def get_single_venue(self, id: str) -> Optional[Venue]:
        return self.__get_single_entity(id, Venue)
    
    @backoff.on_exception(backoff.expo,
                  (requests.exceptions.Timeout,
                   requests.exceptions.ConnectionError),
                  max_time=60,
                  on_backoff=print(f"Backing off"))    
    def get_single_institution(self, id: str) -> Optional[Institution]:
        return self.__get_single_entity(id, Venue)
        
    
    # TODO: Adapt this to support multiple namespaces
    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def __get_multiple_entities(self, ids: List[str], oatype: OpenAlexBaseType) -> List[Work]:
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
        entities = []
        for i in range(0, len(ids), PAGE_LIMIT):
            url_ids = '|'.join(ids[i:i+PAGE_LIMIT])
            url = self.base_url + f"{oatype.__name__.lower()}s?filter=openalex_id:{url_ids}&per_page={PAGE_LIMIT}"
            logger.debug(f"Fetching {oatype.__name__.lower()}s {i} through {i+PAGE_LIMIT}")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                entities += [oatype(**e) for e in response.json()['results']]
            elif response.status_code == 403:
                raise ValueError("Got error 403. Are you using OpenAlex IDs?")
            else:
                raise ValueError(f"Got {response.status_code} from OpenAlex")
        return entities

    @backoff.on_exception(backoff.expo,
                  (requests.exceptions.Timeout,
                   requests.exceptions.ConnectionError),
                  max_time=60,
                  on_backoff=print(f"Backing off"))    
    def get_multiple_works(self, ids: List[str]) -> List[Work]:
        return self.__get_multiple_entities(ids, Work)

    @backoff.on_exception(backoff.expo,
                  (requests.exceptions.Timeout,
                   requests.exceptions.ConnectionError),
                  max_time=60,
                  on_backoff=print(f"Backing off"))    
    def get_multiple_authors(self, ids: List[str]) -> List[Author]:
        return self.__get_multiple_entities(ids, Author)

    @backoff.on_exception(backoff.expo,
                  (requests.exceptions.Timeout,
                   requests.exceptions.ConnectionError),
                  max_time=60,
                  on_backoff=print(f"Backing off"))    
    def get_multiple_concepts(self, ids: List[str]) -> List[Author]:
        return self.__get_multiple_entities(ids, Author)

    @backoff.on_exception(backoff.expo,
                  (requests.exceptions.Timeout,
                   requests.exceptions.ConnectionError),
                  max_time=60,
                  on_backoff=print(f"Backing off"))    
    def get_multiple_venues(self, ids: List[str]) -> List[Venue]:
        return self.__get_multiple_entities(ids, Venue)

    @backoff.on_exception(backoff.expo,
                  (requests.exceptions.Timeout,
                   requests.exceptions.ConnectionError),
                  max_time=60,
                  on_backoff=print(f"Backing off"))    
    def get_multiple_institutions(self, ids: List[str]) -> List[Institution]:
        return self.__get_multiple_entities(ids, Institution)

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
        per_page = PAGE_LIMIT if limit is None else min(PAGE_LIMIT, limit)
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
