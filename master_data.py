import csv
import os

offence_fines = {}

OFFENSE_FILE = "master_data/offence_fines.csv"

os.makedirs("master_data", exist_ok=True)

def get_next_id():
    if offence_fines:
        return max(offence_fines.keys()) + 1
    return 1

def add_offense(offense, fine_amount):
    offense_id = get_next_id()
    offence_fines[offense_id] = (offense, fine_amount)
    write_offense_fines_to_csv()
    print(f"Offense '{offense}' added with ID {offense_id} and fine {fine_amount}.")

def update_offense(offense_id, new_fine_amount):
    offense_id = int(offense_id)
    if offense_id in offence_fines:
        offense_name, _ = offence_fines[offense_id]
        offence_fines[offense_id] = (offense_name, new_fine_amount)
        write_offense_fines_to_csv()
        print(f"Offense '{offense_name}' (ID {offense_id}) updated to fine {new_fine_amount}.")
    else:
        print(f"Offense ID {offense_id} not found!")

def delete_offense(offense_id):
    offense_id = int(offense_id)
    if offense_id in offence_fines:
        offense_name, _ = offence_fines.pop(offense_id)
        write_offense_fines_to_csv()
        print(f"Offense '{offense_name}' (ID {offense_id}) deleted.")
    else:
        print(f"Offense ID {offense_id} not found!")

def view_all_offenses():
    print("\n***** All Offenses *****")
    print("ID \tOffense \t\t\t\t\t\tFine Amount")
    
    for offense_id, (offense, fine_amount) in offence_fines.items():
        print(f"{offense_id} \t{offense.ljust(30)} \t\t{fine_amount}")

def find_fine_amount(offense):
    for offense_id, (offense_name, fine_amount) in offence_fines.items():
        if offense_name.lower() == offense.lower():
            return fine_amount
    return None        

def write_offense_fines_to_csv():
    try:
        with open(OFFENSE_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Offense", "Fine Amount"])  # Header
            for offense_id, (offense, fine_amount) in offence_fines.items():
                writer.writerow([offense_id, offense, fine_amount])
    except Exception as e:
        print(f"Unexpected error while writing to CSV: {e}")

def load_offense_fines_from_csv():
    try:
        if os.path.exists(OFFENSE_FILE):
            with open(OFFENSE_FILE, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    offense_id, offense, fine_amount = row
                    offence_fines[int(offense_id)] = (offense, float(fine_amount))  # Store as tuple
            print("Offenses loaded successfully!")
        else:
            print("No existing offense fines data found. Starting fresh.")

    except Exception as e:
        print(f"Unexpected error while reading CSV: {e}")
