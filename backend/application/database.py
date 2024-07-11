from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

login_manager = LoginManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

class InventoryItem(db.Model):
    __tablename__ = 'inventoryitem'
    item_sku = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    item_description = db.Column(db.String, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    item_qty = db.Column(db.Integer, nullable=False)

class Customer(db.Model):  
    __tablename__ = 'customer'
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String, nullable=False)
    c_email = db.Column(db.String, nullable=False)
    c_contact = db.Column(db.String, nullable=False)

class Staff(db.Model, UserMixin):  
    __tablename__ = 'staff'
    s_id = db.Column(db.Integer, primary_key=True)
    s_username = db.Column(db.String, nullable=False)
    s_email = db.Column(db.String, nullable=False)
    s_password = db.Column(db.Text, nullable=False)
    s_contact = db.Column(db.String, nullable=False)
    s_isadmin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Staff : {self.s_username}, Admin? : {self.s_isadmin}>'
    
    def get_id(self):
        return str(self.s_id)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    t_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, db.ForeignKey('customer.c_id'), nullable=False)
    item_sku = db.Column(db.Integer, db.ForeignKey('inventoryitem.item_sku'), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('staff.s_id'), nullable=False)
    t_date = db.Column(db.Date, nullable=False)
    t_time = db.Column(db.Time, nullable=False)
    t_amount = db.Column(db.Integer, nullable=False)
