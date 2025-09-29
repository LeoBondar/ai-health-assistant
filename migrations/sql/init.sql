CREATE SCHEMA IF NOT EXISTS chats;


CREATE TABLE IF NOT EXISTS chats.chat
(
    id             UUID PRIMARY KEY,
    user_id        VARCHAR(255) NOT NULL,
    name           VARCHAR(255) NOT NULL,
    use_context    BOOLEAN NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS chat_user_id_idx ON chats.chat USING HASH (user_id);
CREATE INDEX IF NOT EXISTS chat_risk_factor_id_idx ON chats.chat USING HASH (risk_factor_id);
CREATE INDEX IF NOT EXISTS chat_disease_id_idx ON chats.chat USING HASH (disease_id);
CREATE INDEX IF NOT EXISTS chat_user_goal_id_idx ON chats.chat USING HASH (user_goal_id);


CREATE TABLE IF NOT EXISTS chats.plan
(
    id         UUID PRIMARY KEY,
    chat_id    UUID REFERENCES chats.chat (id) NOT NULL,
    risk_factor_id UUID REFERENCES chats.risk_factor (id),
    disease_id     UUID REFERENCES chats.disease (id),
    user_goal_id   UUID REFERENCES chats.user_goal (id),
    place_id       UUID REFERENCES chats.place (id),
    exercise_id    UUID REFERENCES chats.exercise (id),
    description    TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


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


CREATE TABLE IF NOT EXISTS chats.risk_factor
(
    id         UUID PRIMARY KEY,
    factor     VARCHAR(255)                 NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS chats.disease
(
    id         UUID PRIMARY KEY,
    name       VARCHAR(255)                 NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS chats.user_goal
(
    id         UUID PRIMARY KEY,
    name       VARCHAR(255)                 NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS chats.place
(
    id         UUID PRIMARY KEY,
    name       VARCHAR(255)                 NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS chats.exercise
(
    id         UUID PRIMARY KEY,
    name       VARCHAR(255)                 NOT NULL,
    type       VARCHAR(255)                 NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

