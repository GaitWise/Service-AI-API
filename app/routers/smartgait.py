from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from services.report_services import generate_report
from services.smartgait_services import process_smartgait

# 요청 데이터 모델 정의
class SmartGaitRequest(BaseModel):
    walkingId: str
    height: str
    weight: str
    weight_type: str

router = APIRouter()

@router.post("/smartgait")
def smartgait_def(request: SmartGaitRequest):
    try:
        walkingId = request.walkingId
        height = request.height
        weight = request.weight
        weight_type = request.weight_type
        response_data = process_smartgait(walkingId, height, weight, weight_type)
        report = generate_report(response_data)

        combined_response = {
            "report": report,
            "data": response_data
        }
        return JSONResponse(content=combined_response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
