class UserDAO:
    def __init__(self, connection):
        self.connection = connection

    def create_user(self, username, password, role='user'):
        cursor = self.connection.cursor()
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, role))
        self.connection.commit()

    def get_user(self, username):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        return cursor.fetchone()

    def get_all_users(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM users"
        cursor.execute(query)
        return cursor.fetchall()
    
    def update_user(self, user_id, new_username, new_password, new_role):
        cursor = self.connection.cursor()
        query = "UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s"
        cursor.execute(query, (new_username, new_password, new_role, user_id))
        self.connection.commit()

    def delete_user(self, user_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        self.connection.commit()