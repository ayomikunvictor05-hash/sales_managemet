from database import cursor, myBD
from datetime import datetime
from product import update_stock



def make_order():
    while True:
        search_name = input("Enter customer name: ")
        
        cursor.execute("SELECT * FROM customers WHERE name LIKE %s", ("%" + search_name + "%",))
        customers = cursor.fetchall()
        
        if len(customers) == 0:
            print("No customers found! Try again.")
            continue
        
        print("\nMATCHING CUSTOMERS:")
        for customer in customers:
            print(f"ID: {customer[0]}, Name: {customer[1]}, Phone: {customer[2]}")
        break
    
    try:
        customer_id = int(input("\nEnter customer ID: "))
    except ValueError:
        print("Invalid ID! Please enter a number!")
        return
    
    cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()
    
    if customer is None:
        print("Customer not found!")
        return
    
    print(f"\nHello {customer[1]}! Let's create your order.")
    
    order_items = []
    subtotal_total = 0
    
    while True:
        while True:
            search_product_name = input("\nEnter product name to order (or 'done' to stop): ")
            
            if search_product_name.lower() == "done":
                break
            
            cursor.execute("SELECT * FROM products WHERE name LIKE %s", ("%" + search_product_name + "%",))
            products = cursor.fetchall()
            
            if len(products) == 0:
                print("No products found! Try again.")
                continue
            
            print("\nMATCHING PRODUCTS:")
            for product in products:
                print(f"ID: {product[0]}, Name: {product[1]}, Price: ₦{product[2]:.2f}, Stock: {product[3]}")
            break
        
        if search_product_name.lower() == "done":
            break
        
        try:
            product_id = int(input("Enter product ID: "))
        except ValueError:
            print("Invalid ID! Please enter a number!")
            continue
        
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        
        if product is None:
            print("Product not found!")
            continue
        
        try:
            quantity = int(input(f"Enter quantity for {product[1]}: "))
        except ValueError:
            print("Invalid quantity! Please enter a number!")
            continue
        
        if quantity > product[3]:
            print(f"Sorry! Only {product[3]} units available in stock!")
            continue
        
        subtotal = product[2] * quantity
        subtotal_total += subtotal
        order_items.append((product_id, quantity, subtotal))
        print(f"{product[1]} x {quantity} = ₦{subtotal:.2f} added to order!")
    
    if len(order_items) == 0:
        print("No items added to order!")
        return
    
    print(f"\nSubtotal: ₦{subtotal_total:.2f}")
    
    try:
        discount = float(input("Enter discount percentage (0 if none): "))
        tax = float(input("Enter tax percentage (0 if none): "))
    except ValueError:
        print("Invalid discount or tax! Please enter a number!")
        return
    
    discount_amount = subtotal_total * (discount / 100)
    tax_amount = (subtotal_total - discount_amount) * (tax / 100)
    total = subtotal_total - discount_amount + tax_amount
    
    print(f"Discount: ₦{discount_amount:.2f}")
    print(f"Tax: ₦{tax_amount:.2f}")
    print(f"Total: ₦{total:.2f}")
    
    cursor.execute("""
        INSERT INTO orders (customer_id, date, discount, tax, total)
        VALUES (%s, %s, %s, %s, %s)
    """, (customer_id, datetime.now(), discount, tax, total))
    
    myBD.commit()
    order_id = cursor.lastrowid
    
    for item in order_items:
        cursor.execute("""
            INSERT INTO orderitems (order_id, product_id, quantity, subtotal)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item[0], item[1], item[2]))
        update_stock(item[0], item[1])
    
    myBD.commit()
    print_receipt(order_id, customer[1], order_items, subtotal_total, discount_amount, tax_amount, total, discount, tax)

    
    
def view_order_history():
    try:
        customer_id = int(input("Enter customer ID: "))
    except ValueError:
        print("Invalid ID! Please enter a number!")
        return
    
    cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()
    
    if customer is None:
        print("Customer not found!")
        return
    
    cursor.execute("""
        SELECT orders.id, orders.date, orders.discount, orders.tax, orders.total
        FROM orders
        WHERE orders.customer_id = %s
    """, (customer_id,))
    
    orders = cursor.fetchall()
    
    if len(orders) == 0:
        print(f"No orders found for {customer[1]}!")
        return
    
    print(f"\nORDER HISTORY FOR {customer[1].upper()}:")
    for order in orders:
        print(f"\nOrder ID: {order[0]}, Date: {order[1]}, Discount: {order[2]}%, Tax: {order[3]}%, Total: ₦{order[4]:.2f}")
        
        cursor.execute("""
            SELECT products.name, orderitems.quantity, orderitems.subtotal
            FROM orderitems
            JOIN products ON orderitems.product_id = products.id
            WHERE orderitems.order_id = %s
        """, (order[0],))
        
        items = cursor.fetchall()
        print("Items:")
        for item in items:
            print(f"  - {item[0]} x {item[1]} = ₦{item[2]:.2f}")
            
           

def monthly_revenue():
    month_names = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12
    }
    
    month = input("Enter month (e.g. March or 03): ").strip().lower()
    year = input("Enter year (YYYY): ").strip()
    
    if month in month_names:
        month = month_names[month]
    elif month.isdigit():
        month = int(month)
    else:
        print("Invalid month! Please enter a month name or number!")
        return
    
    if not year.isdigit():
        print("Invalid year! Please enter a valid year!")
        return
    
    cursor.execute("""
        SELECT SUM(total), COUNT(id)
        FROM orders
        WHERE MONTH(date) = %s AND YEAR(date) = %s
    """, (month, int(year)))
    
    result = cursor.fetchone()
    
    if result[0] is None:
        print(f"No orders found for {month}/{year}!")
    else:
        print(f"\nMONTHLY REVENUE FOR {month}/{year}:")
        print(f"Total Revenue: ₦{result[0]:.2f}")
        print(f"Total Orders: {result[1]}")        

def view_all_orders():
    cursor.execute("""
        SELECT orders.id, customers.name, orders.date, orders.total
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
    """)
    
    orders = cursor.fetchall()
    
    if len(orders) == 0:
        print("No orders found!")
        return
    
    print("\nALL ORDERS:")
    for order in orders:
        print(f"Order ID: {order[0]}, Customer: {order[1]}, Date: {order[2]}, Total: ₦{order[3]:.2f}")
        
        


def print_receipt(order_id, customer_name, order_items, subtotal_total, discount_amount, tax_amount, total, discount, tax):
    print("\n")
    print("         VICTOR STORE")
    print("")
    print(f"  Order ID: {order_id}")
    print(f"  Customer: {customer_name}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("_______________________________________________")
    
    for item in order_items:
        cursor.execute("SELECT name FROM products WHERE id = %s", (item[0],))
        product = cursor.fetchone()
        print(f"  {product[0]} x {item[1]}        ₦{item[2]:.2f}")
    
    print("_______________________________________________")
    print(f"  Subtotal:          ₦{subtotal_total:.2f}")
    print(f"  Discount ({discount}%):      ₦{discount_amount:.2f}")
    print(f"  Tax ({tax}%):           ₦{tax_amount:.2f}")
    print("_______________________________________________")
    print(f"  TOTAL:             ₦{total:.2f}")
    print("")
    print("     Thank you for your patronage!")
    print("\n")


