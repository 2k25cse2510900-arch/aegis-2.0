from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/status")
def auth_status():
    return {"status": "not_configured", "message": "Authentication is a placeholder."}
