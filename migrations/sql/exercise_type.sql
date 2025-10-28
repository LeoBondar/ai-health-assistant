ALTER TABLE IF EXISTS chats.plan
ADD exercise_type VARCHAR(255) NULL;

ALTER TABLE IF EXISTS chats.exercise
DROP COLUMN type;
