from flask import Blueprint, request, render_template, redirect, url_for
from database import db, Staff
from flask_login import current_user

staff_bp = Blueprint('staff', __name__, template_folder='templates')

# Check if user is logged in before accessing any routes
@staff_bp.before_request
def before_request():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

@staff_bp.route('/')
def home():
    staff_members = Staff.query.all()
    return render_template('staff/home.html', staff_members=staff_members)

@staff_bp.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'GET':
        return render_template('staff/add_staff.html')
    if request.method == 'POST':
        data = request.form
        new_staff = Staff(s_username=data['s_username'], s_email=data['s_email'], s_contact=data['s_contact'], s_password=data['s_password'], s_isadmin=data['s_isadmin'])
        db.session.add(new_staff)
        db.session.commit()
        return redirect(url_for('staff.home'))

@staff_bp.route('/update_staff/<int:staff_id>', methods=['GET', 'POST'])
def update_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if request.method == 'POST':
        staff.s_username = request.form['s_username']
        staff.s_email = request.form['s_email']
        staff.s_contact = request.form['s_contact']
        staff.s_password = request.form['s_password']
        staff.s_isadmin = request.form['s_isadmin']
        db.session.commit()
        return redirect(url_for('staff.home'))
    return render_template('staff/update_staff.html', staff=staff)

@staff_bp.route('/delete_staff/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    db.session.delete(staff)
    db.session.commit()
    return redirect(url_for('staff.home'))