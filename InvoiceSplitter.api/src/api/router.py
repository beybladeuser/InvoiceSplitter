from fastapi import APIRouter

from modules.scan.router import router as scan_router
from modules.debts.router import router as debts_router

api_router = APIRouter()

api_router.include_router(scan_router)
api_router.include_router(debts_router)