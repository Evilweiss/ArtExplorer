from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.schemas.fact import FactResponse
from app.schemas.painting import PaintingResponse
from app.services.facts import get_facts_for_painting
from app.services.paintings import (
    get_painting_by_alias_pair,
    get_painting_by_combined_alias,
    get_painting_by_slugs,
)

router = APIRouter(prefix="/api/v1/paintings", tags=["paintings"])


@router.get("/{artist_slug}/{painting_slug}", response_model=PaintingResponse)
async def read_painting(artist_slug: str, painting_slug: str, session: AsyncSession = Depends(get_session)):
    painting = await get_painting_by_slugs(session, artist_slug, painting_slug)
    if not painting:
        alias_painting = await get_painting_by_alias_pair(session, artist_slug, painting_slug)
        if alias_painting:
            return RedirectResponse(
                url=f"/api/v1/paintings/{alias_painting.artist_slug}/{alias_painting.painting_slug}",
                status_code=301,
            )
        raise HTTPException(status_code=404, detail="Painting not found")
    return PaintingResponse(
        id=painting.id,
        name=painting.name,
        artist_name=painting.artist_name,
        artist_slug=painting.artist_slug,
        painting_slug=painting.painting_slug,
        museum_name=painting.museum_name,
        genre_name=painting.genre_name,
        image_url=painting.image_url,
        source_url=painting.source_url,
        license_name=painting.license_name,
        license_url=painting.license_url,
        facts_count=len(painting.facts),
    )


@router.get("/{artist_and_painting_slug}", include_in_schema=False)
async def redirect_combined_slug(artist_and_painting_slug: str, session: AsyncSession = Depends(get_session)):
    alias_painting = await get_painting_by_combined_alias(session, artist_and_painting_slug)
    if alias_painting:
        return RedirectResponse(
            url=f"/api/v1/paintings/{alias_painting.artist_slug}/{alias_painting.painting_slug}",
            status_code=301,
        )
    raise HTTPException(status_code=404, detail="Painting not found")


@router.get("/by-id/{painting_id}/facts", response_model=list[FactResponse])
async def read_facts(painting_id: str, session: AsyncSession = Depends(get_session)):
    facts = await get_facts_for_painting(session, painting_id)
    return [FactResponse.model_validate(fact) for fact in facts]
