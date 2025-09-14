from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, Table, Text, text

from app.persistent.db_schemas.base import CHATS_SCHEMA, mapper_registry

chat_table = Table(
    "chat",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", String(255), nullable=False),
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
