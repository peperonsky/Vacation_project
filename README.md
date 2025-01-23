Python version - Python 3.8
Required software - MySQL database

This project is a vacation management system built using Python and MySQL. It is designed with a three-layer architecture for better organization and separation of concerns:

- Data Access Layer (DAL): Handles all database interactions.
- Business Logic Layer (BLL): Implements application rules and validations.
- Facade Layer: Provides a simple interface for the system.

- User Features:
  - Register and log in to the system.
  - View vacations and like/unlike them.
  - View vacations they have liked.

- Admin Features:
  - Add, edit, or delete vacations.
  - Manage user roles (promote a user to admin).

- Role-Based Access Control:
  - Admin-only actions are restricted to users with the "admin" role.

- Python 3.8 or above.
- MySQL installed on your system.

1. Clone the repository:
   ```
   git clone https://github.com/LiadM1/vacation-management-system.git
   cd vacation-management-system
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the database:
   - Run the provided database creation script in your MySQL server.
   - Populate the database with initial data (users, vacations, and roles).

4. Run the application:
   ```
   python src/main.py
   ```

- The database schema includes the following tables:
  - Users: Stores user information like name, email, password, role, etc.
  - Vacations: Stores vacation details such as title, country, dates, and price.
  - Roles: Manages roles (user/admin).
  - Likes: Tracks which user liked which vacation.
  - Countries: Stores a list of available countries.

vacation-management-system/
├── src/
│   ├── utils/
│   │   └── dal.py              # Data Access Layer
│   ├── logic/
│   │   ├── user_logic.py       # User-related business logic
│   │   ├── vacation_logic.py   # Vacation-related business logic
│   │   └── country_logic.py    # country-related business logic
│   ├── facade/
│   │   └── system_facade.py    # Facade Layer
│   └── main.py                 # Entry point of the application
├── tests/                      # Contains test scripts
├── requirements.txt            # Dependency list
├── README.md                   # Project documentation
```
### User Workflow
1. Register: Create an account with a valid email and secure password.
2. Log in: Authenticate with email and password.
3. Explore Vacations: Browse all available vacations.
4. Like/Unlike Vacations: Save your favorite vacations.
5. View Liked Vacations: See a list of all vacations you have liked.

### Admin Workflow
1. Log in: Authenticate as an admin.
2. Manage Vacations: Add, edit, or delete vacations.
3. Manage Roles: Promote or demote users to admin or standard roles.

## Testing
- A checklist for testing includes:
  - User Features:
    - Registration with valid and invalid data.
    - Logging in with correct and incorrect credentials.
  - Vacation Features:
    - Creating, editing, and deleting vacations.
    - Validating vacation prices and dates.
  - Like System:
    - Liking and unliking vacations.
    - Ensuring a user can only like a vacation once.

## Team Members
- Guy Lautin: Contributions to main.py, counrty_logic.py.
- Liad Mashi: Contributions to user_logic.py, README.md, requirements.txt.
- Ori Shamir: Contributions to dal.py, facade.py, vacation_logic.py.

## License
This project is for educational purposes and is not licensed for production use.
