from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.chat import Plan
from app.repositories.exception import RepositoryNotFoundException


class IPlanRepository(Protocol):
    async def get(self, plan_id: UUID, with_lock: bool = False) -> Plan:
        pass

    async def get_all_plans(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Plan]:
        pass

    async def save(self, plan: Plan) -> None:
        pass


class PlanRepository(IPlanRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, plan_id: UUID, with_lock: bool = True) -> Plan:
        stmt = select(Plan).filter_by(id=plan_id)
        if with_lock:
            stmt = stmt.with_for_update()
        plan = (await self.session.execute(stmt)).scalar()
        if not plan:
            raise RepositoryNotFoundException
        return plan

    async def get_all_plans(self, chat_id: UUID, with_lock: bool = True) -> Sequence[Plan]:
        stmt = select(Plan).filter_by(chat_id=chat_id)
        if with_lock:
            stmt = stmt.with_for_update()
        plans = (await self.session.execute(stmt)).scalars().all()
        return plans

    async def save(self, plan: Plan) -> None:
        self.session.add(plan)
