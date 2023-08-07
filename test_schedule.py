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
schedule.every().day.at("14:34").do(process_data)

# step2.스캐쥴 시작
while True:
    schedule.run_pending()
    time.sleep(60)