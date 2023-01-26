from typing import Union
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

import json
import requests
from json import dumps

from pandas import read_excel

class Item(BaseModel):
    url: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Teste 2"}

@app.post("/test")
def create_item(item: Item):
    data = pd.read_excel("file.xlsx", sheet_name="Planilha1")

    json_data = data.to_json(orient="records")
    json_data = json.loads(json_data)
    return {"success": "true", "data": json_data}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}