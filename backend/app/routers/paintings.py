from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.schemas.fact import FactResponse
from app.schemas.painting import PaintingResponse
from app.services.facts import get_facts_for_painting
from app.services.paintings import get_painting_by_slugs

router = APIRouter(prefix="/api/v1/paintings", tags=["paintings"])
CANONICAL_PAINTING_SLUGS = {
    ("van-gogh", "the-starry-night"): ("van-gogh", "starry-night"),
}
COMBINED_SLUG_ALIASES = {
    "van-gogh-starry-night": ("van-gogh", "starry-night"),
    "van-gogh-the-starry-night": ("van-gogh", "starry-night"),
}


@router.get("/{artist_slug}/{painting_slug}", response_model=PaintingResponse)
async def read_painting(artist_slug: str, painting_slug: str, session: AsyncSession = Depends(get_session)):
    canonical_slugs = CANONICAL_PAINTING_SLUGS.get((artist_slug, painting_slug))
    if canonical_slugs:
        canonical_artist, canonical_painting = canonical_slugs
        return RedirectResponse(
            url=f"/api/v1/paintings/{canonical_artist}/{canonical_painting}",
            status_code=301,
        )

    painting = await get_painting_by_slugs(session, artist_slug, painting_slug)
    if not painting:
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
async def redirect_combined_slug(artist_and_painting_slug: str):
    canonical_slugs = COMBINED_SLUG_ALIASES.get(artist_and_painting_slug)
    if canonical_slugs:
        canonical_artist, canonical_painting = canonical_slugs
        return RedirectResponse(
            url=f"/api/v1/paintings/{canonical_artist}/{canonical_painting}",
            status_code=301,
        )
    raise HTTPException(status_code=404, detail="Painting not found")


@router.get("/by-id/{painting_id}/facts", response_model=list[FactResponse])
async def read_facts(painting_id: str, session: AsyncSession = Depends(get_session)):
    facts = await get_facts_for_painting(session, painting_id)
    return [FactResponse.model_validate(fact) for fact in facts]
