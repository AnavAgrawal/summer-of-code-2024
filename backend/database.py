from flask_sqlalchemy import SQLAlchemy

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

class Staff(db.Model):  
    __tablename__ = 'staff'
    s_id = db.Column(db.Integer, primary_key=True)
    s_username = db.Column(db.String, nullable=False)
    s_email = db.Column(db.String, nullable=False)
    s_password = db.Column(db.Text, nullable=False)
    s_contact = db.Column(db.String, nullable=False)
    s_isadmin = db.Column(db.Boolean, nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    t_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, db.ForeignKey('customer.c_id'), nullable=False)
    item_sku = db.Column(db.Integer, db.ForeignKey('inventoryitem.item_sku'), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('staff.s_id'), nullable=False)
    t_date = db.Column(db.Date, nullable=False)
    t_amount = db.Column(db.Integer, nullable=False)
    t_category = db.Column(db.String, nullable=False)
