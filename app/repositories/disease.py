from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chat import Disease
from app.repositories.exception import RepositoryNotFoundException


class IDiseaseRepository(Protocol):
    async def get(self, disease_id: UUID, with_lock: bool = False) -> Disease:
        pass

    async def get_all_diseases(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Disease]:
        pass

    async def save(self, disease: Disease) -> None:
        pass


class DiseaseRepository(IDiseaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, disease_id: UUID, with_lock: bool = True) -> Disease:
        stmt = select(Disease).filter_by(id=disease_id)
        if with_lock:
            stmt = stmt.with_for_update()
        disease = (await self.session.execute(stmt)).scalar()
        if not disease:
            raise RepositoryNotFoundException
        return disease

    async def get_all_diseases(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Disease]:
        stmt = select(Disease).filter_by(chat_id=chat_id)
        if with_lock:
            stmt = stmt.with_for_update()
        diseases = (await self.session.execute(stmt)).scalars().all()
        return diseases

    async def save(self, disease: Disease) -> None:
        self.session.add(disease)
