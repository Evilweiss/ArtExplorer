from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.painting import Painting


async def get_painting_by_slugs(session: AsyncSession, artist_slug: str, painting_slug: str) -> Painting | None:
    stmt = (
        select(Painting)
        .where(Painting.artist_slug == artist_slug, Painting.painting_slug == painting_slug)
        .options(selectinload(Painting.facts))
    )
    result = await session.execute(stmt)
    return result.scalars().first()
