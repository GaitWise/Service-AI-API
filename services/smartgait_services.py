# Service: 데이터 처리 및 비즈니스 로직
from bson import ObjectId
from database.dbconnet import DB_Connect
from utils.helpers import ( get_nested_data, calculate_steps, calculate_distance, calculate_calories, 
                           calculate_balance_score, detect_abnormal_gait, recommend_training)


# [Function] MongoDB에서 걸음 데이터를 조회
# Parameters: db (object): MongoDB 연결 객체, object_id_str (str): 조회할 ObjectId 문자열
# Returns: dict: 조회된 walking 데이터 또는 에러 메시지
def get_walking_data(db, object_id_str):
    try:
        object_id = ObjectId(object_id_str)
        walking_data = db['walking'].find_one({"_id": object_id})
        if walking_data:
            walking_data["_id"] = str(walking_data["_id"])
            return walking_data
        else:
            return {"error": "데이터를 찾을 수 없습니다"}
    except Exception as e:
        return {"error": f"유효하지 않은 ObjectId: {e}"}


# [Function] MongoDB 데이터에서 필요한 정보를 처리
# Parameters: db (object): MongoDB 연결 객체, walking_data (dict): 조회된 walking 데이터
# Returns: dict: 처리된 센서 데이터 및 걸음 데이터
def process_walking_data(db, walking_data):
    try:
        acc_ids = walking_data.get("acc", [])
        rot_ids = walking_data.get("rot", [])
        gyro_ids = walking_data.get("gyro", [])
        walkingtime = walking_data.get("walking_time", [])

        acc_data = get_nested_data(db, acc_ids, "acc")
        rot_data = get_nested_data(db, rot_ids, "rot")
        gyro_data = get_nested_data(db, gyro_ids, "gyro")

        return {
            "event_time": walking_data.get("event_time", []),
            "acc": acc_data,
            "rot": rot_data,
            "gyro": gyro_data,
            "walkingtime": walkingtime
        }
        
    except Exception as e:
        return {"error": f"walking 데이터 처리 중 오류 발생: {e}"}


# [Function] Smart Gait 데이터를 처리하고 결과 반환
# Returns: dict: 걸음 수, 거리, 칼로리, 균형 점수, 걸음 상태 및 추천 훈련 데이터
def process_smartgait(walkingId, height, weight, weight_type):
    db = DB_Connect()
    print('IN')

    walking_data = get_walking_data(db, walkingId)
    print('walking_data', walking_data)
    processed_data = process_walking_data(db, walking_data)
    print('processed_data', processed_data)

    acc_values = processed_data.get("acc", [])
    gyro_values = processed_data.get("gyro", [])
    walkingtime = processed_data.get("walkingtime", [])

    accx = acc_values[0]['accX']
    accy = acc_values[0]['accY']
    accz = acc_values[0]['accZ']
    gyroy = gyro_values[0]['gyroY']

    steps = calculate_steps(accz)
    distance = calculate_distance(steps, height)
    calories = calculate_calories(weight, walkingtime)
    balance_score = calculate_balance_score(gyroy)
    gait_status = detect_abnormal_gait(accx, accy, gyroy)
    training_recommendation = recommend_training(gait_status, balance_score)

    return {
        "steps": steps,
        "distance": f"{distance:.2f} m",
        "calories": f"{calories:.2f} kcal",
        "balance_score": f"{balance_score:.2f}",
        "gait_status": gait_status,
        "training_recommendation": training_recommendation
    }
