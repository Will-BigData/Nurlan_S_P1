class ProductDAO:
    def __init__(self, connection):
        self.connection = connection

    def add_product(self, name, description, price, stock):
        cursor = self.connection.cursor()
        query = "INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, description, price, stock))
        self.connection.commit()

    def get_product(self, product_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(query, (product_id,))
        return cursor.fetchone()

    def get_all_products(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM products"
        cursor.execute(query)
        return cursor.fetchall()
    
    def update_product(self, product_id, new_name, new_description, new_price, new_stock):
        cursor = self.connection.cursor()
        query = "UPDATE products SET name = %s, description = %s, price = %s, stock = %s WHERE id = %s"
        cursor.execute(query, (new_name, new_description, new_price, new_stock, product_id))
        self.connection.commit()

    def delete_product(self, product_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM products WHERE id = %s"
        cursor.execute(query, (product_id,))
        self.connection.commit()