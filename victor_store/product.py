from database import cursor, myBD

def add_product():
    name = input("Enter product name: ")
    
    try:
        price = float(input("Enter product price: ").replace(" ", ""))
    except ValueError:
        print("Invalid price! Please enter a number!")
        return
    
    try:
        stock = int(input("Enter product stock quantity: ").replace(" ", ""))
    except ValueError:
        print("Invalid stock! Please enter a number!")
        return

    cursor.execute("""
        INSERT INTO products (name, price, stock)
        VALUES (%s, %s, %s)
    """, (name, price, stock))

    myBD.commit()
    print(f"{name} has been added successfully!")


def view_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if len(products) == 0:
        print("No products found!")
    else:
        print("\nALL PRODUCTS:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ₦{product[2]}, Stock: {product[3]}")

def update_stock(product_id, quantity):
    cursor.execute("""
        UPDATE products SET stock = stock - %s WHERE id = %s
    """, (quantity, product_id))
    myBD.commit()
    
    
def search_product():
    name = input("Enter product name to search: ")
    
    cursor.execute("SELECT * FROM products WHERE name LIKE %s", ("%" + name + "%",))
    products = cursor.fetchall()
    
    if len(products) == 0:
        print(f"No products found with the name '{name}'!")
    else:
        print(f"\nSEARCH RESULTS FOR '{name.upper()}':")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ₦{product[2]:.2f}, Stock: {product[3]}")
            

def delete_product():
    view_products()
    
    try:
        product_id = int(input("Enter product ID to delete: "))
    except ValueError:
        print("Invalid ID! Please enter a number!")
        return
    
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if product is None:
        print("Product not found!")
        return
    
    confirm = input(f"Are you sure you want to delete {product[1]}? (yes/no): ")
    
    if confirm.lower() == "yes":
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        myBD.commit()
        print(f"{product[1]} has been deleted successfully!")
    else:
        print("Deletion cancelled!")
        
        
def restock_product():
    while True:
        search_name = input("Enter product name to restock: ")
        
        cursor.execute("SELECT * FROM products WHERE name LIKE %s", ("%" + search_name + "%",))
        products = cursor.fetchall()
        
        if len(products) == 0:
            print("No products found! Try again.")
            continue
        
        print("\nMATCHING PRODUCTS:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ₦{product[2]:.2f}, Stock: {product[3]}")
        break
    
    try:
        product_id = int(input("Enter product ID: "))
    except ValueError:
        print("Invalid ID! Please enter a number!")
        return
    
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if product is None:
        print("Product not found!")
        return
    
    try:
        quantity = int(input(f"Enter quantity to add to {product[1]}: ").replace(" ", ""))
    except ValueError:
        print("Invalid quantity! Please enter a number!")
        return
    
    cursor.execute("""
        UPDATE products SET stock = stock + %s WHERE id = %s
    """, (quantity, product_id))
    
    myBD.commit()
    print(f"{product[1]} restocked successfully! New stock: {product[3] + quantity}")


def update_price():
    while True:
        search_name = input("Enter product name to update price: ")
        
        cursor.execute("SELECT * FROM products WHERE name LIKE %s", ("%" + search_name + "%",))
        products = cursor.fetchall()
        
        if len(products) == 0:
            print("No products found! Try again.")
            continue
        
        print("\nMATCHING PRODUCTS:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ₦{product[2]:.2f}, Stock: {product[3]}")
        break
    
    try:
        product_id = int(input("Enter product ID: "))
    except ValueError:
        print("Invalid ID! Please enter a number!")
        return
    
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if product is None:
        print("Product not found!")
        return
    
    print(f"Current price of {product[1]}: ₦{product[2]:.2f}")
    
    try:
        new_price = float(input(f"Enter new price for {product[1]}: ").replace(" ", ""))
    except ValueError:
        print("Invalid price! Please enter a number!")
        return
    
    cursor.execute("""
        UPDATE products SET price = %s WHERE id = %s
    """, (new_price, product_id))
    
    myBD.commit()
    print(f"{product[1]} price updated successfully! New price: ₦{new_price:.2f}")