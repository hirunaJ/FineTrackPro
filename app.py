from user import add_new_user, view_all_users, save_users_to_csv, load_users_from_csv, delete_user, edit_user, get_user_by_username_password

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
        print("2. Manage Cases")
        print("3. System Settings")
        print("4. Logout")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                manage_users_menu()
            elif choice == 2:
                print("System settings (feature coming soon!)")
            elif choice == 3:
                print("System settings (feature coming soon!)")    
            elif choice == 4:
                save_users_to_csv()
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

def display_manage_cases_menu():
    print("\n***** Manage Cases *****")
    print("1. View Cases")
    print("2. Add Case")
    print("3. Back to Main Menu")
    choice = input("Enter your choice: ")


def display_regular_user_menu():
    while True:
        print("\n***** Police Officer Menu *****")
        print("1. Manage Cases")
        print("2. Manage Profile")
        print("3. Logout")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 1:
                print("View Cases")
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
        display_regular_user_menu()
    else:
        print("Invalid credentials. Access denied.")

if __name__ == "__main__":
    load_users_from_csv()
    login()
