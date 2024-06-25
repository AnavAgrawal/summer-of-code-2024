from flask import Flask, request
import psycopg2
import dotenv
import os

# get url from .env file
dotenv.load_dotenv()
url = os.getenv('DATABASE_URL')

app = Flask(__name__)
conn = psycopg2.connect(url)

with conn:
    with conn.cursor() as cur:
        # Create InventoryItem Table
        cur.execute("CREATE TABLE IF NOT EXISTS InventoryItem (Item_SKU SERIAL PRIMARY KEY, Item_Name VARCHAR, Item_Description VARCHAR, Item_Price INT, Item_Qty INT);")

        # Create Customer Table
        cur.execute("CREATE TABLE IF NOT EXISTS Customer (c_ID SERIAL PRIMARY KEY, c_name VARCHAR, c_email VARCHAR, c_contact VARCHAR);")

        # Create Staff Table
        cur.execute("CREATE TABLE IF NOT EXISTS Staff (s_ID SERIAL PRIMARY KEY, s_name VARCHAR, s_email VARCHAR, s_isAdmin BOOLEAN, s_contact VARCHAR);")

        # Create Transaction Table
        cur.execute("CREATE TABLE IF NOT EXISTS Transaction (t_ID SERIAL PRIMARY KEY, c_ID INT REFERENCES Customer(c_ID), Item_SKU INT REFERENCES InventoryItem(Item_SKU), s_ID INT REFERENCES Staff(s_ID), t_Date DATE, t_Amount INT, t_Category VARCHAR);")
        
@app.get('/')
def get_inventory():
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM InventoryItem;")
            inventory = cur.fetchall()
            return str(inventory)
        
@app.post('/add_item')
def add_item():
    data = request.json
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO InventoryItem (Item_Name, Item_Description, Item_Price, Item_Qty) VALUES (%s, %s, %s, %s);", (data['Item_Name'], data['Item_Description'], data['Item_Price'], data['Item_Qty']))
            return (f"Item named {data['Item_Name']} added successfully")
        
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
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Staff (s_name, s_email, s_isAdmin, s_contact) VALUES (%s, %s, %s, %s);", (data['s_name'], data['s_email'], data['s_isAdmin'], data['s_contact']))
            return (f"Staff named {data['s_name']} added successfully")
        
@app.post('/add_transaction')
def add_transaction():
    data = request.json
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Transaction (c_ID, Item_SKU, s_ID, t_Date, t_Amount, t_Category) VALUES (%s, %s, %s, %s, %s, %s);", (data['c_ID'], data['Item_SKU'], data['s_ID'], data['t_Date'], data['t_Amount'], data['t_Category']))
            cur.execute("SELECT Item_Name from InventoryItem WHERE Item_SKU = %s;", (data['Item_SKU'],))
            item_name = cur.fetchone()
            return (f"Transaction for item {item_name[0]} added successfully")

@app.get('/total_sales')
def get_sales():
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(t_Amount) FROM Transaction;")
            total_sales = cur.fetchone()
            return f"Total sales done are Rs.{str(total_sales[0])}"


if __name__ == '__main__':
    app.run(debug=True)