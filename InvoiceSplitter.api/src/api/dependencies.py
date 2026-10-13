from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db_session
from modules.expense_groups.repository import ExpenseGroupsRepository
from modules.expense_groups.service import ExpenseGroupsService


def get_expense_groups_service(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> ExpenseGroupsService:
    repository = ExpenseGroupsRepository(session)

    service = ExpenseGroupsService(repository)

    return service