from flask import Blueprint, request
import psycopg2
import dotenv
import os

# get url from .env file
dotenv.load_dotenv()
url = os.getenv('DATABASE_URL')

products_bp = Blueprint('products', __name__)
conn = psycopg2.connect(url)

@products_bp.get('/')
def get_products():
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM InventoryItem;")
            inventory = cur.fetchall()
            items_return = "Name : Quantity<br>"
            items_return += "<br>".join([str(item[1]) + " : " + str(item[4]) for item in inventory])
            return items_return
        
@products_bp.post('/add_item')
def add_item():
    data = request.json
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO InventoryItem (Item_Name, Item_Description, Item_Price, Item_Qty) VALUES (%s, %s, %s, %s);", (data['Item_Name'], data['Item_Description'], data['Item_Price'], data['Item_Qty']))
            return (f"Item named {data['Item_Name']} added successfully")  

# Delete item from inventory
@products_bp.delete('/delete_item')
def delete_item():
    data = request.json
    with conn:
        with conn.cursor() as cur:
            
            # Check if item exists
            cur.execute("SELECT * FROM InventoryItem WHERE Item_Name = %s;", (data['Item_Name'],))
            item = cur.fetchall()
            if len(item) == 0:
                return (f"Item with name {data['Item_Name']} does not exist")
            
            # Check if item is being used in a transaction
            try : 
                cur.execute("DELETE FROM InventoryItem WHERE Item_Name = %s;", (data['Item_Name'],))
            except psycopg2.errors.ForeignKeyViolation as e:
                return (f"Item with name {data['Item_Name']} cannot be deleted as it is being used in a transaction")
            
            return (f"Item with name {data['Item_Name']} deleted successfully")

# Update item quantity
@products_bp.post('/update_quantity')
def update_item():
    data = request.json
    with conn:
        with conn.cursor() as cur:
            
            # Check if item exists
            cur.execute("SELECT * FROM InventoryItem WHERE Item_Name = %s;", (data['Item_Name'],))
            item = cur.fetchall()
            if len(item) == 0:
                return (f"Item with name {data['Item_Name']} does not exist")
            
            # Update item quantity
            cur.execute("UPDATE InventoryItem SET Item_Qty = %s WHERE Item_Name = %s;", (data['Item_Qty'], data['Item_Name']))
            return (f"Item with name {data['Item_Name']} updated successfully")
        
# Update item price
@products_bp.post('/update_price')
def update_price():
    data = request.json
    with conn:
        with conn.cursor() as cur:
            
            # Check if item exists
            cur.execute("SELECT * FROM InventoryItem WHERE Item_Name = %s;", (data['Item_Name'],))
            item = cur.fetchall()
            if len(item) == 0:
                return (f"Item with name {data['Item_Name']} does not exist")
            
            # Update item price
            cur.execute("UPDATE InventoryItem SET Item_Price = %s WHERE Item_Name = %s;", (data['Item_Price'], data['Item_Name']))
            return (f"Item with name {data['Item_Name']} updated successfully")
    
# Get item details
@products_bp.post('/get_item')
def get_item():
    data = request.json
    with conn:
        with conn.cursor() as cur:
            
            # Check if item exists
            cur.execute("SELECT * FROM InventoryItem WHERE Item_Name = %s;", (data['Item_Name'],))
            item = cur.fetchall()
            if len(item) == 0:
                return (f"Item with name {data['Item_Name']} does not exist")
            
            # Return item details
            return (f"Item Name: {item[0][1]}<br>Item Description: {item[0][2]}<br>Item Price: {item[0][3]}<br>Item Quantity: {item[0][4]}")