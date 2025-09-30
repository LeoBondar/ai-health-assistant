from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chat import RiskFactor
from app.repositories.exception import RepositoryNotFoundException


class IRiskFactorRepository(Protocol):
    async def get(self, risk_factor_id: UUID, with_lock: bool = False) -> RiskFactor:
        pass

    async def get_all_risk_factors(self, chat_id: UUID, with_lock: bool = True) -> Sequence[RiskFactor]:
        pass

    async def save(self, risk_factor: RiskFactor) -> None:
        pass


class RiskFactorRepository(IRiskFactorRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, risk_factor_id: UUID, with_lock: bool = True) -> RiskFactor:
        stmt = select(RiskFactor).filter_by(id=risk_factor_id)
        if with_lock:
            stmt = stmt.with_for_update()
        risk_factor = (await self.session.execute(stmt)).scalar()
        if not risk_factor:
            raise RepositoryNotFoundException
        return risk_factor

    async def get_all_risk_factors(self, chat_id: UUID, with_lock: bool = True) -> Sequence[RiskFactor]:
        stmt = select(RiskFactor).filter_by(chat_id=chat_id)
        if with_lock:
            stmt = stmt.with_for_update()
        risk_factors = (await self.session.execute(stmt)).scalars().all()
        return risk_factors

    async def save(self, risk_factor: RiskFactor) -> None:
        self.session.add(risk_factor)
