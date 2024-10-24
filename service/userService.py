from DAO.userDAO import UserDAO

class UserService:
    def __init__(self, connection):
        self.user_dao = UserDAO(connection)

    def get_user(self, username):
        user = self.user_dao.get_user(username)
        if user != None:
            return user
        else:
            print("User not found!")
        
        return None
    
    def login(self, username, password):
        user = self.user_dao.get_user(username)
        if user != None:
            if password == user['password']:
                print(f"Welcome, {user['username']}! Your role is: {user['role']}")
                return user
            else:
                print("Incorrect password!")
        else:
            print("User not found!")
        
        return None
    
    def register(self, username, password, role='user'):
        if self.user_dao.get_user(username) != None:
            print(f"Error: Username '{username}' is already taken.")
            return None
        
        self.user_dao.create_user(username, password, role)
        print(f"User '{username}' registered successfully with role '{role}'")

    def get_all_users(self):
        users = self.user_dao.get_all_users()
        for user in users:
            print(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")

    def delete_user(self, username):
        user = self.user_dao.get_user(username)
        if user != None:
            self.user_dao.delete_user(user['id'])
            print(f"User '{username}' has been deleted.")
        else:
            print(f"Error: User '{username}' not found.")

    def update_user(self, current_username, new_username=None, new_password=None, new_role=None):
        user = self.user_dao.get_user(current_username)
        
        if user != None:
            updated_username = new_username if new_username else user['username']
            updated_password = new_password if new_password else user['password']
            updated_role = new_role if new_role else user['role']

            self.user_dao.update_user(user['id'], updated_username, updated_password, updated_role)
            print(f"User '{current_username}' updated successfully.")
        else:
            print(f"Error: User '{current_username}' not found.")