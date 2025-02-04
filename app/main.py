from fastapi import FastAPI
from app.routers import smartgait
from database.dbconnet import DB_Connect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# MongoDB 데이터베이스 가져오기
db = DB_Connect()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서의 요청을 허용합니다.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용합니다.
    allow_headers=["*"],  # 모든 헤더를 허용합니다
)

#Smartgait router
app.include_router(smartgait.router)