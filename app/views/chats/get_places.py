from uuid import UUID

from sqlalchemy import select

from app.api.chats.schemas import GetPlacesResponse, PlaceData
from app.persistent.db_schemas.chat import place_table
from app.repositories.uow import UnitOfWork


class GetPlacesView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, limit: int, offset: int) -> GetPlacesResponse:
        async with self._uow.begin():
            stmt = select(place_table.c.id, place_table.c.name).limit(limit).offset(offset)

            places = (await self._uow.session.execute(stmt)).all()

            return GetPlacesResponse(places=[PlaceData(id=place.id, name=place.name) for place in places])
