from database import cursor, myBD
from order import make_order, view_order_history, monthly_revenue, view_all_orders
from customers import add_customer, view_customers, delete_customer
from product import add_product, view_products, search_product, delete_product, restock_product, update_price


while True:
    print("\nSALES MANAGEMENT SYSTEM")
    print("1. Add customer")
    print("2. View all customers")
    print("3. Add product")
    print("4. View all products")
    print("5. Make an order")
    print("6. View order history for a customer")
    print("7. View monthly revenue")
    print("8. View all orders")
    print("9. Search product by name")
    print("10. Delete customer")
    print("11. Delete product")
    print("12. Restock product")
    print("13. Update product price")
    print("14. Exit")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        add_customer()
    elif choice == "2":
        view_customers()
    elif choice == "3":
        add_product()
    elif choice == "4":
        view_products()
    elif choice == "5":
        make_order()
    elif choice == "6":
        view_order_history()
    elif choice == "7":
        monthly_revenue()
    elif choice == "8":
        view_all_orders()
    elif choice == "9":
        search_product()    
    elif choice == "10":
        delete_customer()
    elif choice == "11":
        delete_product()
    elif choice == "12":
        restock_product()
    elif choice == "13":
        update_price()
    elif choice == "14":
        print("Goodbye!")
        cursor.close()
        myBD.close()
        break
