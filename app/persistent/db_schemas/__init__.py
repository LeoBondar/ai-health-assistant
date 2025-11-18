from sqlalchemy.orm import relationship

from app.domain.chat import Chat, Disease, Exercise, Message, Place, Plan, RiskFactor, UserGoal
from app.persistent.db_schemas.base import mapper_registry
from app.persistent.db_schemas.chat import (
    chat_table,
    disease_table,
    exercise_table,
    message_table,
    place_table,
    plan_table,
    risk_factor_table,
    user_goal_table,
)


def init_mappers() -> None:
    mapper_registry.map_imperatively(
        Chat,
        chat_table,
        properties={
            "messages": relationship(
                "Message",
                back_populates="chat",
                cascade="all, delete-orphan",
            ),
            "plan": relationship("Plan", uselist=False, backref="chat"),
        },
    )

    mapper_registry.map_imperatively(
        Message,
        message_table,
        properties={
            "chat": relationship(
                "Chat",
                back_populates="messages",
            ),
        },
    )

    mapper_registry.map_imperatively(
        RiskFactor,
        risk_factor_table,
    )

    mapper_registry.map_imperatively(
        Disease,
        disease_table,
    )

    mapper_registry.map_imperatively(
        UserGoal,
        user_goal_table,
    )

    mapper_registry.map_imperatively(
        Place,
        place_table,
    )

    mapper_registry.map_imperatively(
        Exercise,
        exercise_table,
    )

    mapper_registry.map_imperatively(
        Plan,
        plan_table,
        properties={
            "risk_factor": relationship(
                "RiskFactor", foreign_keys=[plan_table.c.risk_factor_id], uselist=False, lazy="selectin"
            ),
            "disease": relationship("Disease", foreign_keys=[plan_table.c.disease_id], uselist=False, lazy="selectin"),
            "user_goal": relationship(
                "UserGoal", foreign_keys=[plan_table.c.user_goal_id], uselist=False, lazy="selectin"
            ),
            "place": relationship("Place", foreign_keys=[plan_table.c.place_id], uselist=False, lazy="selectin"),
            "exercise": relationship(
                "Exercise", foreign_keys=[plan_table.c.exercise_id], uselist=False, lazy="selectin"
            ),
        },
    )
