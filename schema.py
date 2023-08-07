from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List
import uvicorn

class DataFrameRow(BaseModel):
    location: str
    time: str
    link: str
    message : str
    criminal_info : str