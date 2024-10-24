from DAO.ordersDAO import OrdersDAO
from DAO.productDAO import ProductDAO

class OrdersService:
    def __init__(self, connection):
        self.orders_dao = OrdersDAO(connection)
        self.product_dao = ProductDAO(connection)

    def get_all_orders(self):
        orders = self.orders_dao.get_all_orders()
        for order in orders:
            print(f"ID: {order['id']}, User ID: {order['user_id']}, Product ID: {order['product_id']}, Quantity: {order['quantity']}, Date: {order['order_date']}")
    
    def get_user_orders(self, user_id):
        orders = self.orders_dao.get_orders_by_user(user_id)
        if orders:
            for order in orders:
                print(f"Order ID: {order['id']}, Product ID: {order['product_id']}, Quantity: {order['quantity']}, Date: {order['order_date']}")
        else:
            print("No orders found.")

    def place_order(self, user_id, product_id, quantity):
        product = self.product_dao.get_product(product_id)
        if not product:
            print("Product not found.")
            return
        
        if product['stock'] < quantity:
            print("Not enough stock available.")
            return

        self.orders_dao.create_order(user_id, product_id, quantity)
        self.product_dao.update_product(product_id, product['name'], product['description'], product['price'], product['stock'] - quantity)
        print("Order placed successfully.")

    def update_order(self, order_id, user, new_quantity):
        order = self.orders_dao.get_order(order_id)
        if not order or (order['user_id'] != user['id'] and user['role'] != 'admin'):
            print("Order not found or access denied.")
            return
        
        product = self.product_dao.get_product(order['product_id'])
        if not product:
            print("Product not found.")
            return

        # Calculate the difference between old and new quantity
        quantity_diff = new_quantity - order['quantity']
        if product['stock'] < quantity_diff:
            print("Not enough stock available.")
            return

        self.orders_dao.update_order(order_id, new_quantity)
        self.product_dao.update_product(order['product_id'], product['name'], product['description'], product['price'], product['stock'] - quantity_diff)
        print("Order updated successfully.")

    def delete_order(self, order_id, user):
        order = self.orders_dao.get_order(order_id)
        if not order or (order['user_id'] != user['id'] and user['role'] != 'admin'):
            print("Order not found or access denied.")
            return

        # Restore the stock when deleting the order
        product = self.product_dao.get_product(order['product_id'])
        self.product_dao.update_product(product['id'], product['name'], product['description'], product['price'], product['stock'] + order['quantity'])
        
        self.orders_dao.delete_order(order_id)
        print("Order deleted successfully.")