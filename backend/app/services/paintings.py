from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.painting import Painting
from app.models.painting_alias import PaintingAlias


async def get_painting_by_slugs(session: AsyncSession, artist_slug: str, painting_slug: str) -> Painting | None:
    stmt = (
        select(Painting)
        .where(Painting.artist_slug == artist_slug, Painting.painting_slug == painting_slug)
        .options(selectinload(Painting.facts))
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_painting_by_alias_pair(session: AsyncSession, artist_slug: str, painting_slug: str) -> Painting | None:
    stmt = (
        select(Painting)
        .join(PaintingAlias, PaintingAlias.painting_id == Painting.id)
        .where(PaintingAlias.artist_slug == artist_slug, PaintingAlias.painting_slug == painting_slug)
        .options(selectinload(Painting.facts))
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_painting_by_combined_alias(session: AsyncSession, combined_slug: str) -> Painting | None:
    stmt = (
        select(Painting)
        .join(PaintingAlias, PaintingAlias.painting_id == Painting.id)
        .where(PaintingAlias.combined_slug == combined_slug)
        .options(selectinload(Painting.facts))
    )
    result = await session.execute(stmt)
    return result.scalars().first()
