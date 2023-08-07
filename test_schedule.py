import schedule
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List
import uvicorn
from schema import DataFrameRow
from data_process import process_data


# step1.실행 주기 설정
schedule.every().day.at("23:00").do(process_data)

# step2.스캐쥴 시작
while True:
    schedule.run_pending()
    time.sleep(60)


# def job():
#     url= "https://www.google.co.kr/search?q=national+park&source=lnms&tbm=nws"
#     print(url) # Google 뉴스에서 'national park' 검색결과
# # 매일 특정 HH:MM 및 다음 HH:MM:SS에 작업 실행
# schedule.every().day.at("00:00").do(job)
# import datetime
# import pytz
# now = datetime.datetime.now() 
# print(now)
# local_timezone = pytz.timezone("Asia/Seoul")  # "Asia/Seoul"은 대한민국의 시간대입니다.
# local_time = datetime.datetime.now(local_timezone)
# print(local_time)
# while True:
#     schedule.run_pending()
#     time.sleep(1)