import sys
import os

# הוספת התיקייה הראשית (vacation-system) לנתיב החיפוש
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# כעת ניתן לייבא את DAL
from utils.dal import DAL

class CountryLogic:
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()

    def check_if_country_exist(self, countries_name):
        try:
            query = """
            SELECT COUNT(*) 
            FROM vacationbooking.countries 
            WHERE country_name = %s
            """
            params = (countries_name,)
            
            result = self.dal.get_scalar(query, params)
            
            if result and result['COUNT(*)'] > 0:
                return True
            return False
            
        except Exception as e:
            print(f"Error checking if country exists: {e}")
            return False


    def get_all_countries(self):
        try:
            query = "SELECT * FROM vacationbooking.countries"
            
            # Get all rows from the query
            countries = self.dal.get_table(query)
            
            return countries if countries else []
        
        except Exception as e:
            print(f"Error retrieving all countries: {e}")
            return []

    def add_country(self, country_name):
        try:
            # בדוק אם המדינה כבר קיימת
            if self.check_if_country_exist(country_name):
                print(f"Country '{country_name}' already exists.")
                return False

            # שאילתת ה-INSERT להוספת מדינה חדשה
            query = """
            INSERT INTO vacationbooking.countries (country_name)
            VALUES (%s)
            """
            params = (country_name,)
            
            # הוספת המדינה
            self.dal.insert(query, params)
            print(f"Country '{country_name}' added successfully.")
            return True

        except Exception as e:
            print(f"Error adding country: {e}")
            return False

    def del_country(self, country_name):
        try:
            # בדוק אם המדינה קיימת
            if not self.check_if_country_exist(country_name):
                print(f"Country '{country_name}' does not exist.")
                return False

            # שאילתת DELETE להסרת המדינה
            query = """
            DELETE FROM vacationbooking.countries 
            WHERE country_name = %s
            """
            params = (country_name,)
            
            # הסרת המדינה
            self.dal.delete(query, params)
            print(f"Country '{country_name}' deleted successfully.")
            return True

        except Exception as e:
            print(f"Error deleting country: {e}")
            return False


if __name__ == "__main__":
    
    try:
        with CountryLogic() as country_logic:
            
            countries = country_logic.get_all_countries()
            for country in countries:
                print("----------------------")
                print(country)
    except Exception as err:
        print(f"Error: {err}")
