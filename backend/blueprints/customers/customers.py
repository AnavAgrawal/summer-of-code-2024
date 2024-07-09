from flask import Blueprint, request, render_template, redirect, url_for
from database import db, Customer
from flask_login import current_user

customers_bp = Blueprint('customers', __name__, template_folder='templates')

# Check if user is logged in before accessing any routes
@customers_bp.before_request
def before_request():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

@customers_bp.route('/')
def home():
    customers = Customer.query.all()
    return render_template('customers/home.html', customers=customers)

@customers_bp.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'GET':
        return render_template('customers/add_customer.html')
    if request.method == 'POST':
        data = request.form
        new_customer = Customer(c_name=data['c_name'], c_email=data['c_email'], c_contact=data['c_contact'])
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('customers.home'))

@customers_bp.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if request.method == 'POST':
        customer.c_name = request.form['c_name']
        customer.c_email = request.form['c_email']
        customer.c_contact = request.form['c_contact']
        db.session.commit()
        return redirect(url_for('customers.home'))
    return render_template('customers/update_customer.html', customer=customer)

@customers_bp.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customers.home'))
