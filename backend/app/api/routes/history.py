from fastapi import APIRouter

router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
def history_placeholder():
    return {"status": "not_implemented", "items": []}
