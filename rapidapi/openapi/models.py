from typing import List, Optional

from pydantic import BaseModel


class Operation(BaseModel):
    tags: Optional[List[str]] = None
    summary: Optional[str] = None
    description: Optional[str] = None


class PathItem(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
