import asyncio
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from db.models import ExpenseGroup
from modules.expense_groups.repository import ExpenseGroupsRepository
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession


def test_get_groups_by_user_id_returns_query_results() -> None:
    user_id = uuid4()
    expected_groups = [Mock(spec=ExpenseGroup)]
    result = Mock()
    result.all.return_value = expected_groups
    session = AsyncMock(spec=AsyncSession)
    session.scalars.return_value = result

    groups = asyncio.run(
        ExpenseGroupsRepository(session).get_groups_by_user_id(user_id)
    )

    statement = session.scalars.await_args.args[0]
    sql = str(statement.compile(dialect=postgresql.dialect()))

    assert groups == expected_groups
    assert "JOIN group_members" in sql
    assert "JOIN members" in sql
    assert "members.user_id =" in sql


def test_get_groups_by_user_id_returns_empty_list_when_no_groups_exist() -> None:
    result = Mock()
    result.all.return_value = []
    session = AsyncMock(spec=AsyncSession)
    session.scalars.return_value = result

    groups = asyncio.run(
        ExpenseGroupsRepository(session).get_groups_by_user_id(uuid4())
    )

    assert groups == []
