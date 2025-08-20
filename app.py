from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List


app = FastAPI()

app.mount("/static", StaticFiles(directory="Template_Folder", html = True), name = "static")

OrdersDB = {}
SalesOrderCounter = 0

def SalesOrderVerification(CustomerName: str, LineItemName: List[str], LineItemQuantity: List[int]):
    if not CustomerName or not LineItemName or not LineItemQuantity:
        return False
    if len(LineItemName) != len(LineItemQuantity):
        return "Line item names and quantities must match in length."
    for index, quantity in enumerate(LineItemQuantity):
        if quantity <= 0:
            return f"{LineItemName[index]}\'s quantity must be greater than zero."
    return True

@app.post("/order", response_class = HTMLResponse)
async def submit(
    CustomerName: str = Form(...),
    LineItemName: List[str] = Form(...),
    LineItemQuantity: List[int] = Form(...)
):
    print("Customer Name:", CustomerName)
    print("Line Item Names:", LineItemName)
    print("Line Item Quantities:", LineItemQuantity)
    if SalesOrderVerification(CustomerName, LineItemName, LineItemQuantity):
        OrdersDB[SalesOrderCounter] = {
            "CustomerName": CustomerName,
            "LineItemName": LineItemName,
            "LineItemQuantity": LineItemQuantity
        }
        SalesOrderCounter += 1
        return {"message": "Recieved:"} 
    else:
        raise HTTPException(status_code=400, detail="Invalid order data")
    

