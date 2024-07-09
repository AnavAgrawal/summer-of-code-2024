from flask import Flask, request
import dotenv
import os
from database import login_manager, bcrypt, db, InventoryItem, Customer, Staff, Transaction
from blueprints.products.products import products_bp
from blueprints.login.login import login_bp
from blueprints.customers.customers import customers_bp
from blueprints.staff.staff import staff_bp

def create_app():
    app = Flask(__name__)
    
    # get url from .env file
    dotenv.load_dotenv()
    url = os.getenv('DATABASE_URL')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SECRET_KEY'] = 'secret'
    app.config['EXPLAIN_TEMPLATE_LOADING'] = True

    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
        
    @login_manager.user_loader
    def load_user(user_id):
        return Staff.query.get(int(user_id))

    app.register_blueprint(login_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    
    return app

def setup_db(app):

    with app.app_context():
        db.create_all()

app = create_app()

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
    pass_hash = bcrypt.generate_password_hash(data['s_password']).decode('utf-8')
    new_staff = Staff(s_username=data['s_username'], s_email=data['s_email'], s_isadmin=data['s_isadmin'], s_contact=data['s_contact'], s_password=pass_hash)
    db.session.add(new_staff)
    db.session.commit()
    return f"Staff with username {data['s_username']} added successfully"

@app.post('/add_transaction')
def add_transaction():
    data = request.json
    customer = Customer.query.filter_by(c_name=data['c_name']).first()
    if not customer:
        return "Customer not found"
    
    staff = Staff.query.filter_by(s_name=data['s_name']).first()
    if not staff:
        return "Staff not found"
    
    item = InventoryItem.query.filter_by(item_name=data['Item_Name']).first()
    if not item:
        return "Item not found"

    new_transaction = Transaction(c_id=customer.c_id, item_sku=item.item_sku, s_id=staff.s_id, t_date=data['t_date'], t_amount=data['t_amount'], t_category=data['t_category'])
    db.session.add(new_transaction)
    db.session.commit()
    return f"Transaction for item {data['Item_Name']} added successfully"

@app.get('/total_sales')
def get_sales():
    total_sales = db.session.query(db.func.sum(Transaction.t_amount)).scalar()
    return f"Total sales done are Rs. {total_sales}"

if __name__ == '__main__':
    setup_db(app)
    app.run(debug=True)