from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, Table, Text, text

from app.persistent.db_schemas.base import CHATS_SCHEMA, mapper_registry

chat_table = Table(
    "chat",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", String(255), nullable=False),
    Column("plan_id", UUID(as_uuid=True), ForeignKey(f"{CHATS_SCHEMA}.plan.id"), nullable=True),
    Column("name", String(255), nullable=False),
    Column("use_context", Boolean, nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=CHATS_SCHEMA,
)

message_table = Table(
    "message",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "chat_id",
        UUID(as_uuid=True),
        ForeignKey(f"{CHATS_SCHEMA}.chat.id"),
        nullable=False,
    ),
    Column("text", Text, nullable=False),
    Column("type", String(50), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=CHATS_SCHEMA,
)

risk_factor_table = Table(
    "risk_factor",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("factor", String(255), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=CHATS_SCHEMA,
)

disease_table = Table(
    "disease",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(255), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=CHATS_SCHEMA,
)

user_goal_table = Table(
    "user_goal",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(255), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=CHATS_SCHEMA,
)

place_table = Table(
    "place",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(255), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=CHATS_SCHEMA,
)

exercise_table = Table(
    "exercise",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("type", String(255), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=CHATS_SCHEMA,
)

plan_table = Table(
    "plan",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "risk_factor_id",
        UUID(as_uuid=True),
        ForeignKey(f"{CHATS_SCHEMA}.risk_factor.id"),
        nullable=True,
    ),
    Column(
        "disease_id",
        UUID(as_uuid=True),
        ForeignKey(f"{CHATS_SCHEMA}.disease.id"),
        nullable=True,
    ),
    Column(
        "user_goal_id",
        UUID(as_uuid=True),
        ForeignKey(f"{CHATS_SCHEMA}.user_goal.id"),
        nullable=True,
    ),
    Column(
        "place_id",
        UUID(as_uuid=True),
        ForeignKey(f"{CHATS_SCHEMA}.place.id"),
        nullable=True,
    ),
    Column(
        "exercise_id",
        UUID(as_uuid=True),
        ForeignKey(f"{CHATS_SCHEMA}.exercise.id"),
        nullable=True,
    ),
    Column("description", Text, nullable=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
    schema=CHATS_SCHEMA,
)
