import asyncio
import uuid

from sqlalchemy import delete

from app.db.database import AsyncSessionLocal
from app.models.fact import Fact
from app.models.painting import Painting
from app.models.painting_alias import PaintingAlias


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(delete(PaintingAlias))
        await session.execute(delete(Fact))
        await session.execute(delete(Painting))

        painting_id = uuid.uuid4()
        painting = Painting(
            id=painting_id,
            name="The Starry Night",
            artist_name="Vincent van Gogh",
            artist_slug="van-gogh",
            painting_slug="starry-night",
            museum_name="Museum of Modern Art",
            genre_name=["Post-Impressionism", "Modern art"],
            image_url="https://upload.wikimedia.org/wikipedia/commons/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
            source_url="https://commons.wikimedia.org/wiki/File:The_Starry_Night.jpg",
            license_name="Public domain",
            license_url="https://creativecommons.org/publicdomain/zero/1.0/",
        )
        facts = [
            Fact(
                painting_id=painting_id,
                name="Сворачивающееся небо",
                description_md="Крупные завитки в небе усиливают ощущение движения и глубины.",
                geometry_type="rect",
                x=0.12,
                y=0.08,
                w=0.38,
                h=0.32,
                order_index=1,
            ),
            Fact(
                painting_id=painting_id,
                name="Кипарис на переднем плане",
                description_md="Темный кипарис соединяет землю и небо и создает драматический контраст.",
                geometry_type="rect",
                x=0.05,
                y=0.18,
                w=0.18,
                h=0.62,
                order_index=2,
            ),
            Fact(
                painting_id=painting_id,
                name="Лунный диск",
                description_md="Яркая луна освещает деревню и создает ощущение ночного света.",
                geometry_type="rect",
                x=0.68,
                y=0.12,
                w=0.1,
                h=0.1,
                order_index=3,
            ),
            Fact(
                painting_id=painting_id,
                name="Деревня внизу",
                description_md="Небольшие дома и церковь делают сцену более человечной и спокойной.",
                geometry_type="rect",
                x=0.32,
                y=0.6,
                w=0.35,
                h=0.25,
                order_index=4,
            ),
        ]
        session.add(painting)
        session.add_all(facts)
        session.add_all(
            [
                PaintingAlias(
                    painting_id=painting_id,
                    artist_slug="vincent-van-gogh",
                    painting_slug="starry-night",
                ),
                PaintingAlias(
                    painting_id=painting_id,
                    combined_slug="van-gogh-starry-night",
                ),
            ]
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
