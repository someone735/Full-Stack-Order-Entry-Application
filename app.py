from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

OrdersDB = {}
order_ID_counter = 0

class Order:
    def __init__(self, id, customer_name, ):
        self.ID = id

class Line_Item:
    def __init__(self, **item_names):
        self.item_names = []
        for item in item_names:
            self.item_names.append(item)
            
def line_item_verification(line_item_names, line_items_quantity):
    
    if len(line_item_names) != len(line_items_quantity): #every item name must have a quantity
        return False
    
    for i in line_item_names:   # all line_item_names must be provided
        if i.lower == "null" or i.lower == "none":
            return False
        
    for j in line_items_quantity: # all line_item quantities must be greater than 0
        if j <= 0:
            return False 
        
    return True    


@app.get("/")
def root():
    return {"message": "Hello World"}


# This /order endpoint should process the form data, 
# create a sales order object, 
# and store it in an in-memory dictionary.

@app.post("/order")
def create_sales_order(customer_name: str, line_item_names: list[str], line_item_quantity: list[int]):
    
    
    if (False):
        raise HTTPException(status_code=400, detail= "invalid input")
    return ("result")

