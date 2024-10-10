from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_def():
    a= 15
    return a
