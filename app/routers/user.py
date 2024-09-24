from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_def():
    a= 10
    return a
