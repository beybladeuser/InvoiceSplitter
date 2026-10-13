from uuid import UUID

from db.models import ExpenseGroup
from modules.expense_groups.repository import ExpenseGroupsRepository


class ExpenseGroupsService:
    def __init__(self, repository: ExpenseGroupsRepository):
        self.repository = repository

    async def get_user_expense_groups(self, user_id: UUID) -> list[ExpenseGroup]:
        return await self.repository.get_groups_by_user_id(user_id)
