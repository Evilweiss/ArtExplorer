from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FactResponse(BaseModel):
    id: UUID
    painting_id: UUID
    name: str
    description_md: str
    geometry_type: str
    x: float
    y: float
    w: float
    h: float
    order_index: int

    model_config = ConfigDict(from_attributes=True)
