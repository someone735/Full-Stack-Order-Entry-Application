from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List


app = FastAPI()

app.mount("/static", StaticFiles(directory="Template_Folder", html = True), name = "static")

OrdersDB = {}
SalesOrderCounter = 0

def SalesOrderVerification(CustomerName: str, LineItemName: List[str], LineItemQuantity: List[int]):
    if not CustomerName or not LineItemName or not LineItemQuantity:
        return "Customer name, line item names, and quantities cannot be empty."
    if len(LineItemName) != len(LineItemQuantity):
        return "Line item names and quantities must match in length."
    for index, quantity in enumerate(LineItemQuantity):
        if quantity <= 0:
            return f"The item {LineItemName[index]} quantity must be greater than zero."
    return True

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("Template_Folder/index.html")

@app.post("/order", response_class = HTMLResponse)
async def submit(
    CustomerName: str = Form(...),
    LineItemName: List[str] = Form(...),
    LineItemQuantity: List[int] = Form(...)
):
    global SalesOrderCounter
    
    VerificationResponse = SalesOrderVerification(CustomerName, LineItemName, LineItemQuantity)
    
    if isinstance(VerificationResponse, bool):
        SalesOrderCounter += 1
        OrdersDB[SalesOrderCounter] = {
            "CustomerName": CustomerName,
            "LineItemName": LineItemName,
            "LineItemQuantity": LineItemQuantity
        }
        return f''' 
        <div>Order received successfully!</div><br>
        <div>Order ID: {SalesOrderCounter}</div>
        <div>Customer Name: {CustomerName}</div>
        <div>Line Item Names: {LineItemName}</div>
        <div>Line Item Quantities: {LineItemQuantity}</div> 
        '''
    
    else:
        raise HTTPException(status_code=400, detail = VerificationResponse)

@app.get("/orders", response_class=JSONResponse)
async def getSalesOrders():
    return JSONResponse(content={
        "counter": SalesOrderCounter,
        "orders": OrdersDB
    })
    

