import csv
import os
from datetime import datetime
from master_data import find_fine_amount
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


VIOLATION_FILE = "./violation_data/violation_records.csv"
os.makedirs("violation_data", exist_ok=True)  

violation_records = []
violation_id_sequence = 1

class Violation:
    def __init__(self, driver_name, vehicle_no, date_of_offense, place, offense, license_no, court, court_date, police_station, issuing_officer, email, notify_method, paid_status, fine_amount):
        self.id = violation_id_sequence

        self.driver_name = driver_name
        self.vehicle_no = vehicle_no
        self.date_of_offense = date_of_offense
        self.place = place
        self.offense = offense
        self.license_no = license_no
        self.court = court
        self.court_date = court_date
        self.police_station = police_station
        self.issuing_officer = issuing_officer
        self.email = email
        self.notify_method = notify_method
        self.paid_status = paid_status
        self.fine_amount = fine_amount
        self.is_court_case = court.strip() != ""



def write_violations_to_csv():
    try:
        with open(VIOLATION_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "ID", "Driver Name", "Vehicle No", "Date of Offense", "Place", "Offense",
                "License No", "Court", "Court Date", "Police Station", "Issuing Officer",
                "Email", "Notify Method", "Fine Amount", "isCourtCase"
            ])
            for violation in violation_records:
                writer.writerow([violation.id, violation.driver_name, violation.vehicle_no, violation.date_of_offense, violation.place, violation.offense, violation.license_no, violation.court, violation.court_date, violation.police_station, violation.issuing_officer, violation.email, violation.notify_method, violation.fine_amount, violation.is_court_case])
    except Exception as e:
        print(f"Error writing violations to CSV: {e}")

def load_violations_from_csv():
    global violation_id_sequence
    try:
        if os.path.exists(VIOLATION_FILE):
            with open(VIOLATION_FILE, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    violation = Violation(
                        row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]
                    )
                    violation_records.append(violation)

                if violation_records:
                    violation_id_sequence = max(v.id for v in violation_records) + 1
        else:
            print("No existing violation records found. Starting fresh.")
    except Exception as e:
        print(f"Error loading violations from CSV: {e}")


def add_violation():
    global violation_id_sequence

    print("\n***** Add New Violation *****")
    
    try:
        full_name = input("Enter Driver's Full Name: ")
        vehicle_no = input("Enter Vehicle Number: ")
        date_of_offense = input("Enter Date of Offense (YYYY-MM-DD): ")
        place = input("Enter Place of Offense: ")
        offense = input("Enter Offense: ")
        driving_license_no = input("Enter Driving License Number: ")
        court = input("Enter Court (Leave empty if not applicable): ")
        court_date = input("Enter Court Date (YYYY-MM-DD, Leave empty if not applicable): ")
        police_station = input("Enter Police Station: ")
        issuing_officer = input("Enter Issuing Officer Name: ")
        notify_method = input("Enter Notification Method (email/none): ").strip().lower()
        if notify_method == "email":
            email = input("Enter Driver's Email: ")
        else:
            email = ""    
        is_court_case = court.strip() != ""  # If court is provided, it's a court case
        amount = find_fine_amount(offense)

        # Create violation record
        violation = Violation(full_name, vehicle_no, date_of_offense, place, offense, driving_license_no, court, court_date, police_station, issuing_officer, email, notify_method, False, amount)

        violation_records.append(violation)
        violation_id_sequence += 1

        write_violations_to_csv()

        print("Violation added successfully!")

        # Send email if notify method is "email"
        if notify_method == "email" and email:
            send_violation_email(violation_id_sequence, email, offense, amount, vehicle_no, driving_license_no)

    except ValueError:
        print("Invalid input. Please enter correct values.")

# View all violations
def view_violations():
    print("\n***** Violation Records *****")
    print("#ID  | Driver Name | Vehicle No | Date | Place | Offense | License No | Court | Court Date | Police Station | Officer | Paid Status")

    for v in violation_records:
        print(f"{v.id} | {v.driver_name} | {v.vehicle_no} | {v.date_of_offense} | {v.place} | {v.offense} | {v.license_no} | {v.court} | {v.court_date} | {v.police_station} | {v.issuing_officer} | {v.paid_status}")

def make_payment(violation_id, amount):
    violation_id = int(violation_id)
    for v in violation_records:
        if v.id == violation_id and not v.paid_status and amount >= v.fine_amount:
            v.paid_status = True
            write_violations_to_csv()
            print(f"Violation record {violation_id} updated successfully!")
            return
        elif v.id == violation_id and not v.paid_status and amount < v.fine_amount:
            print(f"Amount paid is less than the fine amount. Please pay the full fine amount of ${v.fine_amount}.")
    print(f"Violation ID {violation_id} not found!")


def delete_violation(violation_id):
    global violation_records
    violation_id = int(violation_id)
    violation_records = [v for v in violation_records if v.id != violation_id]
    write_violations_to_csv()
    print(f"Violation record {violation_id} deleted successfully!")





def send_violation_email(id, email, offense, amount, vehicle_no, driving_license_no):
    global SENDGRID_API_KEY

    message = Mail(
        from_email="trafficguard2@gmail.com",
        to_emails=email,
        subject="Traffic Violation Notice",
        html_content=f"""
        <p>Dear Driver,</p>
        <p>You have been fined for the following offense: <b>{offense}</b>.</p>
        <p><b>Reference:</b> {id}</p>
        <p><b>Fine Amount:</b> ${amount}</p>
        <p><b>Vehicle Number:</b> {vehicle_no}</p>
        <p><b>Driving License Number:</b> {driving_license_no}</p>
        <p>Please make the payment before the due date to avoid further penalties.</p>
        <p>Thank you.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {email}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")