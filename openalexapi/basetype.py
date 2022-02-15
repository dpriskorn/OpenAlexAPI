from typing import Optional

from pydantic import BaseModel


class OpenAlexBaseType(BaseModel):
    id: Optional[str]  # this is urls like https://openalex.org/W123

    def id_without_prefix(self):
        if self.id is not None:
            return self.id.replace("https://openalex.org/", "")
