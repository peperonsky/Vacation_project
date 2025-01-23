
import sys
import os

# הוספת התיקייה הראשית (vacation-system) לנתיב החיפוש
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# כעת ניתן לייבא את DAL
from dal import DAL

class VacationLogic:
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()

    def get_all_vacations(self):

        query = "SELECT * from vacationbooking.vacations"
        result = self.dal.get_table(query)
        return result if result is not None else []

    def add_vacation(self, title, description, start_date, end_date,countries_name, price):
        try:
            query = """
            INSERT INTO vacationbooking.vacations 
            (title, description, start_date, end_date, countries_id, price, likes)
            VALUES 
            (%s, %s, %s, %s, (SELECT id FROM vacationbooking.countries WHERE country_name LIKE %s), %s, 0)
            """
            params = (title, description, start_date,
                    end_date, f"%{countries_name}%", price)
            self.dal.insert(query, params)
            return True

        except Exception as err:
            print(f"Error adding vacation: {err}")
            return False

    def edit_vacation(self, id, **kwargs):
        if not kwargs:
            return False

        clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])

        params = tuple(kwargs.values()) + (id,)
        query = f"UPDATE vacationbooking.vacations SET {clause} WHERE id = %s"

        try:
            self.dal.update(query, params)
            return True
        except Exception as e:
            print(f"Error updating vacation: {e}")
            return False

    def del_vacation(self, id):
        query = "DELETE FROM vacationbooking.vacations WHERE id = %s"
        params = (id,)
        try:
            result = self.dal.delete(query, params)
            return True
        except Exception as err:
            print(f"Error deleting vacation: {err}")
            return False


if __name__ == "__main__":
    
    try:
        with VacationLogic() as vacation_logic:

            vacations = vacation_logic.get_all_vacations()
            for vacation in vacations:
                print("----------------------")
                print(vacation)
    except Exception as err:
        print(f"Error: {err}")