import logging
from fastapi import APIRouter, Depends, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/debts", tags=["Debts"])

@router.get("/{group_id}")
async def get_debts(group_id: str):
	logger.info(f"Fetching debts for group {group_id}")
	return {"message": f"Debts for group {group_id} are working!"}