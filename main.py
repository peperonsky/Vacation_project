from country_logic import CountryLogic
from vacation_logic import VacationLogic
from system_facade import VacationFacade
from user_logic import UserLogic
from dal import DAL
import re
import datetime
class user:
    def __init__(self):
        pass
        self.cur_user  = 0
        self.viewed_vac = 0
    def start(self):
        print("Welcome to the VacationBooking! what would you like to do?\n 1 - Sign up\n 2 - Sign in")
        while(True):
            response = input()
            if (response == "1"):
                self.signUp1()
            elif (response == "2"):
                self.signIn1()
            else:
                print("Invalid input try again.")
    def get_first_name_by_id(self, user_id):

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
    
        
    def start2(self):
        name = self.get_first_name_by_id(self.cur_user)
        print("here")
        if (not UserLogic().is_admin(self.cur_user)):
            print("Hello ", name, "!\n What will you like to do?\n 1 - View vacations\n 2 - View liked vacations\n 3 - Sign out")
            while(True):
                response = input()
                if (response == "1"):
                    self.showVacations()
                    self.which_vacation()
                elif (response == "3"):
                    self.signOut()
                elif (response == "2"):
                    self.get_liked_vacation_names()
                    self.start2()
                else:
                    print("Invalid input try again.")
        else:
            print("Hello ", name, "!\n What will you like to do?\n 1 - View vacations\n 2 - Add new vacation\n 3 - Edit existing vacations\n 4 - delete vacations\n 5 - Sign out")
            while(True):
                response = input()
                if (response == "1"):
                    self.showVacations()
                    self.which_vacation()
                elif (response == "5"):
                    self.signOut()
                elif (response == "2"):
                    self.adding_vac()
                elif (response == "3"):
                    x = input("Which vacation would you like to edit?")
                    if(x.isalnum):
                        if (int(x)> 1 and int(x) < 15):
                            self.get_vacation_update_details(x)
                    else:
                        print("Invalid input")
                        self.start2()
                elif (response == "2"):
                    x = input("Which vacation would you like to delete?")
                    if(x.isalnum):
                        if (int(x)> 1 and int(x) < 15):
                            VacationLogic.del_vacation(x)
                    else:
                        print("Invalid input")
                else:
                    print("Invalid input try again.")
    def get_vacation_update_details(self, vacation_id):

        kwargs = {}

        print(f"Updating vacation with ID: {vacation_id}")

        while True:
            vacation_title = input("Enter the new vacation title (at least 2 characters, or press Enter to skip): ").strip()
            if vacation_title and len(vacation_title) >= 2:
                kwargs["vacation_title"] = vacation_title
                break
            elif vacation_title == "":
                break
            else:
                print("Invalid input. Vacation title must be at least 2 characters.")

        while True:
            description = input("Enter the new vacation description (at least 10 characters, or press Enter to skip): ").strip()
            if description and len(description) >= 10:
                kwargs["description"] = description
                break
            elif description == "":
                break
            else:
                print("Invalid input. Description must be at least 10 characters.")

        while True:
            country = input("Enter the new country name (only letters, or press Enter to skip): ").strip()
            if country and country.isalpha() and len(country) >= 2:
                kwargs["country"] = country
                break
            elif country == "":
                break
            else:
                print("Invalid input. Country name must contain only letters and be at least 2 characters.")

        while True:
            try:
                start_date = input("Enter the new start date (YYYY-MM-DD, or press Enter to skip): ").strip()
                if start_date:
                    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                    if start_date_obj > datetime.today():
                        kwargs["start_date"] = start_date
                        break
                    else:
                        print("Invalid input. Start date must be in the future.")
                else:
                    break
            except ValueError:
                print("Invalid format. Please enter the date in YYYY-MM-DD format.")

        while True:
            try:
                end_date = input("Enter the new end date (YYYY-MM-DD, or press Enter to skip): ").strip()
                if end_date:
                    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
                    if end_date_obj > start_date_obj:
                        kwargs["end_date"] = end_date
                        break
                    else:
                        print("Invalid input. End date must be after the start date.")
                else:
                    break
            except ValueError:
                print("Invalid format. Please enter the date in YYYY-MM-DD format.")

        while True:
            try:
                price = input("Enter the new price (1,000 - 10,000, or press Enter to skip): ").strip()
                if price:
                    price = int(price)
                    if 1000 <= price <= 10000:
                        kwargs["price"] = price
                        break
                    else:
                        print("Invalid input. Price must be between 1,000 and 10,000.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        with VacationLogic() as vacation_logic:
            vacation_logic.edit_vacation(vacation_id, kwargs)
            self.start2()
        
    def adding_vac(self):
        while True:
            vacation_title = input("Enter the vacation title (at least 2 characters): ").strip()
            if len(vacation_title) >= 2:
                break
            print("Invalid input. Vacation title must be at least 2 characters.")

        while True:
            country = input("Enter the country name (only letters): ").strip()
            if country.isalpha() and len(country) >= 2:
                break
            print("Invalid input. Country name must contain only letters and be at least 2 characters.")

        while True:
            try:
                start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                if start_date_obj > datetime.today():
                    break
                print("Invalid input. Start date must be in the future.")
            except ValueError:
                print("Invalid format. Please enter the date in YYYY-MM-DD format.")

        while True:
            try:
                end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
                if end_date_obj > start_date_obj:
                    break
                print("Invalid input. End date must be after the start date.")
            except ValueError:
                print("Invalid format. Please enter the date in YYYY-MM-DD format.")
        while True:
            description = input("Enter the vacation description (at least 10 characters): ").strip()
            if len(description) >= 10:
                break
            print("Invalid input. Description must be at least 10 characters.")

        while True:
            try:
                price = int(input("Enter the vacation price (1,000 - 10,000): ").strip())
                if 1000 <= price <= 10000:
                    break
                print("Invalid input. Price must be between 1,000 and 10,000.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        with VacationLogic() as vacation_logic:
            vacation_logic.add_vacation(vacation_title, description, start_date, end_date, country, price)
            self.start2()
    def which_vacation(self):
        print("Enter which vacation you would like to view or enter anything else to go back: ")
        response = input()
        if (response.isalnum):
            if (int(response) > 1 and int(response) < 15):
                self.print_vacation_details_by_number(int(response))
                self.viewing()
            else:
                self.start2()
        else:
            self.start2()
    def viewing(self):
        if not UserLogic().is_admin(self.cur_user):
            print("What will you like to do?")
            if (self.has_liked_vacation()):
                print("1 - unlike vacation\n 2 - go back")
                response = input()
                if (response == "1"):
                    self.unlike_vacation()
                    self.viewing()
                if (response == "2"):
                    self.start2()
            else:
                print("1 - like vacation\n 2 - go back")
                response = input()
                if (response == "1"):
                    self.like_vacation()
                    self.viewing()
                if (response == "2"):
                    self.start2()
        else:
            self.start2()
    def get_liked_vacation_names(self):
        user_id = self.cur_user
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

    def signUp1(self):
        flag = True
        while(flag):
            f_name = input("Enter first name:")
            if re.fullmatch(r"[a-zA-Z]+", f_name):
                flag = False
            if len(f_name) <= 2:
                flag = True
            if (flag == True):
                print("Invalid input: first name must be longer than 2 letters and contain only letters!\n Try again.")
        flag = True
        while(flag):
            l_name = input("Enter last name: ")
            if re.fullmatch(r"[a-zA-Z]+", l_name):
                flag = False
            if len(l_name) <= 2:
                flag = True
            if (flag == True):
                print("Invalid input: last name must be longer than 2 letters and contain only letters!\n Try again.")
        flag = True

        while(flag):
            email = input("Enter email: ")
            email_regex = r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
            if not re.match(email_regex, email):
                print("Invalid email format.\n Try again")
                flag = True
            else:
                flag = False
        flag = True
        while(flag):
            password = input("Enter password: ")
            if len(password) < 6:
                print("Password should be at least 6 characters long.\n Try again")
            else:
                flag = False
        flag = True
        while(flag):
            d_o_b = input("Enter birth date (YYYY-MM-DD): ")
            try:
                datetime.datetime.strptime(d_o_b, "%Y-%m-%d")
                flag = False
            except ValueError:
                print("Invalid date of birth format. Use YYYY-MM-DD.")
        query_check = """
        SELECT COUNT(*) 
        FROM vacationbooking.users 
        WHERE email = %s
        """
        params_check = (email,)
        result_check = DAL().get_scalar(query_check, params_check)

        if result_check and result_check['COUNT(*)'] > 0:
            print("Email already exists.")
            self.signUp1()
        self.signUp2(f_name, l_name, email, password, d_o_b)
                
        
    def signUp2(self, f_name, l_name, email, password, d_o_b):
        try:   
            with UserLogic() as user_logic:
                user_logic.add_user(f_name, l_name, email, password, d_o_b, 2)
                self.cur_user = self.get_user_id_by_email(email)
                self.start2()
        except Exception as err:
            print(f"Error: {err}")
            self.signUp1()
    def signIn1(self):
        flag = True
        while(flag):
            f_name = input("Enter first name:")
            if re.fullmatch(r"[a-zA-Z]+", f_name):
                flag = False
            if len(f_name) <= 2:
                flag = True
            if (flag == True):
                print("Invalid input: first name must be longer than 2 letters and contain only letters!\n Try again.")
        flag = True
        while(flag):
            l_name = input("Enter last name: ")
            if re.fullmatch(r"[a-zA-Z]+", l_name):
                flag = False
            if len(l_name) <= 2:
                flag = True
            if (flag == True):
                print("Invalid input: last name must be longer than 2 letters and contain only letters!\n Try again.")
        flag = True

        while(flag):
            email = input("Enter email: ")
            email_regex = r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
            if not re.match(email_regex, email):
                print("Invalid email format.\n Try again")
                flag = True
            else:
                flag = False
        flag = True
        while(flag):
            password = input("Enter password: ")
            if len(password) < 6:
                print("Password should be at least 6 characters long.\n Try again")
            else:
                flag = False
        self.signIn2(f_name, l_name, email, password)
    def signIn2(self, f_name, l_name, email, password):
        try:   
            if (self.is_user_exists_by_details(f_name, l_name, email, password)):
                self.cur_user = self.get_user_id_by_email(email)
                self.start2()
            else:
                print("One or more of the details is wrong.")
                self.signIn1()
        except Exception as err:
            print(f"Error: {err}")
            self.signIn1()
    def signOut(self):
        self.cur_user = 0
        self.start()
    def is_user_exists_by_details(self, firstname, lastname, email, password) -> bool:
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
    def showVacations(self):
        try:
           
            vacations = DAL().get_table("SELECT title FROM vacations")

            if not vacations:
                print("No vacations found.")
                return

            print("List of all vacations:")
            for i, vacation in enumerate(vacations, start=1):
                print(f"{i} - {vacation['title']}")

        except Exception as e:
            print(f"Error fetching vacations: {e}")

    def print_vacation_details_by_number(self, vacation_number):
        try:
            
            vacations = DAL().get_table("SELECT title, start_date, end_date, price, description FROM vacations")

            if not vacations or vacation_number < 1 or vacation_number > len(vacations):
                print("Invalid vacation number.")
                return

            selected_vacation = vacations[vacation_number - 1]
            
            print("Vacation Details:")
        
            print(f"title: {selected_vacation['title']}")
            print(f"Start Date: {selected_vacation['start_date']}")
            print(f"End Date: {selected_vacation['end_date']}")
            print(f"Price: ${selected_vacation['price']:.2f}")
            print(f"Description: {selected_vacation['description']}")
            vacations = DAL().get_table("SELECT ID FROM vacations")
            self.viewed_vac = vacations[vacation_number - 1]

        except Exception as e:
            print(f"Error fetching vacation details: {e}")
    def like_vacation(self):
        """
        פונקציה שמסמנת לייק לחופשה עבור משתמש מסוים ומעדכנת את total_likes.
        """
        vacation_id = self.viewed_vac
        try:
            check_query = """
            SELECT COUNT(*) AS like_count
            FROM likes
            WHERE users_id = %s AND vacations_id = %s
            """
            params = (self.cur_user, vacation_id['ID'])
            result = DAL().get_scalar(check_query, params)

            if result and result['like_count'] > 0:
                print("You already liked this vacation.")
                return False

            insert_query = """
            INSERT INTO likes (users_id, vacations_id)
            VALUES (%s, %s)
            """
            DAL().insert(insert_query, params)

            update_query = """
            UPDATE vacations
            SET total_likes = total_likes + 1
            WHERE vacation_id = %s
            """
            DAL()._execute_query(update_query, (vacation_id['ID'],))

            print("Vacation liked successfully.")
            return True

        except Exception as e:
            print(f"Error liking vacation: {e}")
            return False


    def unlike_vacation(self):
        user_id = self.cur_user
        vacation_id = self.viewed_vac
        try:
            check_query = """
            SELECT COUNT(*) AS like_count
            FROM likes
            WHERE users_id = %s AND vacations_id = %s
            """
            params = (user_id, vacation_id['ID'])
            result = DAL().get_scalar(check_query, params)

            if not result or result['like_count'] == 0:
                print("No like found for this vacation.")
                return False

            delete_query = """
            DELETE FROM likes
            WHERE users_id = %s AND vacations_id = %s
            """
            DAL()._execute_query(delete_query, params)

            update_query = """
            UPDATE vacations
            SET total_likes = total_likes - 1
            WHERE vacation_id = %s
            """
            DAL()._execute_query(update_query, (vacation_id['ID'],))

            print("Vacation unliked successfully.")
            return True

        except Exception as e:
            print(f"Error unliking vacation: {e}")
            return False

    def has_liked_vacation(self):
        user_id = self.cur_user
        vacation_id = self.viewed_vac
        try:
            # בדיקת קיום לייק
            query = """
            SELECT COUNT(*) AS like_count
            FROM likes
            WHERE users_id = %s AND vacations_id = %s
            """
            params = (user_id, vacation_id['ID'])
            result = DAL().get_scalar(query, params)

            # החזרת התוצאה
            return result and result['like_count'] > 0

        except Exception as e:
            print(f"Error checking like status: {e}")
            return False
user1 = user()
user1.start()
        
    