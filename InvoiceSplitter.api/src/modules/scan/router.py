import logging

from fastapi import APIRouter, Depends, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scan", tags=["Scan"])

@router.get("/")
async def scan():
	logger.info("Scanning endpoint accessed")
	return {"message": "Scan endpoint is working!"}