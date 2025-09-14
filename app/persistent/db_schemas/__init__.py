from sqlalchemy.orm import relationship

from app.domain.chat import Chat, Message
from app.persistent.db_schemas.base import mapper_registry

from .chat import chat_table, message_table


def init_mappers() -> None:
    message_mapper = mapper_registry.map_imperatively(Message, message_table)
    chat_mapper = mapper_registry.map_imperatively(
        Chat,
        chat_table,
        properties={
            "messages": relationship(
                message_mapper,
                foreign_keys=message_mapper.c.chat_id,
                lazy="selectin",
            ),
        },
    )
