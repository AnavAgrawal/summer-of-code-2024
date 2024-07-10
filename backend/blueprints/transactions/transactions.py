from flask import Blueprint, render_template, before_request, redirect, url_for, flash, request
from flask_login import current_user
from database import db, Transaction

transactions = Blueprint('transactions', __name__, template_folder='templates')

# Check if user is logged in before accessing any routes
@before_request
def before_request():
    if not current_user.is_authenticated:
        flash('You are not logged in.', 'warning')
        return redirect(url_for('login.login'))

@transactions.route('/')
def home():
    transactions = Transaction.query.all()
    return render_template('transactions/home.html', transactions=transactions)

@transactions.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template('transactions/add_transaction.html')
    
@transactions.route('/update_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def update_transaction(transaction_id, methods=['GET', 'POST']):
    return render_template('transactions/update_transaction.html', transaction_id=transaction_id)

