# Final Project - Dosa Restaurant REST API

## Overview

In this project, we developed a REST API backend for a dosa restaurant using FastAPI and SQLite. We creating three main entities — customers, items, and orders — and implementing a full CRUD functionality for each of them. The API is designed to interact with an SQLite database (`db.sqlite`) and is initialized using the `init_db.py` script, which populates the database with data from the `example_orders.json` file which we used in the midterm project.

## Features

We included the following core features:

- **Customers**: Create, read, update, and delete customer records.
- **Items**: Create, read, update, and delete menu items.
- **Orders**: Create, read, update, and delete customer orders.

## Endpoints

The API provides the following endpoints for interacting with customers, items, and orders:

| Method | Path           | Description                                                   |
|--------|----------------|---------------------------------------------------------------|
| POST   | /customers      | Creates a customer in the DB given a JSON representation       |
| GET    | /customers/{id} | Retrieves a JSON representation of a customer in the DB       |
| DELETE | /customers/{id} | Deletes a customer in the DB                                   |
| PUT    | /customers/{id} | Updates a customer in the DB given a JSON representation       |
| POST   | /items          | Creates an item in the DB given a JSON representation          |
| GET    | /items/{id}     | Retrieves a JSON representation of an item in the DB          |
| DELETE | /items/{id}     | Deletes an item in the DB                                      |
| PUT    | /items/{id}     | Updates an item in the DB given a JSON representation          |
| POST   | /orders         | Creates an order in the DB given a JSON representation         |
| GET    | /orders/{id}    | Retrieves a JSON representation of an order in the DB         |
| DELETE | /orders/{id}    | Deletes an order in the DB                                     |
| PUT    | /orders/{id}    | Updates an order in the DB given a JSON representation         |

## Technologies Used

- **FastAPI**
- **SQLite**
- **Python 3.12.4**

## Setup Instructions

### 1. Clone the repository

To get started, clone the repository:

```bash
git clone https://github.com/LakshayMunjal-dev/dosa_restaurant_IS601.git
cd dosa_restaurant_IS601
```

### 2. Set up the virtual environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### 3. Install the dependencies

Install the necessary dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

To initialize the database with data, run the `init_db.py` script:

```bash
python init_db.py
```

This will create the `db.sqlite` file and populate it with data from `example_orders.json`.

### 5. Run the FastAPI backend

To start the FastAPI server:

```bash
fastapi dev
```
or 

```bash
uvicorn main:app --reload
```

## Project Structure

- **init_db.py**: Script to initialize the SQLite database using data from `example_orders.json`.
- **main.py**: FastAPI backend for handling API requests and database interactions.
- **db.sqlite**: SQLite database file for storing customer, item, and order data.
- **example_orders.json**: Example data file used for initializing the database.
- **README.md**: Documentation for setting up and using the project.


### Key Sections:
1. **Project Overview**: A concise description of the project and what it involves.
2. **Features**: Highlights the main features of the application.
3. **Endpoints**: Lists all available API endpoints with their methods and descriptions.
4. **Technologies Used**: Specifies the technologies used for the project (FastAPI, SQLite, Python).
5. **Setup Instructions**: Provides a step-by-step guide to setting up the environment, installing dependencies, initializing the database, and running the FastAPI server.
6. **Project Structure**: Describes the project file structure.


