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

