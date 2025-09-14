CREATE SCHEMA IF NOT EXISTS chats;


CREATE TABLE IF NOT EXISTS chats.chat
(
    id         UUID PRIMARY KEY,
    user_id    VARCHAR(255) NOT NULL,
    name       VARCHAR(255) NOT NULL,
    use_context BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS chat_user_id_idx ON chats.chat USING HASH (user_id);


CREATE TABLE IF NOT EXISTS chats.message
(
    id         UUID PRIMARY KEY,
    chat_id    UUID REFERENCES chats.chat (id) NOT NULL,
    text       TEXT                            NOT NULL,
    type       VARCHAR(255)                    NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS message_chat_id_idx ON chats.message USING HASH (chat_id);
