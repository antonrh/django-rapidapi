from typing import List, Optional

from .models import Operation, PathItem


def path(summary: Optional[str] = None, description: Optional[str] = None):
    def annotation(endpoint):
        setattr(
            endpoint, "__openapi__", PathItem(summary=summary, description=description)
        )
        return endpoint

    return annotation


def operation(
    tags: Optional[List[str]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
):
    def annotation(operation):
        setattr(
            operation,
            "__openapi__",
            Operation(tags=tags, summary=summary, description=description),
        )
        return operation

    return annotation
