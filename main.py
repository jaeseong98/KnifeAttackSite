from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List
import uvicorn
from schema import DataFrameRow
from data_process import process_data
import schedule
import time
import glob
import os

app = FastAPI()

# 가상의 DataFrame 생성 (예시용)
all_csv_files = glob.glob(os.path.join(os.getcwd() + "/data/final", "*.csv"))

# 파일의 마지막 수정 시간을 기준으로 정렬합니다.
latest_csv_file = max(all_csv_files, key=os.path.getctime)

# 가장 최근의 csv 파일을 pandas로 읽습니다.
df = pd.read_csv(latest_csv_file)
# df = pd.read_csv("/home/jaeseong2418/myenv/final_data_20230806_06시53분19초.csv")

class DataFrameRow(BaseModel):
    location: str
    time: str
    link: str
    message : str
    criminal_info : str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/all_rows", response_model=List[DataFrameRow])
def news_data():
    if df.empty:
        raise HTTPException(status_code=404, detail="DataFrame is empty.")
    
    rows = []
    for _, row in df.iterrows():
        rows.append(DataFrameRow(location=row['Location'], time=row['Time'], link=row['Link'], message=row['Text'],criminal_info=row['Criminal Info']))
    return rows

# from fastapi import FastAPI, BackgroundTasks, Depends
# from pydantic import BaseModel
# import pandas as pd
# from typing import List
# import uvicorn
# import schedule
# import time

# app = FastAPI()

# def update_data():
#     df = process_data()
#     return df
# def run_schedule():
#     schedule.every().day.at("09:00").do(update_data)
#     while True:
#         schedule.run_pending()
#         time.sleep(60)

# @app.on_event("startup")
# async def startup_event():
#     task = BackgroundTasks()
#     task.add_task(run_schedule)

# class DataFrameRow(BaseModel):
#     location: str
#     time: str
#     link: str
#     message : str
#     criminal_info : str


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# # def get_df():
# #     return df

# @app.get("/all_rows", response_model=List[DataFrameRow])
# def news_data(df: pd.DataFrame = Depends(update_data)):
#     if df.empty:
#         raise HTTPException(status_code=404, detail="DataFrame is empty.")

    
#     rows = []
#     for _, row in df.iterrows():
#         rows.append(DataFrameRow(location=row['Location'], time=row['Time'], link=row['Link'], message=row['Text'],criminal_info=row['Criminal Info']))
#     return rows

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)