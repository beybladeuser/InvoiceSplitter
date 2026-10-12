CREATE TABLE expense_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL CHECK (btrim(name) <> ''),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL CHECK (btrim(name) <> ''),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE group_members (
    group_id UUID NOT NULL REFERENCES expense_groups(id) ON DELETE CASCADE,
    member_id UUID NOT NULL REFERENCES members(id),
    joined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (group_id, member_id)
);

CREATE INDEX group_members_member_idx ON group_members (member_id); --usefull for finding all groups a member belongs to
CREATE INDEX group_members_group_idx ON group_members (group_id); --useful for finding all members in a group

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID NOT NULL REFERENCES expense_groups(id) ON DELETE CASCADE,
    paid_by_member_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (group_id, id),
    FOREIGN KEY (group_id, paid_by_member_id)
        REFERENCES group_members (group_id, member_id)
);

CREATE INDEX transactions_group_created_idx
    ON transactions (group_id, created_at DESC);

CREATE TABLE transaction_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID NOT NULL,
    transaction_id UUID NOT NULL,
    name TEXT NOT NULL CHECK (btrim(name) <> ''),
    amount_cents BIGINT NOT NULL CHECK (amount_cents >= 0),
    UNIQUE (group_id, id),
    FOREIGN KEY (group_id, transaction_id)
        REFERENCES transactions (group_id, id) ON DELETE CASCADE
);

CREATE INDEX transaction_items_transaction_idx
    ON transaction_items (group_id, transaction_id);

CREATE TABLE item_participants (
    group_id UUID NOT NULL,
    transaction_item_id UUID NOT NULL,
    member_id UUID NOT NULL,
    PRIMARY KEY (group_id, transaction_item_id, member_id),
    FOREIGN KEY (group_id, transaction_item_id)
        REFERENCES transaction_items (group_id, id) ON DELETE CASCADE,
    FOREIGN KEY (group_id, member_id)
        REFERENCES group_members (group_id, member_id)
);

CREATE INDEX item_participants_member_idx
    ON item_participants (group_id, member_id);

