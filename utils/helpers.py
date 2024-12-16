# Util 폴더: 재사용 가능한 유틸리티 함수들
import numpy as np
from bson import ObjectId
from scipy.signal import find_peaks

# [Function] MongoDB에서 ObjectId 기반 데이터 조회
# Parameters: db (object): MongoDB 데이터베이스 객체, object_ids (list): MongoDB ObjectId 리스트 또는 단일 ObjectId, collection_name (str): 조회할 컬렉션 이름
# Returns: list: 조회된 데이터 리스트
def get_nested_data(db, object_ids, collection_name):
    try:
        if not isinstance(object_ids, list):
            object_ids = [object_ids]
        object_ids = [oid if isinstance(oid, ObjectId) else ObjectId(oid) for oid in object_ids]
        data = list(db[collection_name].find({"_id": {"$in": object_ids}}))
        
        for item in data:
            item["_id"] = str(item["_id"])
        
        return data
    except Exception as e:
        return {"error": f"{collection_name} 데이터를 가져오는 중 오류 발생: {e}"}
    

# [Function] 걸음 수 계산
# Parameters: acc_z (list): Z축 가속도 데이터
# Returns: int: 걸음 수
def calculate_steps(acc_z):
    peaks, _ = find_peaks(acc_z, height=0.03, distance=10)
    return len(peaks)


# [Function] 이동 거리 계산
# Parameters: steps (int): 걸음 수, height (float): 키 (m)
# Returns: float: 총 이동 거리 (m)
def calculate_distance(steps, height):
    stride_length = height * 0.415 
    return steps * stride_length


# [Function] 에너지 소비량 계산
# Parameters: weight (float): 체중 (kg), walking_time (str): 걸은 시간 ("분:초" 형식)
# Returns: float: 소모된 칼로리 (kcal)
def calculate_calories(weight, walking_time):
    minutes, seconds = map(int, walking_time.split(":"))
    time_in_hours = (minutes + (seconds / 60)) / 60 
    METs = 3.5  
    calories_burned = METs * weight * time_in_hours  
    return round(calories_burned, 2) 


# [Function] 균형 점수 계산
# Parameters: gyro_data (list): Y축 자이로스코프 데이터
# Returns: float: 균형 상태 점수 (0~1)
def calculate_balance_score(gyro_data):
    balance_variation = np.var(gyro_data)  
    balance_score = max(0, 1 - balance_variation / 10)  
    return balance_score 


# [Function] 비정상 걸음걸이 감지
# Parameters: acc_x: X축 가속도, acc_y: Y축 가속도, gyro_y: Y축 자이로스코프 
# Returns: str: "정상적인 걸음걸이" 또는 "비정상적인 걸음걸이 감지"
def detect_abnormal_gait(acc_x, acc_y, gyro_y):
    stride_variation = np.var(acc_x) + np.var(acc_y)  
    balance_variation = np.var(gyro_y)  
    if stride_variation > 1.5 or balance_variation > 1.5:
        return "비정상적인 걸음걸이 감지"
    return "정상적인 걸음걸이"


# [Function] 훈련 프로그램 추천
# Parameters: gait_status: 걸음걸이 상태, balance_score: 균형 상태 점수 (0~1)
# Returns: str: 추천 훈련 프로그램 또는 메시지
def recommend_training(gait_status, balance_score):
    if gait_status == "비정상적인 걸음걸이 감지" or balance_score < 0.5:
        return "균형 훈련 프로그램: 1. 한 발 서기, 2. 무릎 굽히기, 3. 라인 걷기"
    return "걸음걸이가 정상입니다. 지속적으로 걷기 운동을 추천합니다."

