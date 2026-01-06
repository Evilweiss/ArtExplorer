from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fact import Fact


async def get_facts_for_painting(session: AsyncSession, painting_id) -> list[Fact]:
    stmt = select(Fact).where(Fact.painting_id == painting_id).order_by(Fact.order_index)
    result = await session.execute(stmt)
    return list(result.scalars().all())
