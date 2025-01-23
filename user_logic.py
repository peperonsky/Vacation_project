from dal import DAL
import re
from datetime import datetime
        

class UserLogic:
    # Existing methods...
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()
    def validate_user_data(self, firstname, lastname, email, password, date_of_birth):
        if not firstname or len(firstname) < 2:
            print("Invalid first name. Must be at least 2 characters.")
            return False

        if not lastname or len(lastname) < 2:
            print("Invalid last name. Must be at least 2 characters.")
            return False

        email_regex = r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
        if not re.match(email_regex, email):
            print("Invalid email format.")
            return False

        if len(password) < 6:
            print("Password should be at least 6 characters long.")
            return False

        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            print("Invalid date of birth format. Use YYYY-MM-DD.")
            return False

        return True
    
    def is_admin(self, user_id):
        check_query = """
        SELECT role_id
        FROM users
        WHERE users_id = %s
        """
        params = (user_id,)
        result = self.dal._execute_query(check_query, params)

        if not result or result['role_id'] == 1:
            return True
        return False

    
    def add_user(self, firstname, lastname, email, password, date_of_birth, role):
        try:
            query_check = """
            SELECT COUNT(*) 
            FROM vacationbooking.users 
            WHERE email = %s
            """
            params_check = (email,)
            result_check = self.dal.get_scalar(query_check, params_check)

            if result_check and result_check['COUNT(*)'] > 0:
                print("Email already exists.")
                return False            

            query = """
            INSERT INTO vacationbooking.users (firstname, lastname, email, password, date_of_birth, role_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (firstname, lastname, email, password, date_of_birth, role)
            
            self.dal.insert(query, params)
            print(f"User '{firstname} {lastname}' added successfully.")
            return True

        except Exception as e:
            print(f"Error adding user: {e}")
            return False


    
    def view_all_users(self, admin_id):
        if not self.is_admin(admin_id):
            raise PermissionError("Access denied. Admin privileges required.")
        return self.dal.get_all_users()

    def manage_user_roles(self, admin_id, user_id, new_role):
        if not self.is_admin(admin_id):
            raise PermissionError("Access denied. Admin privileges required.")
        
        if new_role not in ['user', 'admin']:
            raise ValueError("Invalid role")

        return self.dal.update_user(user_id, {'role': new_role})

if __name__ == "__main__":
    
    try:
        with UserLogic() as user_logic:
            
            dal = DAL()
            users = dal.get_table("SELECT * FROM users")
            for user in users:
                print(f"User name:{user['firstname']}")
            

    except Exception as err:
        print(f"Error: {err}")