class OrdersDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_order(self, order_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM orders WHERE id = %s"
        cursor.execute(query, (order_id,))
        return cursor.fetchone()

    def get_all_orders(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM orders"
        cursor.execute(query)
        return cursor.fetchall()

    def update_order(self, order_id, quantity):
        cursor = self.connection.cursor()
        query = "UPDATE orders SET quantity = %s WHERE id = %s"
        cursor.execute(query, (quantity, order_id))
        self.connection.commit()
    
    def delete_order(self, order_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM orders WHERE id = %s"
        cursor.execute(query, (order_id,))
        self.connection.commit()

    #------------------ user ----------------------
    def get_orders_by_user(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM orders WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    
    def create_order(self, user_id, product_id, quantity):
        cursor = self.connection.cursor()
        query = "INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, product_id, quantity))
        self.connection.commit()