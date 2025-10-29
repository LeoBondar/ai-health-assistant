from uuid import UUID

from sqlalchemy import select

from app.api.chats.schemas import (
    DiseaseData,
    ExerciseData,
    GetPlanInfoResponse,
    PlaceData,
    RiskFactorData,
    UserGoalData,
)
from app.api.errors.api_error import PlanNotFoundApiError
from app.persistent.db_schemas.chat import (
    disease_table,
    exercise_table,
    place_table,
    plan_table,
    risk_factor_table,
    user_goal_table,
)
from app.repositories.uow import UnitOfWork


class GetPlanInfoView:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def __call__(self, plan_id: UUID) -> GetPlanInfoResponse:
        async with self._uow.begin():
            plan_stmt = (
                select(
                    plan_table.c.id,
                    plan_table.c.description,
                    risk_factor_table.c.id.label("risk_factor_id"),
                    risk_factor_table.c.factor.label("risk_factor_name"),
                    disease_table.c.id.label("disease_id"),
                    disease_table.c.name.label("disease_name"),
                    user_goal_table.c.id.label("user_goal_id"),
                    user_goal_table.c.name.label("user_goal_name"),
                    place_table.c.id.label("place_id"),
                    place_table.c.name.label("place_name"),
                    exercise_table.c.id.label("exercise_id"),
                    exercise_table.c.name.label("exercise_name"),
                    exercise_table.c.description.label("exercise_description"),
                    plan_table.c.exercise_type.label("plan_exercise_type"),
                )
                .select_from(
                    plan_table.outerjoin(risk_factor_table, plan_table.c.risk_factor_id == risk_factor_table.c.id)
                    .outerjoin(disease_table, plan_table.c.disease_id == disease_table.c.id)
                    .outerjoin(user_goal_table, plan_table.c.user_goal_id == user_goal_table.c.id)
                    .outerjoin(place_table, plan_table.c.place_id == place_table.c.id)
                    .outerjoin(exercise_table, plan_table.c.exercise_id == exercise_table.c.id)
                )
                .where(plan_table.c.id == plan_id)
            )

            plan_result = (await self._uow.session.execute(plan_stmt)).first()

            if not plan_result:
                raise PlanNotFoundApiError

            risk_factor = None
            if plan_result.risk_factor_id:
                risk_factor = RiskFactorData(id=plan_result.risk_factor_id, factor=plan_result.risk_factor_name)

            disease = None
            if plan_result.disease_id:
                disease = DiseaseData(id=plan_result.disease_id, name=plan_result.disease_name)

            user_goal = None
            if plan_result.user_goal_id:
                user_goal = UserGoalData(id=plan_result.user_goal_id, name=plan_result.user_goal_name)

            place = None
            if plan_result.place_id:
                place = PlaceData(id=plan_result.place_id, name=plan_result.place_name)

            exercise = None
            if plan_result.exercise_id:
                exercise = ExerciseData(
                    id=plan_result.exercise_id, name=plan_result.exercise_name, type=plan_result.plan_exercise_type, description=plan_result.exercise_description
                )

            return GetPlanInfoResponse(
                id=plan_result.id,
                description=plan_result.description,
                risk_factor=risk_factor,
                disease=disease,
                user_goal=user_goal,
                place=place,
                exercise=exercise,
                exercise_type=plan_result.plan_exercise_type,
            )
