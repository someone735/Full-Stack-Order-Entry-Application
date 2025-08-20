from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List


app = FastAPI()

app.mount("/", StaticFiles(directory="Template_Folder", html = True), name = "static")


@app.post("/order", response_class = JSONResponse)
async def submit(
    CustomerName: str = Form(...),
    LineItemName: List[str] = Form(...),
    LineItemQuantity: List[int] = Form(...)
):
    print("Received")
    return {"message": "Recieved:"}
    

