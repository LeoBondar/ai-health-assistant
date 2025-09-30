from uuid import UUID

from sqlalchemy import select

from app.api.chats.schemas import GetRiskFactorsResponse, RiskFactorData
from app.persistent.db_schemas.chat import risk_factor_table
from app.repositories.uow import UnitOfWork


class GetFactorsView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, limit: int, offset: int) -> GetRiskFactorsResponse:
        async with self._uow.begin():
            stmt = select(risk_factor_table.c.id, risk_factor_table.c.factor).limit(limit).offset(offset)

            factors = (await self._uow.session.execute(stmt)).all()

            return GetRiskFactorsResponse(
                factors=[RiskFactorData(id=factor.id, factor=factor.factor) for factor in factors]
            )
