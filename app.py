from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional


app = FastAPI() # Initialize FastAPI application 

app.mount("/static", StaticFiles(directory="Template_Folder", html = True), name = "static") # Mount the static files directory

# Initialize in-memory database and order counter
OrdersDB = {}
SalesOrderCounter = 0

# Workaround to handle empty quantities in LineItemQuantity
def cleanItemQuantities(LineItemQuantity: List[str]):
    converted_List = []
    # Convert string quantities to integers, handling empty strings
    for i in LineItemQuantity:
        if i.isdigit():
            converted_List.append(int(i))
        else:
            converted_List.append(None)
    # Return the converted list
    return converted_List

# Function to verify sales order details
def SalesOrderVerification(CustomerName: str, LineItemName: List[str], LineItemQuantity: List[int]):
    # Check if customer name is provided
    if not CustomerName:
        return "Customer name cannot be empty."
    # Check if customer name is or contains a number
    if any(char.isdigit() for char in CustomerName):
        return "Customer name cannot be or have a number."
    # Check if line item names and quantities match in length
    if len(LineItemName) != len(LineItemQuantity):
        return "Line item names and quantities must match in length."
    # Check if line item names are provided and not empty
    for (index, name) in enumerate(LineItemName):
        if not name:
            return f"Line item {index+1}'s name cannot be empty."
        if not name.startswith("id:") and any(char.isdigit() for char in name):
            return f"Line item {index+1}'s name must be use 'id:' when using an ID number."
        if name.isdigit():
            return f"Line item {index+1}'s name cannot be a number."
    # check if item quantities are greater than zero and not empty
    for index, quantity in enumerate(LineItemQuantity):
        if not quantity:
            return f"The item {LineItemName[index]} cannot be empty."
        if quantity <= 0:
            return f"The item {LineItemName[index]} quantity must be greater than zero."
    # If all checks pass, return True
    return True

# Define the root endpoint to serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("Template_Folder/index.html")

# Endpoint to handle sales order submission
@app.post("/order", response_class = HTMLResponse)
async def submit(
    CustomerName: str = Form(""),
    LineItemName: List[str] = Form([]),
    LineItemQuantity: List[str] = Form([]) # Workaround for empty quantities in LineItemQuantity
):
    LineItemQuantity = cleanItemQuantities(LineItemQuantity)  # Clean up LineItemQuantity
    # Accesses global variable to keep track of the sales order counter
    global SalesOrderCounter
    # Verify the sales order details
    VerificationResponse = SalesOrderVerification(CustomerName, LineItemName, LineItemQuantity)
    
    # Successful verification
    if isinstance(VerificationResponse, bool):
        SalesOrderCounter += 1
        # Store the order in the in-memory database
        OrdersDB[SalesOrderCounter] = {
            "CustomerName": CustomerName,
            "LineItemName": LineItemName,
            "LineItemQuantity": LineItemQuantity
        }
        # Return a success message with order details
        return f''' 
        <div>Order received successfully!</div><br>
        <div>Order ID: {SalesOrderCounter}</div>
        <div>Customer Name: {CustomerName}</div>
        <div>Line Item Names: {LineItemName}</div>
        <div>Line Item Quantities: {LineItemQuantity}</div> 
        '''
    else:
        # If verification fails, raise an HTTP exception with the error message
        raise HTTPException(status_code=400, detail = VerificationResponse + " Please try again.")

# Endpoint to retrieve all sales orders
@app.get("/orders", response_class=JSONResponse)
async def getSalesOrders():
    return JSONResponse(content={
        "counter": SalesOrderCounter,
        "orders": OrdersDB
    })
    

