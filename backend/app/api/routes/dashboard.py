from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def dashboard_placeholder():
    return {"status": "not_implemented", "message": "Dashboard data is not configured."}
