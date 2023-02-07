from typing import Union
import pandas as pd
from pandas import read_excel
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import json
from json import dumps
import boto3
import string
import random
import os

class Item(BaseModel):
    bucket: str
    file: str

app = FastAPI()

@app.post("/excelToJson", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    session = boto3.Session(
        aws_access_key_id=os.environ['AWS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET']
    )

    s3 = session.resource('s3')

    sheet = s3.Object(item.bucket, item.file)
    fileContent = sheet.get()['Body'].read()
    sheetContent = pd.read_excel(fileContent)

    content = sheetContent.to_json(orient="records")

    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
    fileName = (name) + ".json"

    s3File = s3.Bucket(item.bucket).put_object(
        Key=fileName,
        Body=content
    )

    if s3File:
        return {"success": "true", "bucket": item.bucket, "fileKey": fileName}
    raise HTTPException(500, f"Erro ao converter o arquivo")