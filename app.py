from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI()

app.mount("/", StaticFiles(directory="Template_Folder", html = True), name = "static")

# OrdersDB = {}
# order_ID_counter = 0

# class Order:
#     def __init__(self, id, customer_name, ):
#         self.ID = id

# class Line_Item:
#     def __init__(self, **item_names):
#         self.item_names = []
#         for item in item_names:
#             self.item_names.append(item)
            
# def line_item_verification(line_item_names, line_items_quantity):
#     if len(line_item_names) != len(line_items_quantity): #every item name must have a quantity
#         return False
    
#     for i in line_item_names:   # all line_item_names must be provided
#         if i.lower == "null" or i.lower == "none":
#             return False
        
#     for j in line_items_quantity: # all line_item quantities must be greater than 0
#         if j <= 0:
#             return False 
        
#     return True    


# This /order endpoint should process the form data, 
# create a sales order object, 
# and store it in an in-memory dictionary.
    
@app.get("/")
def root():
    return{"message": "hi"}

class item(BaseModel):
    customer_name: str
    item_name: str
    item_quantity: str

@app.post("/order")
async def submit(item: item):
    print(item)
    return {"message": "Recieved: "}
    

