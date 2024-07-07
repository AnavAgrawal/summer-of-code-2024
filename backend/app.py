from flask import Flask, request
import psycopg2
import dotenv
import os
import hashlib
from products import products_bp

# get url from .env file
dotenv.load_dotenv()
url = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.register_blueprint(products_bp, url_prefix='/products')
conn = psycopg2.connect(url)

with conn:
    with conn.cursor() as cur:
        # Create InventoryItem Table
        cur.execute("CREATE TABLE IF NOT EXISTS InventoryItem (Item_SKU SERIAL PRIMARY KEY, Item_Name VARCHAR, Item_Description VARCHAR, Item_Price INT, Item_Qty INT);")

        # Create Customer Table
        cur.execute("CREATE TABLE IF NOT EXISTS Customer (c_ID SERIAL PRIMARY KEY, c_name VARCHAR, c_email VARCHAR, c_contact VARCHAR);")

        # Create Staff Table
        cur.execute("CREATE TABLE IF NOT EXISTS Staff (s_ID SERIAL PRIMARY KEY, s_name VARCHAR, s_email VARCHAR, s_isAdmin BOOLEAN, s_contact VARCHAR, pass_hash TEXT);")

        # Create Transaction Table
        cur.execute("CREATE TABLE IF NOT EXISTS Transaction (t_ID SERIAL PRIMARY KEY, c_ID INT REFERENCES Customer(c_ID), Item_SKU INT REFERENCES InventoryItem(Item_SKU), s_ID INT REFERENCES Staff(s_ID), t_Date DATE, t_Amount INT, t_Category VARCHAR);")
        
@app.get('/')
def get_inventory():
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM InventoryItem;")
            inventory = cur.fetchall()
            return str(inventory)
        
# @app.post('/add_item')
# def add_item():
#     data = request.json
#     with conn:
#         with conn.cursor() as cur:
#             cur.execute("INSERT INTO InventoryItem (Item_Name, Item_Description, Item_Price, Item_Qty) VALUES (%s, %s, %s, %s);", (data['Item_Name'], data['Item_Description'], data['Item_Price'], data['Item_Qty']))
#             return (f"Item named {data['Item_Name']} added successfully")
        
@app.post('/add_customer')
def add_customer():
    data = request.json
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Customer (c_name, c_email, c_contact) VALUES (%s, %s, %s);", (data['c_name'], data['c_email'], data['c_contact']))
            return (f"Customer named {data['c_name']} added successfully")
        
@app.post('/add_staff')
def add_staff():
    data = request.json

    # Calculate hash of the password
    pass_hash = hashlib.sha256(data['password'].encode()).hexdigest()

    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Staff (s_name, s_email, s_isAdmin, s_contact, pass_hash) VALUES (%s, %s, %s, %s, %s);", (data['s_name'], data['s_email'], data['s_isAdmin'], data['s_contact'], pass_hash))
            return (f"Staff named {data['s_name']} added successfully")
        
@app.post('/add_transaction')
def add_transaction():
    data = request.json
    with conn:
        with conn.cursor() as cur:

            cur.execute("SELECT c_ID FROM Customer WHERE c_name = %s;", (data['c_name'],))
            c_ID = cur.fetchone()[0]
            if c_ID is None:
                return "Customer not found"
            
            cur.execute("SELECT s_ID FROM Staff WHERE s_name = %s;", (data['s_name'],))
            s_ID = cur.fetchone()[0]
            if s_ID is None:
                return "Staff not found"
            
            cur.execute("SELECT Item_SKU FROM InventoryItem WHERE Item_Name = %s;", (data['Item_Name'],))
            Item_SKU = cur.fetchone()[0]
            if Item_SKU is None:
                return "Item not found"

            cur.execute("INSERT INTO Transaction (c_ID, Item_SKU, s_ID, t_Date, t_Amount, t_Category) VALUES (%s, %s, %s, %s, %s, %s);", (c_ID, Item_SKU, s_ID, data['t_Date'], data['t_Amount'], data['t_Category']))
            return (f"Transaction for item {data['Item_Name']} added successfully")

@app.get('/total_sales')
def get_sales():
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(t_Amount) FROM Transaction;")
            total_sales = cur.fetchone()
            return f"Total sales done are Rs. {str(total_sales[0])}"


if __name__ == '__main__':
    app.run(debug=True)