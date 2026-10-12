CREATE TABLE app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    oidc_issuer TEXT NOT NULL CHECK (btrim(oidc_issuer) <> ''),
    oidc_subject TEXT NOT NULL CHECK (btrim(oidc_subject) <> ''),
    CONSTRAINT app_users_oidc_identity_key UNIQUE (oidc_issuer, oidc_subject),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE members
    ADD COLUMN user_id UUID REFERENCES app_users(id) ON DELETE SET NULL;

CREATE UNIQUE INDEX members_user_id_unique_idx
    ON members (user_id)
    WHERE user_id IS NOT NULL;