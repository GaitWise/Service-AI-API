from fastapi import APIRouter

router = APIRouter()

@router.get("/report")
def report():
    
    # 1. csv 파일 로드 후 데이터 추출
    
    # 2. 센서 데이터를 백터화 시켜 milvus 벡터 Database에서 같은 유사한 질병 판단
    
    # 3. 센서데이터를 넣어 AI 모델를 통해 질병 판단.
    
    # 4. 2가징 방식으로 나온 판단 결과를 통해 관련 논문이나 txt를 참고하기
    
    # 5. 랭체인을 통한 형식에 맞는 보고서 출력 
    
    return 
