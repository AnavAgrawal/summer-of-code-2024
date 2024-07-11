from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from database import db, Transaction, InventoryItem, Customer, Staff

transactions_bp = Blueprint('transactions', __name__, template_folder='templates')

# Check if user is logged in before accessing any routes
@transactions_bp.before_request
def before_request():
    if not current_user.is_authenticated:
        flash('You are not logged in.', 'warning')
        return redirect(url_for('login.login'))

@transactions_bp.route('/')
def home():
    transactions = Transaction.query.all()
    transactions_data = [
        {
            'transaction': transaction,
            'customer': Customer.query.get(transaction.c_id),
            'staff': Staff.query.get(transaction.s_id),
            'item': InventoryItem.query.get(transaction.item_sku)
        } for transaction in transactions
    ]

    return render_template('transactions/home.html', transactions_data=transactions_data)

@transactions_bp.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        items = InventoryItem.query.all()
        customers = Customer.query.all()
        return render_template('transactions/add_transaction.html', items=items, customers=customers)
    if request.method == 'POST':
        data = request.form
        
        transaction = Transaction(
            c_id = data['c_id'],
            s_id = current_user.s_id,
            item_sku = data['item_sku'],
            t_date=data['t_date'],
            t_time=data['t_time'],
            t_amount=data['t_amount'],
        )

        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transactions.home'))

@transactions_bp.route('/update_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def update_transaction(transaction_id, methods=['GET', 'POST']):
    transaction = Transaction.query.get(transaction_id)
    items = InventoryItem.query.all()
    customers = Customer.query.all()

    if request.method == 'POST':
        data = request.form
        transaction.c_id = data['c_id']
        # transaction.s_id = current_user.s_id
        transaction.item_sku = data['item_sku']
        transaction.t_date = data['t_date']
        transaction.t_time = data['t_time']
        transaction.t_amount = data['t_amount']

        db.session.commit()
        return redirect(url_for('transactions.home'))
    return render_template('transactions/update_transaction.html', transaction=transaction, items=items, customers=customers)

# delete transaction
@transactions_bp.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('transactions.home'))
