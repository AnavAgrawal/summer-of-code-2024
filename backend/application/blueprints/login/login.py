from flask import Blueprint, request, render_template, redirect, url_for, flash
from database import db, Staff, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))
    return render_template('login/home.html')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('login.index'))
    if request.method == 'GET':
        return render_template('login/login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        staff = Staff.query.filter_by(s_username=username).first()
        if staff and bcrypt.check_password_hash(staff.s_password, password):
            login_user(staff)
            return redirect(url_for('login.index'))
        else:
            return render_template('login/login.html', error='Invalid username or password')
    
@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))



