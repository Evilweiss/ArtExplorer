from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaintingResponse(BaseModel):
    id: UUID
    name: str
    artist_name: str
    artist_slug: str
    painting_slug: str
    museum_name: str | None
    genre_name: list[str] | None
    image_url: str
    source_url: str
    license_name: str | None
    license_url: str | None
    facts_count: int

    model_config = ConfigDict(from_attributes=True)
