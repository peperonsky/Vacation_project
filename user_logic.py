from utils.dal import DAL
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
    def get_user_id_by_email(self, email):
        try:
            query = "SELECT user_id FROM users WHERE email = %s"
            params = (email,)
            
            result = DAL().get_scalar(query, params)
            
            if result:
                return result['user_id']
            else:
                print(f"No user found with email: {email}")
                return None
        except Exception as e:
            print(f"Error fetching user_id: {e}")
            return None
    
    def is_user_exists_by_details(firstname, lastname, email, password) -> bool:
        try:
            query = """
            SELECT COUNT(*) 
            FROM users 
            WHERE firstname = %s AND lastname = %s AND email = %s AND password = %s
            """
            params = (firstname, lastname, email, password)
            result = DAL().get_scalar(query, params)
            
            if result and result['COUNT(*)'] > 0:
                return True
            return False
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False
    def get_liked_vacation_names(cur_user):
        user_id = cur_user
        try:
            query = """
            SELECT v.title
            FROM vacations v
            JOIN likes l ON v.id = l.vacations_id
            WHERE l.users_id = %s
            """
            params = (user_id,)

            vacations = DAL().get_table(query, params)

            if not vacations:
                print(f"No liked vacations found for user ID {user_id}.")
                return []

            print("Liked Vacations:")
            for i, vacation in enumerate(vacations, start=1):
                print(f"{i}. {vacation['title']}")

            return [vacation['title'] for vacation in vacations]

        except Exception as e:
            print(f"Error retrieving liked vacation names: {e}")
            return []
    def get_first_name_by_id(user_id):

        try:
            query = """
            SELECT firstname 
            FROM users
            WHERE user_id = %s
            """
            params = (user_id,)
            
            result = DAL().get_scalar(query, params)

            if result:
                return result['firstname']
            else:
                print(f"No user found with ID: {user_id}")
                return None

        except Exception as e:
            print(f"Error retrieving first name: {e}")
            return None
    
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
