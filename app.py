from user import add_new_user, view_all_users, save_users_to_csv, load_users_from_csv, delete_user, edit_user, get_user_by_username_password
from master_data import add_offense, update_offense, delete_offense, write_offense_fines_to_csv, load_offense_fines_from_csv, view_all_offenses
from violation import load_violations_from_csv, add_violation, view_violations, write_violations_to_csv, make_payment, delete_violation
# Super User Credentials
SUPERUSER_NAME = "admin"
SUPERUSER_PASSWORD = "admin123"

logged_in_user = None

def manage_users_menu():
    while True:
        print("\n***** Manage Users *****")
        print("1. Add New User")
        print("2. View All Users")
        print("3. Edit User")
        print("4. Delete User")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                add_new_user()
            elif choice == 2:
                view_all_users()
            elif choice == 3:
                edit_user()
            elif choice == 4:
                delete_user()    
            elif choice == 5:
                break  # Return to the main menu
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")


def display_superuser_menu():
    while True:
        print("\n***** Admin Menu *****")
        print("1. Manage Users")
        print("2. Manage Violation Records")
        print("3. System Settings")
        print("4. Logout")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                manage_users_menu()
            elif choice == 2:
                display_manage_cases_menu_admin()
            elif choice == 3:
                display_system_settings_menu()  
            elif choice == 4:
                save_users_to_csv()
                write_offense_fines_to_csv()
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

def display_manage_cases_menu_admin():
    while True:
        print("\n***** Manage Violation Records *****")
        print("1. View Violation Records")
        print("2. Add Violation Record")
        print("3. Delete Violation Record")
        print("4. Make Payment")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                view_violations()
            elif choice == 2:
                add_violation()
            elif choice == 3:
                violation_id = input("Enter the violation ID to delete: ")
                delete_violation(violation_id)
            elif choice == 4:
                violation_id = input("Enter the violation ID to make payment: ")
                fine_amount = float(input("Enter the fine amount: "))
                make_payment(violation_id, fine_amount)
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

def display_system_settings_menu():
    while True:
        print("\n***** System Settings *****")
        print("1. Manage Offense Types")
        print("2. Back to Main Menu")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                manage_offenses_menu()
            elif choice == 2:
                break  # Return to the main menu
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

def manage_offenses_menu():
    while True:
        print("\n***** Manage Offenses *****")
        print("1. Add Offense Type")
        print("2. Update Offense Type")
        print("3. Delete Offense Type")
        print("4. View All Offense Types")
        print("5. Back to System Settings")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                offense = input("Enter the offense: ")
                fine_amount = float(input("Enter the fine amount: "))
                add_offense(offense, fine_amount)
            elif choice == 2:
                offense = input("Enter the offense to update: ")
                new_fine_amount = float(input("Enter the new fine amount: "))
                update_offense(offense, new_fine_amount)
            elif choice == 3:
                offense = input("Enter the offense to delete: ")
                delete_offense(offense)
            elif choice == 4:
                view_all_offenses()
            elif choice == 5:
                break  # Return to the system settings menu
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")


def display_police_officer_menu():
    while True:
        print("\n***** Police Officer Menu *****")
        print("1. Manage Violation Records")
        print("2. Manage Profile")
        print("3. Logout")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                print("View Violation Records")
            elif choice == 2:
                print("Add Case")
            elif choice == 3:
                save_users_to_csv()
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

def display_postal_clerk_menu():
    while True:
        print("\n***** Postal Clerk Menu *****")
        print("1. Manage Violation Records")
        print("2. Manage Profile")
        print("3. Logout")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                print("View Violation Records")
            elif choice == 2:
                print("Add Case")
            elif choice == 3:
                save_users_to_csv()
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")            


def login():
    global logged_in_user
    print("****************** Welcome to FineTrackPro ********************")
    print("Please enter your credentials to login.")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == SUPERUSER_NAME and password == SUPERUSER_PASSWORD:
        logged_in_user = "Admin"
        print("Login successful! Welcome, Admin.")
        display_superuser_menu()
    elif get_user_by_username_password(username, password) is not None:
        user = get_user_by_username_password(username, password)
        if user.role == "Police Officer":
            logged_in_user = "Police Officer"
        else:
            logged_in_user = "Postal Clerk"

        print(f"Login successful! Welcome, {user.name}.")
        if logged_in_user == "Police Officer":
            display_police_officer_menu()
        else:
            display_postal_clerk_menu()
    else:
        print("Invalid credentials. Access denied.")

if __name__ == "__main__":
    load_users_from_csv()
    load_offense_fines_from_csv()
    login()
