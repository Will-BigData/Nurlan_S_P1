from DAO.productDAO import ProductDAO

class ProductService:
    def __init__(self, connection):
        self.product_dao = ProductDAO(connection)

    def get_product(self, id):
        product = self.product_dao.get_product(id)
        if product != None:
            return product
        else:
            print("Product Not Found")

    def add_product(self, name, description, price, stock):
        self.product_dao.add_product(name, description, price, stock)
        print(f"Product '{name}' added successfully.")
    
    def get_all_products(self):
        products = self.product_dao.get_all_products()
        for product in products:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Stock: {product['stock']}")

    def update_product(self, product_id, name=None, description=None, price=None, stock=None):
        product = self.product_dao.get_product(product_id)
        if product:
            if name is None:
                name = product['name']
            if description is None:
                description = product['description']
            if price is None:
                price = product['price']
            if stock is None:
                stock = product['stock']

            self.product_dao.update_product(product_id, name, description, price, stock)
            print(f"Product ID '{product_id}' updated successfully.")
        else:
            print(f"Error: Product ID '{product_id}' not found.")

    def delete_product(self, product_id):
        self.product_dao.delete_product(product_id)
        print(f"Product ID '{product_id}' deleted successfully.")