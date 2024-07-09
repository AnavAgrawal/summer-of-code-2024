from flask import Blueprint, request, render_template, redirect, url_for
from database import db, InventoryItem
from flask_login import current_user

products_bp = Blueprint('products', __name__, template_folder='templates')

# Check if user is logged in before accessing any routes
@products_bp.before_request
def before_request():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login')) 

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
        return redirect(url_for('products.home'))
    return render_template('products/update_item.html', item=item)

@products_bp.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = InventoryItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('products.home'))

