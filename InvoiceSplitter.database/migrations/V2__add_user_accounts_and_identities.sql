CREATE TABLE app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE user_identities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    issuer TEXT NOT NULL CHECK (btrim(issuer) <> ''),
    subject TEXT NOT NULL CHECK (btrim(subject) <> ''),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT user_identities_issuer_subject_key UNIQUE (issuer, subject)
);

CREATE INDEX user_identities_user_id_idx ON user_identities (user_id);

ALTER TABLE members
    ADD COLUMN user_id UUID REFERENCES app_users(id) ON DELETE SET NULL;

CREATE UNIQUE INDEX members_user_id_unique_idx
    ON members (user_id)
    WHERE user_id IS NOT NULL;