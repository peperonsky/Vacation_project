from logic.country_logic import CountryLogic
from logic.vacation_logic import VacationLogic
from facade.system_facade import VacationFacade
from logic.user_logic import UserLogic
from utils.dal import DAL
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
    
        
    def start2(self):
        name = UserLogic().get_first_name_by_id(self.cur_user)
        print("here")
        if (not UserLogic().is_admin(self.cur_user)):
            print("Hello ", name, "!\n What will you like to do?\n 1 - View vacations\n 2 - View liked vacations\n 3 - Sign out")
            while(True):
                response = input()
                if (response == "1"):
                    VacationLogic().showVacations()
                    self.which_vacation()
                elif (response == "3"):
                    self.signOut()
                elif (response == "2"):
                    self.get_liked_vacation_names(self.cur_user)
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
                elif response == "3":
                    try:
                        x = input("Which vacation would you like to edit? ")

                        if not x.isdigit():
                            print("Invalid input.")
                            self.start2()
                            return

                        x = int(x)

                        if 1 <= x <= 15:
                            self.get_vacation_update_details(x)
                        else:
                            print("Invalid vacation ID.")
                            self.start2()
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        self.start2()

                elif response == "4":
                    try:
                        x = input("Which vacation would you like to delete? ")

                        if not x.isdigit():
                            print("Invalid input.")
                            self.start2()
                            return

                        x = int(x)

                        if 1 <= x <= 15:
                            VacationLogic().del_vacation(x-1)
                            self.start2()
                        else:
                            print("Invalid vacation ID. Please enter a number between 1 and 15.")
                            self.start2()
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        self.start2()
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
            try:
                if (int(response) > 1 and int(response) < 15):
                    VacationLogic().print_vacation_details_by_number(int(response))
                    self.viewing()
                else:
                    self.start2()
            except:
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
                self.cur_user = user_logic.get_user_id_by_email(email)
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
            if (UserLogic().is_user_exists_by_details(f_name, l_name, email, password)):
                self.cur_user = UserLogic().get_user_id_by_email(email)
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
    
    
    def like_vacation(self):
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
            query = """
            SELECT COUNT(*) AS like_count
            FROM likes
            WHERE users_id = %s AND vacations_id = %s
            """
            params = (user_id, vacation_id['ID'])
            result = DAL().get_scalar(query, params)

            return result and result['like_count'] > 0

        except Exception as e:
            print(f"Error checking like status: {e}")
            return False
if __name__ == "__main__":
    user1 = user()
    user1.start()
        
    
