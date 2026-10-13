from uuid import UUID

from db.models import ExpenseGroup, GroupMember, Member
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ExpenseGroupsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_groups_by_user_id(self, user_id: UUID) -> list[ExpenseGroup]:
        statement = (
            select(ExpenseGroup)
            .join(GroupMember, GroupMember.group_id == ExpenseGroup.id)
            .join(Member, Member.id == GroupMember.member_id)
            .where(Member.user_id == user_id)
        )
        result = await self.session.scalars(statement)
        return list(result.all())
