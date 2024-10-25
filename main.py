import sys
import logging

import db_connection
from service.userService import UserService
from service.productService import ProductService
from service.ordersService import OrdersService

# Configure logging
logging.basicConfig(
    filename='store_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def admin_menu():
    action = None
    while True:
        print("\nAdmin Menu:")
        print("1. See All Users")
        print("2. Delete User")
        print("3. See All Products")
        print("4. Add Product")
        print("5. Update Product")
        print("6. Delete Product")
        print("7. See All Orders")
        print("8. Update Order")
        print("9. Delete Order")
        print("R. Grant/Revoke admin role")
        print("E. Logout")

        action = input("Input: ")
        if action not in "123456789RrEe" or len(action)!=1:
            print("I don't know how to do this")
            continue
        else:
            return action
        
def user_menu():
    action = None
    while True:
        print("\nUser Menu:")
        print("1. See All Products")
        print("2. Place Order")
        print("3. See All Orders")
        print("4. Update Order")
        print("5. Delete Order")
        print("E. Logout")

        action = input("Input: ")
        if action not in "12345Ee" or len(action)!=1:
            print("I don't know how to do this")
            continue
        else:
            return action

# Establish connection
connection = db_connection.create_connection()

if connection == None:
    logging.error("Failed to connect to the database.")
    sys.exit(1)

logging.info("Connected to the database successfully.")

user_service = UserService(connection)
product_service = ProductService(connection)
orders_service = OrdersService(connection)

while True:
    print("Welcome to the Store Application!")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    user = None
    action=input("Input: ")
    if action not in "123" or len(action)!=1:
        print("I don't know how to do this")
        continue
    if action == '1':
        username = input("Username: ")
        password = input("Password: ")
        user_service.register(username, password)
        logging.info(f"User '{username}' registered successfully.")
    elif action == '2':
        username = input("Username: ")
        password = input("Password: ")
        user = user_service.login(username, password)
        if user:
            logging.info(f"User '{username}' logged in successfully with role '{user['role']}'.")
        else:
            logging.warning(f"Failed login attempt for user '{username}'.")
    elif action == '3':
        logging.info("Application exited by the user.")
        sys.exit(1)

    if user != None:
        break

while True:
    if user['role'] == 'admin':
        action = admin_menu()
        if action == '1':
            # Call function to display all users
            user_service.get_all_users()
            logging.info("Admin viewed all users.")
        elif action == '2':
            # Call function to delete a user
            print("Username to delete")
            action=input("Input: ")
            user_service.delete_user(action)
            logging.info(f"Admin deleted user '{username}'.")
        elif action == '3':
            # Call function to display all products
            product_service.get_all_products()
            logging.info("Admin viewed all products.")
        elif action == '4':
            # Call function to add a product
            try:
                print("Enter product Name:")
                name = input("Input: ")
                print("Enter product Description:")
                description = input("Input: ")
                print("Enter product Price:")
                price = float(input("Input: "))
                print("Enter product Stock:")
                stock = int(input("Input: "))
                product_service.add_product(name, description, price, stock)
                logging.info(f"Admin added product '{name}'.")
            except ValueError:
                print("Invalid input.")
                logging.error("Invalid input while adding a product.")
        elif action == '5':
            # Call function to update a product
            try:
                print("Enter product ID:")
                id = int(input("Input: "))
                print("Enter product Name:")
                name = input("Input: ")
                print("Enter product Description:")
                description = input("Input: ")
                print("Enter product Price:")
                price = float(input("Input: "))
                print("Enter product Stock:")
                stock = int(input("Input: "))
                product_service.update_product(id, name, description, price, stock)
                logging.info(f"Admin updated product with ID '{id}'.")
            except ValueError:
                print("Invalid input.")
                logging.error("Invalid input while updating a product.")
        elif action == '6':
            # Call function to delete a product
            try:
                print("Enter product ID:")
                id = int(input("Input: "))
                product_service.delete_product(id)
                logging.info(f"Admin deleted product with ID '{id}'.")
            except ValueError:
                print("Invalid input.")
                logging.error("Invalid input while deleting a product.")
        elif action == '7':
            # Call function to display all orders
            orders_service.get_all_orders()
            logging.info("Admin viewed all orders.")
        elif action == '8':
            # Call function to update an order
            try:
                print("Enter order ID:")
                order_id = int(input("Input: "))
                print("Enter new quantity:")
                new_quantity = int(input("Input: "))
                if new_quantity < 1:
                    print("Wrong quantity")
                    continue
                orders_service.update_order(order_id, user, new_quantity)
                logging.info(f"Admin updated order with ID '{order_id}'.")
            except ValueError:
                print("Invalid input.")
                logging.error("Invalid input while updating an order.")
        elif action == '9':
            # Call function to delete an order
            try:
                print("Enter order ID:")
                order_id = int(input("Input: "))
                orders_service.delete_order(order_id, user)
                logging.info(f"Admin deleted order with ID '{order_id}'.")
            except ValueError:
                print("Invalid input.")
                logging.error("Invalid input while deleting an order.")
        elif action == 'R' or action == 'r':
            #Grant/Revoke admin role
            print("Enter Username")
            username = input("Input: ")
            userR = user_service.get_user(username)
            if userR == None:
                logging.warning(f"Attempt to change role of a non-existent user '{username}'.")
                continue
            if userR['role'] == 'admin':
                user_service.update_user(userR['username'], userR['username'], userR['password'], 'user')
                logging.info(f"Admin revoked admin privileges from user '{username}'.")
            elif userR['role'] == 'user':
                user_service.update_user(userR['username'], userR['username'], userR['password'], 'admin')
                logging.info(f"Admin granted admin privileges to user '{username}'.")
        elif action == 'E' or action == 'e':
            print("Logging out...")
            logging.info("Admin logged out.")
            break

 #---------------- user ------------------
    if user['role'] == 'user':
        action = user_menu()
        if action == '1':
            # Display all products
            product_service.get_all_products()
            logging.info(f"User '{user['username']}' viewed all products.")
        elif action == '2':
            # Place an order
            try:
                print("Enter product ID:")
                product_id = int(input("Input: "))
                print("Enter quantity:")
                quantity = int(input("Input: "))
                if quantity < 1:
                    print("Wrong quantity")
                    continue
                orders_service.place_order(user['id'], product_id, quantity)
                logging.info(f"User '{user['username']}' placed an order for product ID '{product_id}' with quantity '{quantity}'.")
            except ValueError:
                print("Invalid input.")
                logging.error("Failed to place order due to invalid input.")
        elif action == '3':
            # Display all orders for the user
            orders_service.get_user_orders(user['id'])
            logging.info(f"User '{user['username']}' viewed their orders.")
        elif action == '4':
            # Update an order
            try:
                print("Enter order ID:")
                order_id = int(input("Input: "))
                print("Enter new quantity:")
                new_quantity = int(input("Input: "))
                if new_quantity < 1:
                    print("Wrong quantity")
                    continue
                orders_service.update_order(order_id, user, new_quantity)
                logging.info(f"User '{user['username']}' updated order ID '{order_id}'.")
            except ValueError:
                print("Invalid input.")
                logging.error("Failed to update order due to invalid input.")
        elif action == '5':
            # Delete an order
            try:
                print("Enter order ID:")
                order_id = int(input("Input: "))
                orders_service.delete_order(order_id, user)
                logging.info(f"User '{user['username']}' deleted order ID '{order_id}'.")
            except ValueError:
                print("Invalid input.")
                logging.error("Failed to delete order due to invalid input.")
        elif action == 'E' or action == 'e':
            print("Logging out...")
            logging.info(f"User '{user['username']}' logged out.")
            break
