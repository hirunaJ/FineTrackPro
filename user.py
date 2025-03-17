# Handles user management
import csv
import os

USER_DATA_FOLDER = "user_data"
users_array = []
user_id_sequence = 1

class User:
    def __init__(self, username, name, password, role):
        self.username = username
        self.name = name
        self.user_id = user_id_sequence
        self.role = role
        self.password = password

    def display_info(self):
        return f"{self.user_id} \t{self.name} \t{self.role}"
    
    # update password
    def update_username_password(self, new_username, new_password):
        self.username = new_username
        self.password = new_password
        self.update()

    def delete(self):
        users_array.remove(self)  
              
    def update(self):
        for i in range(len(users_array)):
            if users_array[i].user_id == self.user_id:
                users_array[i] = self
                break

    def save(self):
        global user_id_sequence
        user_id_sequence += 1
        users_array.append(self)


class PoliceOfficer(User):
    def __init__(self, username, name, password, reference_no, police_station, rank, department):
        super().__init__(username, name, password, "Police Officer")
        self.reference_no = reference_no
        self.police_station = police_station
        self.rank = rank
        self.department = department

    def display_info(self):
        return f"{super().display_info()} \t{self.reference_no} \t{self.police_station} \t{self.rank} \t{self.department}"


class PostalClerk(User):
    def __init__(self, username, name, password, post_office, region):
        super().__init__( username, name, password, "Postal Clerk")
        self.post_office = post_office
        self.region = region

    def display_info(self):
        return f"{super().display_info()} \t{self.post_office} \t{self.region}"


def add_new_user():
    print("\n***** Add New User *****")
    print("Choose user type:")
    print("1. Police Officer")
    print("2. Postal Clerk")

    try:
        choice = int(input("Enter your choice: "))

        name = input("Enter Name: ")
        username = input("Enter User Name: ")
        password = input("Enter User Password: ")

        if choice == 1:
            reference_no = input("Enter Reference Number: ")
            police_station = input("Enter Police Station: ")
            rank = input("Enter Rank: ")
            department = input("Enter Department: ")
            user = PoliceOfficer(username, name, password, reference_no, police_station, rank, department)
        elif choice == 2:
            post_office = input("Enter Post Office: ")
            region = input("Enter Region: ")
            user = PostalClerk(username, name, password, post_office, region)
        else:
            print("Invalid choice.")
            return

        user.save()
        save_users_to_csv()
        print("User added successfully!")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

def delete_user():
    print("\n***** Delete User *****")
    user_id = int(input("Enter User ID to delete: "))

    user = next((user for user in users_array if user.user_id == user_id), None)
    if user:
        user.delete()
        save_users_to_csv()
        print("User deleted successfully!")
    else:
        print("User not found.")

def edit_user():
    print("\n***** Edit User *****")
    user_id = int(input("Enter User ID to edit: "))

    user = next((user for user in users_array if user.user_id == user_id), None)
    if user:
        print("User found. Enter new details.")
        

        if isinstance(user, PoliceOfficer):
            print("\n#ID \tName \t\tRole \t\tRef \tPolice Station \tRank \tDepartment")
            print(user.display_info())
            name = input("Enter Name: ")
            reference_no = input("Enter Reference Number: ")
            police_station = input("Enter Police Station: ")
            rank = input("Enter Rank: ")
            department = input("Enter Department: ")
            user.name = name
            user.reference_no = reference_no
            user.police_station = police_station
            user.rank = rank
            user.department = department
        elif isinstance(user, PostalClerk):
            print("\n#ID \tName \t\tRole \t\tPost Office \tRegion")
            user.display_info()
            print(user.display_info())
            name = input("Enter Name: ")
            post_office = input("Enter Post Office: ")
            region = input("Enter Region: ")
            user.name = name
            user.post_office = post_office
            user.region = region

        user.update()
        save_users_to_csv()
        print("User updated successfully!")
    else:
        print("User not found.")       

def view_all_users():
    print("\nChoose user type:")
    print("1. Police Officer")
    print("2. Postal Clerk")
    print("3. All Users")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            users = [user for user in users_array if isinstance(user, PoliceOfficer)]
        elif choice == 2:
            users = [user for user in users_array if isinstance(user, PostalClerk)]
        elif choice == 3:
            users = users_array
        else:
            print("Invalid choice.")
            return
        
        if not users:
            print("No users available.")
            return

        if choice == 1:
            print("\n#ID \tName \t\tRole \t\tRef \tPolice Station \tRank \tDepartment")
        elif choice == 2:
            print("\n#ID \tName \t\tRole \t\tPost Office \tRegion")
        elif choice == 3:
            print("\n#ID \tName \t\tRole")

        for user in users:
            print(user.display_info())

    except ValueError:
        print("Invalid input. Please enter a valid number.")
        view_all_users()    
    except Exception as e:  # Catch all other exceptions
        print(f"An unexpected error occurred getting users: {e}")    
        view_all_users()  


def save_users_to_csv():
    police_file = os.path.join(USER_DATA_FOLDER, "police_officers.csv")
    postal_file = os.path.join(USER_DATA_FOLDER, "postal_clerks.csv")

    police_officers = [user for user in users_array if isinstance(user, PoliceOfficer)]
    postal_clerks = [user for user in users_array if isinstance(user, PostalClerk)]

    try:
        with open("./user_data/police_officers.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User ID", "Name", "Reference No", "Police Station", "Rank", "Department", "Password"])
            for officer in police_officers:
                writer.writerow([officer.user_id, officer.name, officer.reference_no, officer.police_station, officer.rank, officer.department, officer.password, officer.username])

        with open("./user_data/postal_clerks.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User ID", "Name", "Post Office", "Region", "Password"])
            for clerk in postal_clerks:
                writer.writerow([clerk.user_id, clerk.name, clerk.post_office, clerk.region, clerk.password, clerk.username])

    except Exception as e:
        print(f"An unexpected error occurred when saving Users: {e}")  

def load_users_from_csv():
    global user_id_sequence
    police_file = os.path.join(USER_DATA_FOLDER, "police_officers.csv")
    postal_file = os.path.join(USER_DATA_FOLDER, "postal_clerks.csv")

    try:

        # Load Police Officers
        if os.path.exists(police_file):
            with open(police_file, "r", newline="") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    user_id, name, reference_no, police_station, rank, department, password, username = row
                    officer = PoliceOfficer(name, username, password, reference_no, police_station, rank, department)
                    officer.user_id = int(user_id)
                    users_array.append(officer)

        # Load Postal Clerks
        if os.path.exists(postal_file):
            with open(postal_file, "r", newline="") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    user_id, name, post_office, region, password, username = row
                    clerk = PostalClerk(name, username, password, post_office, region)
                    clerk.user_id = int(user_id)
                    users_array.append(clerk)

        if users_array:
            user_id_sequence = max([user.user_id for user in users_array]) + 1

    except Exception as e:
        print(f"An unexpected error occurred when loading Users: {e}")     

def get_user_by_username_password(username, password):
    for user in users_array:
        if user.username == username and user.password == password:
            return user
    return None