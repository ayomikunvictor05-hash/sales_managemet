from database import cursor, myBD

def add_customer():
    name = input("Enter customer name: ").strip()
    phone = input("Enter customer phone number: ").strip()
    email = input("Enter customer email: ").strip()

    cursor.execute("""
        INSERT INTO customers (name, phone, email)
        VALUES (%s, %s, %s)
    """, (name, phone, email))

    myBD.commit()
    print(f"{name} has been added successfully!")

def view_customers():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    if len(customers) == 0:
        print("No customers found!")
    else:
        print("\nALL CUSTOMERS:")
        for customer in customers:
            print(f"ID: {customer[0]}, Name: {customer[1]}, Phone: {customer[2]}, Email: {customer[3]}")
            

def delete_customer():
    view_customers()
    
    try:
        customer_id = int(input("Enter customer ID to delete: "))
    except ValueError:
        print("Invalid ID! Please enter a number!")
        return
    
    cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()
    
    if customer is None:
        print("Customer not found!")
        return
    
    confirm = input(f"Are you sure you want to delete {customer[1]}? (yes/no): ")
    
    if confirm.lower() == "yes":
        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        myBD.commit()
        print(f"{customer[1]} has been deleted successfully!")
    else:
        print("Deletion cancelled!")