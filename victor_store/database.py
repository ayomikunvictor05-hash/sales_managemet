import mysql.connector
from datetime import datetime


myBD = mysql.connector.connect(
    host ="localhost",
    user = "root",
    password = "oludunke25",
    database = "victor_store",
    auth_plugin = "mysql_native_password"
)

# connect = myBD.cursor()
# connect.execute("CREATE DATABASE Victor_store")

cursor = myBD.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20),
        email VARCHAR(100)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        price FLOAT,
        stock INT
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        date DATETIME,
        discount FLOAT,
        tax FLOAT,
        total FLOAT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orderitems (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_id INT,
        quantity INT,
        subtotal FLOAT,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")


