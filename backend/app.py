from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import dotenv
import os
from products import products_bp

# get url from .env file
dotenv.load_dotenv()
url = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.register_blueprint(products_bp, url_prefix='/products')

class InventoryItem(db.Model):
    Item_SKU = db.Column(db.Integer, primary_key=True)
    Item_Name = db.Column(db.String, nullable=False)
    Item_Description = db.Column(db.String, nullable=False)
    Item_Price = db.Column(db.Integer, nullable=False)
    Item_Qty = db.Column(db.Integer, nullable=False)

class Customer(db.Model):
    c_ID = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String, nullable=False)
    c_email = db.Column(db.String, nullable=False)
    c_contact = db.Column(db.String, nullable=False)

class Staff(db.Model):
    s_ID = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String, nullable=False)
    s_email = db.Column(db.String, nullable=False)
    s_isAdmin = db.Column(db.Boolean, nullable=False)
    s_contact = db.Column(db.String, nullable=False)
    pass_hash = db.Column(db.Text, nullable=False)

class Transaction(db.Model):
    t_ID = db.Column(db.Integer, primary_key=True)
    c_ID = db.Column(db.Integer, db.ForeignKey('customer.c_ID'), nullable=False)
    Item_SKU = db.Column(db.Integer, db.ForeignKey('inventory_item.Item_SKU'), nullable=False)
    s_ID = db.Column(db.Integer, db.ForeignKey('staff.s_ID'), nullable=False)
    t_Date = db.Column(db.Date, nullable=False)
    t_Amount = db.Column(db.Integer, nullable=False)
    t_Category = db.Column(db.String, nullable=False)


@app.get('/')
def get_inventory():
    inventory = InventoryItem.query.all()
    return str(inventory)

@app.post('/add_customer')
def add_customer():
    data = request.json
    new_customer = Customer(c_name=data['c_name'], c_email=data['c_email'], c_contact=data['c_contact'])
    db.session.add(new_customer)
    db.session.commit()
    return f"Customer named {data['c_name']} added successfully"

@app.post('/add_staff')
def add_staff():
    data = request.json
    pass_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_staff = Staff(s_name=data['s_name'], s_email=data['s_email'], s_isAdmin=data['s_isAdmin'], s_contact=data['s_contact'], pass_hash=pass_hash)
    db.session.add(new_staff)
    db.session.commit()
    return f"Staff named {data['s_name']} added successfully"

@app.post('/add_transaction')
def add_transaction():
    data = request.json
    customer = Customer.query.filter_by(c_name=data['c_name']).first()
    if not customer:
        return "Customer not found"
    
    staff = Staff.query.filter_by(s_name=data['s_name']).first()
    if not staff:
        return "Staff not found"
    
    item = InventoryItem.query.filter_by(Item_Name=data['Item_Name']).first()
    if not item:
        return "Item not found"

    new_transaction = Transaction(c_ID=customer.c_ID, Item_SKU=item.Item_SKU, s_ID=staff.s_ID, t_Date=data['t_Date'], t_Amount=data['t_Amount'], t_Category=data['t_Category'])
    db.session.add(new_transaction)
    db.session.commit()
    return f"Transaction for item {data['Item_Name']} added successfully"

@app.get('/total_sales')
def get_sales():
    total_sales = db.session.query(db.func.sum(Transaction.t_Amount)).scalar()
    return f"Total sales done are Rs. {total_sales}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)