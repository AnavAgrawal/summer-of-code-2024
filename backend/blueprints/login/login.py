from flask import Blueprint, request, render_template, redirect, url_for
from database import db, Staff, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/')
def index():
    return render_template('login/home.html')

@login_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.s_isadmin:
        error = 'You need to login as admin to add new staff'
        return render_template('login/home.html', error=error)

    if request.method == 'GET':
        return render_template('login/register.html')
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        isadmin = request.form['isadmin']
        if isadmin == 'True':
            isadmin = True
        else:
            isadmin = False

        staff = Staff(s_username=username, s_email=email, s_contact=contact, s_password=hashed_password, s_isadmin=isadmin)
        db.session.add(staff)
        db.session.commit()

        login_user(staff)
        return redirect(url_for('login.index'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
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



