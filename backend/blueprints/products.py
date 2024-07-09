from flask import Blueprint, request
import dotenv
import os
from database import db, InventoryItem

# get url from .env file
dotenv.load_dotenv()
url = os.getenv('DATABASE_URL')

products_bp = Blueprint('products', __name__)

@products_bp.get('/')
def get_products():
    inventory = InventoryItem.query.all()
    items_return = "Name : Quantity<br>"
    items_return += "<br>".join([str(item.item_name) + " : " + str(item.item_qty) for item in inventory])
    return items_return

@products_bp.post('/add_item')
def add_item():
    data = request.json
    new_item = InventoryItem(item_name=data['Item_Name'], item_description=data['Item_Description'], item_price=data['Item_Price'], item_qty=data['Item_Qty'])
    db.session.add(new_item)
    db.session.commit()
    return f"Item named {data['Item_Name']} added successfully"

# Delete item from inventory
@products_bp.delete('/delete_item')
def delete_item():
    data = request.json
    item = InventoryItem.query.filter_by(item_name=data['Item_Name']).first()
    if not item:
        return f"Item with name {data['Item_Name']} does not exist"
    
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Item with name {data['Item_Name']} cannot be deleted as it is being used in a transaction"
    
    return f"Item with name {data['Item_Name']} deleted successfully"

# Update item quantity
@products_bp.post('/update_quantity')
def update_item():
    data = request.json
    item = InventoryItem.query.filter_by(item_name=data['Item_Name']).first()
    if not item:
        return f"Item with name {data['Item_Name']} does not exist"
    
    item.item_qty = data['Item_Qty']
    db.session.commit()
    return f"Item with name {data['Item_Name']} updated successfully"

# Update item price
@products_bp.post('/update_price')
def update_price():
    data = request.json
    item = InventoryItem.query.filter_by(item_name=data['Item_Name']).first()
    if not item:
        return f"Item with name {data['Item_Name']} does not exist"
    
    item.item_price = data['Item_Price']
    db.session.commit()
    return f"Item with name {data['Item_Name']} updated successfully"

# Get item details
@products_bp.post('/get_item')
def get_item():
    data = request.json
    item = InventoryItem.query.filter_by(item_name=data['Item_Name']).first()
    if not item:
        return f"Item with name {data['Item_Name']} does not exist"
    
    return f"Item Name: {item.item_name}<br>Item Description: {item.item_description}<br>Item Price: {item.item_price}<br>Item Quantity: {item.item_qty}"