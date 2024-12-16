from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def DB_Connect():
    try:
        # MongoDB 연결 문자열
        client = MongoClient("mongodb://DNSLab:sunmoon418!@210.119.32.188:20057/Gaitwise?authSource=admin")
        db = client['Gaitwise']
        print("MongoDB 연결 성공")
        return db
    except ConnectionFailure as e:
        print(f"MongoDB 연결 실패: {e}")
        return None
