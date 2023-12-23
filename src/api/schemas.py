from uuid import UUID

from pydantic import BaseModel

__all__ = ("IdSchema",)


class IdSchema(BaseModel):
    id: UUID
