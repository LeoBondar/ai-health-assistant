from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chat import Place
from app.repositories.exception import RepositoryNotFoundException


class IPlaceRepository(Protocol):
    async def get(self, place_id: UUID, with_lock: bool = False) -> Place:
        pass

    async def get_all_places(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Place]:
        pass

    async def save(self, place: Place) -> None:
        pass


class PlaceRepository(IPlaceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, place_id: UUID, with_lock: bool = True) -> Place:
        stmt = select(Place).filter_by(id=place_id)
        if with_lock:
            stmt = stmt.with_for_update()
        place = (await self.session.execute(stmt)).scalar()
        if not place:
            raise RepositoryNotFoundException
        return place

    async def get_all_places(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Place]:
        stmt = select(Place).filter_by(chat_id=chat_id)
        if with_lock:
            stmt = stmt.with_for_update()
        places = (await self.session.execute(stmt)).scalars().all()
        return places

    async def save(self, place: Place) -> None:
        self.session.add(place)
