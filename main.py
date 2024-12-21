from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

# Pydantic models
class Customer(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class Item(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class Item(BaseModel):
    id: int

class Order(BaseModel):
    cust_id: Optional[int] = None
    items: Optional[List[Item]] = None
    notes: Optional[str] = None

# Database setup
def db_setup():
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

# Create a new customer
@app.post("/customers")
def create_customer(customer: Customer):
    con = db_setup()
    cur = con.cursor()
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
    con.commit()
    con.close()
    return {"message": "Customer created successfully"}

# Get a customer by ID
@app.get("/customers/{id}")
def read_customer(id: int):
    conn = db_setup()
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM customers WHERE id=?", (id,))
    row = res.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {
        "id": row["id"],
        "name": row["name"],
        "phone_no": row["phone"]
    }

# Update customer by ID
@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    con = db_setup()
    cur = con.cursor()
    cur.execute("SELECT * FROM customers WHERE id=?", (id,))
    existing_customer = cur.fetchone()

    if not existing_customer:
        con.close()
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Conditionally update only the fields that were provided in the request body
    if customer.name is not None:
        cur.execute("UPDATE customers SET name=? WHERE id=?", (customer.name, id))
    if customer.phone is not None:
        cur.execute("UPDATE customers SET phone=? WHERE id=?", (customer.phone, id))

    con.commit()
    con.close()
    return {"message": f"Customer with ID {id} updated successfully"}

# Delete customer by ID
@app.delete("/customers/{id}")
def delete_customer(id: int):
    con = db_setup()
    cur = con.cursor()
    cur.execute("SELECT * FROM customers WHERE id=?", (id,))
    customer = cur.fetchone()
    
    if not customer:
        con.close()
        raise HTTPException(status_code=404, detail="Customer not found")
    
    cur.execute("DELETE FROM customers WHERE id=?", (id,))
    con.commit()
    con.close()
    return {"message": "Customer deleted successfully"}

# Create a new item
@app.post("/items")
def create_item(item: Item):
    con = db_setup()
    cur = con.cursor()
    cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    con.commit()
    con.close()
    return {"message": "Item created successfully"}

# Get item by ID
@app.get("/items/{id}")
def read_item(id: int):
    con = db_setup()
    cur = con.cursor()
    cur.execute("SELECT * FROM items WHERE id=?", (id,))
    row = cur.fetchone()
    con.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"id": row["id"], "name": row["name"], "price": row["price"]}

# Update item by ID
@app.put("/items/{id}")
def update_item(id: int, item: Item):
    con = db_setup()
    cur = con.cursor()
    cur.execute("SELECT * FROM items WHERE id=?", (id,))
    existing_item = cur.fetchone()

    if not existing_item:
        con.close()
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Conditionally update only the fields that were provided in the request body
    if item.name is not None:
        cur.execute("UPDATE items SET name=? WHERE id=?", (item.name, id))
    if item.price is not None:
        cur.execute("UPDATE items SET price=? WHERE id=?", (item.price, id))

    con.commit()
    con.close()
    return {"message": f"Item with ID {id} updated successfully"}

# Delete item by ID
@app.delete("/items/{id}")
def delete_item(id: int):
    con = db_setup()
    cur = con.cursor()
    cur.execute("SELECT * FROM items WHERE id=?", (id,))
    item = cur.fetchone()

    if not item:
        con.close()
        raise HTTPException(status_code=404, detail="Item not found")
    
    cur.execute("DELETE FROM items WHERE id=?", (id,))
    con.commit()
    con.close()
    return {"message": "Item deleted successfully"}

# Create a new order
@app.post("/orders")
def create_order(order: Order):
    con = db_setup()
    cur = con.cursor()

    cur.execute("SELECT id FROM customers WHERE id=?", (order.cust_id,))
    customer = cur.fetchone()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    cur.execute("INSERT INTO orders (cust_id, notes) VALUES (?, ?)", (order.cust_id, order.notes))
    order_id = cur.lastrowid

    # Insert the items into the item_list table using item_id
    for item in order.items:
        cur.execute("SELECT id, price FROM items WHERE id=?", (item.id,))
        item_record = cur.fetchone()

        if item_record:
            cur.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?)", (order_id, item.id))
        else:
            raise HTTPException(status_code=404, detail=f"Item with ID '{item.id}' not found")

    con.commit()
    con.close()
    return {"message": "Order created successfully"}

@app.get("/orders/{id}")
def read_order(id: int):
    con = db_setup()
    cur = con.cursor()

    cur.execute("""
        SELECT orders.id, orders.cust_id, orders.timestamp, orders.notes, customers.name, customers.phone
        FROM orders
        JOIN customers ON orders.cust_id = customers.id
        WHERE orders.id = ?
    """, (id,))
    
    row = cur.fetchone()

    if not row:
        con.close()
        raise HTTPException(status_code=404, detail="Order not found")


    cur.execute("""
        SELECT items.name, items.price
        FROM items
        JOIN item_list ON items.id = item_list.item_id
        WHERE item_list.order_id = ?
    """, (id,))
    
    items = cur.fetchall()
    item_list = [{"name": item["name"], "price": item["price"]} for item in items]

    con.close()
    return {
        "id": row["id"],
        "cust_id": row["cust_id"],
        "timestamp": row["timestamp"],
        "notes": row["notes"],
        "customer": {
            "name": row["name"],
            "phone": row["phone"]
        },
        "items": item_list
    }

# Update order by ID
@app.put("/orders/{id}")
def update_order(id: int, order: Order):
    con = db_setup()
    cur = con.cursor()
    cur.execute("SELECT * FROM orders WHERE id=?", (id,))
    existing_order = cur.fetchone()

    if not existing_order:
        con.close()
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Conditionally update only the fields that were provided in the request body
    if order.notes is not None:
        cur.execute("UPDATE orders SET notes=? WHERE id=?", (order.notes, id))
    
    if order.cust_id is not None:
        cur.execute("UPDATE orders SET cust_id=? WHERE id=?", (order.cust_id, id))
    
    if order.items is not None:
        # For simplicity, let's assume we're updating items completely here, 
        # you can adjust as needed (like appending/removing items)
        cur.execute("DELETE FROM item_list WHERE order_id=?", (id,))
        for item in order.items:
            cur.execute("SELECT id, price FROM items WHERE id=?", (item.id,))
            item_record = cur.fetchone()

            if item_record:
                cur.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?)", (id, item.id))
            else:
                raise HTTPException(status_code=404, detail=f"Item with ID '{item.id}' not found")

    con.commit()
    con.close()
    return {"message": f"Order with ID {id} updated successfully"}

# Delete order by ID
@app.delete("/orders/{id}")
def delete_order(id: int):
    con = db_setup()
    cur = con.cursor()
    cur.execute("SELECT * FROM orders WHERE id=?", (id,))
    order = cur.fetchone()

    if not order:
        con.close()
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Delete the order
    cur.execute("DELETE FROM orders WHERE id=?", (id,))
    con.commit()
    con.close()
    return {"message": "Order deleted successfully"}
