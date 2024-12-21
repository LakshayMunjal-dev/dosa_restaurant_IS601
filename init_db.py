import sqlite3
import json

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
	id INTEGER PRIMARY KEY,
	name CHAR(64) NOT NULL,
	phone CHAR(10) NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
	id INTEGER PRIMARY KEY,
	name CHAR(64) NOT NULL,
	price REAL NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
	id INTEGER PRIMARY KEY,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	cust_id INT NOT NULL,
    notes TEXT
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS item_list(
    order_id NOT NULL,
    item_id NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
""")

# Open and read the JSON file
with open('example_orders.json', 'r') as file:
    data = json.load(file)

# Go through each order and pull out the customers
customers = {}
for order in data:
    name = order['name']
    phone = order['phone']
    customers[phone] = name

# Insert each customer into the customers table
for (phone, name) in customers.items():
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (name, phone))

# Go through each order items and pull out the unique ones
items = {}
for order in data:
    for item in order['items']:
        name = item['name']
        price = item['price']
        items[name] = price

# Insert each item into the items table
for (name, price) in items.items():
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, price))

# Go through each order and pull out order info
for order in data:
    phone = order['phone']
    timestamp = order['timestamp']
    notes = order['notes']
    res = cursor.execute("SELECT id FROM customers WHERE phone=?;", (phone,))
    cust_id = res.fetchone()[0]
    cursor.execute("INSERT INTO orders (timestamp, cust_id, notes) VALUES (?, ?, ?);", (timestamp, cust_id, notes))
    order_id = cursor.lastrowid
    # add items in the item_list table
    for item in order['items']:
        name = item['name']
        res = cursor.execute("SELECT id FROM items WHERE name=?;", (name,))
        item_id = res.fetchone()[0]
        cursor.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?);", (order_id, item_id))

connection.commit()