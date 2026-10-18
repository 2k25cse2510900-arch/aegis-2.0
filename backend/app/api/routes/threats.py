from fastapi import APIRouter

router = APIRouter(prefix="/threats", tags=["threats"])


@router.get("")
def threats_placeholder():
    return {"status": "not_implemented", "items": []}
