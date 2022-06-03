"""
Copyright 2022 Dennis Priskorn
"""
import logging
from typing import Optional, List, Union

import backoff  # type: ignore
import requests
from pydantic import BaseModel, EmailStr

from openalexapi.basetype import OpenAlexBaseType
from openalexapi.work import Work
from openalexapi.author import Author, DehydratedAuthor
from openalexapi.work import Concept, DehydratedConcept
from openalexapi.venue import Venue, DehydratedVenue, HostVenue
from openalexapi.institution import Institution, DehydratedInstitution


logger = logging.getLogger(__name__)


class OpenAlex(BaseModel):
    """This models the OpenAlex HTTP API
    OpenAlex has 2 pools for clients.
    Supplying your email will get you into the polite pool.
    :parameter=email
    """
    email: Optional[EmailStr]
    page_limit: int = 50
    _base_url: str = "https://api.openalex.org/"
    _headers: dict = {
                "Accept": "application/json",
                "User-Agent": f"OpenAlexAPI https://github.com/dpriskorn/OpenAlexAPI"
            }
        #Convenience dict because dehydrated entities do not have works_api_urls and annoying inconsistencies in endpoints (institution vs instititions, host_venue vs venue)
    _works_urls: dict = {
            Author: _base_url+"works?filter=author.id:",
            DehydratedAuthor: _base_url+"works?filter=author.id:",
            Concept: _base_url+"works?filter=concept.id:",
            DehydratedConcept: _base_url+"works?filter=concept.id:",
            Institution: _base_url+"works?filter=institutions.id:",
            DehydratedInstitution: _base_url+"works?filter=institutions.id:",
            Venue: _base_url+"works?filter=host_venue.id:",
            DehydratedVenue: _base_url+"works?filter=host_venue.id:",
            Host: _base_url+"works?filter=host_venue.id:"
        }
    _entities_prefixes: dict = {
        'A':Author,
        'C':Concept,
        'I':Institution,
        'V':Venue,
        'W':Work
    }

    class Config:
        underscore_attrs_are_private = True
        
    def set_email(self,email: EmailStr):
        self.email = email
        self._headers = {
                "Accept": "application/json",
                "User-Agent": f"OpenAlexAPI https://github.com/dpriskorn/OpenAlexAPI mailto:{self.email}"
            }

    @backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError),
                      max_time=60,
                      on_backoff=print(f"Backing off"))
    def get_single_entity(self, id: str) -> Union[Author,Concept,Institution,Venue,Work]:
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
        id =id.replace("https://openalex.org/", "")
        if id[0] in self._entities_prefixes: etype = self._entities_prefixes[id[0]]
        else: raise ValueError("Id prefix does not correspond to a valid entity.")
        url = self._base_url + etype.__name__.lower() + 's/' + id
        logger.debug(f"Fetching {url}")
        response = requests.get(url, headers=self._headers)
        if response.status_code == 200:
            return etype(**response.json())
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
    def hydrate_entity(self, dehydrated_entity: Union[DehydratedAuthor, DehydratedConcept, DehydratedInstitution, DehydratedVenue, HostVenue])  -> Union[Author,Concept,Institution,Venue]:
        return self.get_single_entity(dehydrated_entity.id)
    
    # TODO: Adapt this to support multiple namespaces
    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_entities(self, ids: List[str]) -> Union[List[Author],List[Concept],List[Institution],List[Venue],List[Work]]:
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
        ids = [s.replace("https://openalex.org/", "") for s in ids]
        if ids[0][0] in self._entities_prefixes: etype = self._entities_prefixes[ids[0][0]]
        else: raise ValueError("Id prefix does not correspond to a valid entity.")
        entities = []
        for i in range(0, len(ids), self.page_limit):
            url_ids = '|'.join(ids[i:i+self.page_limit])
            url = self._base_url + f"{etype.__name__.lower()}s?filter=openalex_id:{url_ids}&per_page={self.page_limit}"
            logger.debug(f"Fetching {etype.__name__.lower()}s {i} through {i+self.page_limit}")
            response = requests.get(url, headers=self._headers)
            if response.status_code == 200:
                entities += [etype(**e) for e in response.json()['results']]
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
    def hydrate_entities(self, dehydrated_entities: Union[List[DehydratedAuthor],List[DehydratedConcept],List[DehydratedInstitution],List[DehydratedVenue],List[HostVenue]]) -> Union[List[Author],List[Concept],List[Institution],List[Venue]]:
        return self.get_entities([i.id for i in dehydrated_entities])
        

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_related_works(self, work: Work) -> List[Work]:
        """Fetches works related to the given work.

        :parameter work is OpenAlex Work
        """
        return self.get_entities(work.related_works)

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_referenced_works(self, work: Work) -> List[Work]:
        """Fetches all works referenced by the given work.

        :parameter work is OpenAlex Work
        """
        return self.get_entities(work.referenced_works)

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
        per_page = self.page_limit if limit is None else min(self.page_limit, limit)
        works = []
        cursor = '*'
        while cursor:
            url = f"{work.cited_by_api_url}&per_page={per_page}&cursor={cursor}"
            response = requests.get(url, headers=self._headers)
            if response.status_code == 200:
                works += [Work(**w) for w in response.json()['results']]
                cursor = response.json()['meta']['next_cursor']
            else:
                raise ValueError(f"Got {response.status_code} from OpenAlex")
            if limit and len(works) >= limit:
                break
        return works[:limit]

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.Timeout,
                           requests.exceptions.ConnectionError),
                          max_time=60,
                          on_backoff=print(f"Backing off"))
    def get_associated_works(self, entity: Union[Author, DehydratedAuthor, Institution, DehydratedInstitution, Concept, DehydratedConcept, Venue, DehydratedVenue], limit: int = None) -> List[Work]:
        """Fetches all works associated with the entity, up to some limit.

        :parameter work is OpenAlex Institution, Venue, Author
        :parameter limit is the maximum number of works to return
        """
        if self.email is None:
            print("OpenAlex has 2 pools for clients. "
                  "Please be nice and supply your email as the first argument "
                  "when calling this class to get into the polite pool. This way "
                  "OpenAlex can contact you if needed.")
        per_page = self.page_limit if limit is None else min(self.page_limit, limit)
        works = []
        cursor = '*'
        while cursor:
            url = f"{self._works_urls[type(entity)]}{entity.id}&per_page={per_page}&cursor={cursor}"
            response = requests.get(url, headers=self._headers)
            if response.status_code == 200:
                works += [Work(**w) for w in response.json()['results']]
                cursor = response.json()['meta']['next_cursor']
            else:
                raise ValueError(f"Got {response.status_code} from OpenAlex")
            if limit and len(works) >= limit:
                break
        return works[:limit]    

    @backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout,
                       requests.exceptions.ConnectionError),
                      max_time=60,
                      on_backoff=print(f"Backing off"))
    def search_entities(self, query: str, entity_type= Union["Author","Concept","Institution","Venue","Work"], limit: int = None) -> Union[List[Author],List[Concept],List[Institution],List[Venue],List[Work]]:
        """Fetches all works associated with the entity, up to some limit.

        :parameter work is OpenAlex Institution, Venue, Author
        :parameter limit is the maximum number of works to return
        """
        
        
        
        if self.email is None:
            print("OpenAlex has 2 pools for clients. "
                  "Please be nice and supply your email as the first argument "
                  "when calling this class to get into the polite pool. This way "
                  "OpenAlex can contact you if needed.")
        
        if entity_type[0] in self._entities_prefixes: etype = self._entities_prefixes[entity_type[0]]
        else: raise ValueError("Id prefix does not correspond to a valid entity.")
        
        per_page = self.page_limit if limit is None else min(self.page_limit, limit)
        entities = []
        cursor = '*'
        while cursor:
            url = f"{self._base_url}{etype.__name__.lower()}s?search=\"{query}\"&per_page={per_page}&cursor={cursor}"
            response = requests.get(url, headers=self._headers)
            if response.status_code == 200:
                entities += [etype(**e) for e in response.json()['results']]
                cursor = response.json()['meta']['next_cursor']
            else:
                raise ValueError(f"Got {response.status_code} from OpenAlex")
            if limit and len(entities) >= limit:
                break
        return entities[:limit]