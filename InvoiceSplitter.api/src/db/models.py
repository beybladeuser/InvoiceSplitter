from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Table,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

item_participants = Table(
    "item_participants",
    Base.metadata,
    Column("group_id", PostgreSQLUUID(as_uuid=True), primary_key=True),
    Column(
        "transaction_item_id", PostgreSQLUUID(as_uuid=True), primary_key=True
    ),
    Column("member_id", PostgreSQLUUID(as_uuid=True), primary_key=True),
    ForeignKeyConstraint(
        ["group_id", "transaction_item_id"],
        ["transaction_items.group_id", "transaction_items.id"],
        ondelete="CASCADE",
    ),
    ForeignKeyConstraint(
        ["group_id", "member_id"],
        ["group_members.group_id", "group_members.member_id"],
    ),
    Index("item_participants_member_idx", "group_id", "member_id"),
)


class AppUser(Base):
    __tablename__ = "app_users"
    __table_args__ = (
        CheckConstraint("btrim(oidc_issuer) <> ''"),
        CheckConstraint("btrim(oidc_subject) <> ''"),
        UniqueConstraint(
            "oidc_issuer",
            "oidc_subject",
            name="app_users_oidc_identity_key",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    oidc_issuer: Mapped[str] = mapped_column(Text, nullable=False)
    oidc_subject: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    member: Mapped[Member | None] = relationship(back_populates="user", uselist=False)


class ExpenseGroup(Base):
    __tablename__ = "expense_groups"
    __table_args__ = (CheckConstraint("btrim(name) <> ''"),)

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    memberships: Mapped[list[GroupMember]] = relationship(back_populates="group")
    transactions: Mapped[list[ExpenseTransaction]] = relationship(
        back_populates="group"
    )


class Member(Base):
    __tablename__ = "members"
    __table_args__ = (
        CheckConstraint("btrim(name) <> ''"),
        Index(
            "members_user_id_unique_idx",
            "user_id",
            unique=True,
            postgresql_where=text("user_id IS NOT NULL"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    user_id: Mapped[UUID | None] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("app_users.id", ondelete="SET NULL"),
    )

    user: Mapped[AppUser | None] = relationship(back_populates="member")
    memberships: Mapped[list[GroupMember]] = relationship(back_populates="member")


class GroupMember(Base):
    __tablename__ = "group_members"
    __table_args__ = (
        Index("group_members_member_idx", "member_id"),
        Index("group_members_group_idx", "group_id"),
    )

    group_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("expense_groups.id", ondelete="CASCADE"),
        primary_key=True,
    )
    member_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("members.id"),
        primary_key=True,
    )
    joined_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    group: Mapped[ExpenseGroup] = relationship(back_populates="memberships")
    member: Mapped[Member] = relationship(back_populates="memberships")


class ExpenseTransaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint("group_id", "id"),
        ForeignKeyConstraint(
            ["group_id", "paid_by_member_id"],
            ["group_members.group_id", "group_members.member_id"],
        ),
        Index("transactions_group_created_idx", "group_id", text("created_at DESC")),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    group_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("expense_groups.id", ondelete="CASCADE"),
        nullable=False,
    )
    paid_by_member_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    group: Mapped[ExpenseGroup] = relationship(back_populates="transactions")
    items: Mapped[list[TransactionItem]] = relationship(back_populates="transaction")


class TransactionItem(Base):
    __tablename__ = "transaction_items"
    __table_args__ = (
        CheckConstraint("btrim(name) <> ''"),
        CheckConstraint("amount_cents >= 0"),
        UniqueConstraint("group_id", "id"),
        ForeignKeyConstraint(
            ["group_id", "transaction_id"],
            ["transactions.group_id", "transactions.id"],
            ondelete="CASCADE",
        ),
        Index("transaction_items_transaction_idx", "group_id", "transaction_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    group_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), nullable=False
    )
    transaction_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), nullable=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    amount_cents: Mapped[int] = mapped_column(BigInteger, nullable=False)

    transaction: Mapped[ExpenseTransaction] = relationship(back_populates="items")
