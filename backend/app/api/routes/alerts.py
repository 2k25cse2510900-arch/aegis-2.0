from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
def alerts_placeholder():
    return {"status": "not_implemented", "items": []}
