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
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/2048px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg?20121101035929=&download=",
            source_url="https://commons.wikimedia.org/wiki/File:The_Starry_Night.jpg",
            license_name="Public domain",
            license_url="https://creativecommons.org/publicdomain/zero/1.0/",
        )
        facts = [
            Fact(
                painting_id=painting_id,
                name="Вихрь над холмами",
                description_md="Извилистая линия мазков подчеркивает ветреную, живую ночь.",
                geometry_type="rect",
                x=0.18,
                y=0.05,
                w=0.44,
                h=0.22,
                order_index=1,
            ),
            Fact(
                painting_id=painting_id,
                name="Огненная крона кипариса",
                description_md="Темный силуэт дерева тянется вверх и акцентирует вертикаль композиции.",
                geometry_type="rect",
                x=0.02,
                y=0.16,
                w=0.22,
                h=0.7,
                order_index=2,
            ),
            Fact(
                painting_id=painting_id,
                name="Сияние луны и ореол",
                description_md="Теплый круг света контрастирует с холодными синими оттенками ночи.",
                geometry_type="rect",
                x=0.7,
                y=0.08,
                w=0.12,
                h=0.14,
                order_index=3,
            ),
            Fact(
                painting_id=painting_id,
                name="Дымоходы и крыши",
                description_md="Светлые прямоугольники домов создают спокойный ритм внизу.",
                geometry_type="rect",
                x=0.26,
                y=0.62,
                w=0.34,
                h=0.2,
                order_index=4,
            ),
            Fact(
                painting_id=painting_id,
                name="Колокольня церкви",
                description_md="Острая вершина собора выделяется на фоне неба, добавляя вертикальный акцент.",
                geometry_type="rect",
                x=0.42,
                y=0.56,
                w=0.06,
                h=0.18,
                order_index=5,
            ),
            Fact(
                painting_id=painting_id,
                name="Холмы на горизонте",
                description_md="Мягкие волны рельефа уравновешивают вихри неба и закрывают перспективу.",
                geometry_type="rect",
                x=0.22,
                y=0.46,
                w=0.54,
                h=0.12,
                order_index=6,
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
