from flask import Blueprint, request, render_template, redirect, url_for
from database import db, InventoryItem

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/')
def home():
    inventory = InventoryItem.query.all()
    return render_template('products/home.html', inventory=inventory)

@products_bp.route('/add_item', methods = ['GET', 'POST'])
def add_item():
    if request.method == 'GET':
        return render_template('products/add_item.html')
    if request.method == 'POST':
        data = request.form
        new_item = InventoryItem(item_name=data['item_name'], item_description=data['item_description'], item_price=data['item_price'], item_qty=data['item_qty'])
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('products.home'))

@products_bp.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    item = InventoryItem.query.get(item_id)
    if request.method == 'POST':
        item.item_name = request.form['item_name']
        item.item_description = request.form['item_description']
        item.item_price = request.form['item_price']
        item.item_qty = request.form['item_qty']
        db.session.commit()
        return redirect(url_for('products.view_all'))
    return render_template('products/update_item.html', item=item)

@products_bp.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = InventoryItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('products.home'))

# # Update item quantity
# @products_bp.post('/update_quantity')
# def update_item():
#     data = request.json
#     item = InventoryItem.query.filter_by(item_name=data['Item_Name']).first()
#     if not item:
#         return f"Item with name {data['Item_Name']} does not exist"
    
#     item.item_qty = data['Item_Qty']
#     db.session.commit()
#     return f"Item with name {data['Item_Name']} updated successfully"

# # Update item price
# @products_bp.post('/update_price')
# def update_price():
#     data = request.json
#     item = InventoryItem.query.filter_by(item_name=data['Item_Name']).first()
#     if not item:
#         return f"Item with name {data['Item_Name']} does not exist"
    
#     item.item_price = data['Item_Price']
#     db.session.commit()
#     return f"Item with name {data['Item_Name']} updated successfully"

# Get item details
@products_bp.post('/get_item')
def get_item():
    data = request.json
    item = InventoryItem.query.filter_by(item_name=data['Item_Name']).first()
    if not item:
        return f"Item with name {data['Item_Name']} does not exist"
    
    return f"Item Name: {item.item_name}<br>Item Description: {item.item_description}<br>Item Price: {item.item_price}<br>Item Quantity: {item.item_qty}"

