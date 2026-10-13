import logging
from typing import Annotated
from uuid import UUID

from api.dependencies import get_expense_groups_service
from fastapi import APIRouter, Depends
from modules.expense_groups.schemas import GetGroupsResponse
from modules.expense_groups.service import ExpenseGroupsService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/expenseGroups", tags=["Expense Groups"])


@router.get("/{user_id}", response_model=GetGroupsResponse)
async def get_groups(
    user_id: UUID,
    service: Annotated[ExpenseGroupsService, Depends(get_expense_groups_service)],
) -> GetGroupsResponse:
    logger.info("Getting expense groups for user %s", user_id)
    groups = await service.get_user_expense_groups(user_id)
    return GetGroupsResponse(
        groups=groups
    )
