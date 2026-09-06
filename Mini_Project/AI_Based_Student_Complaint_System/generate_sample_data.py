import csv
from pathlib import Path
from datetime import datetime, timedelta


# =========================================================
# FILE PATH
# =========================================================

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

file_path = OUTPUT_DIR / "complaint_records.csv"


# =========================================================
# SAMPLE COMPLAINTS
# =========================================================

complaints = [

    # ACADEMIC
    ("The examination timetable has not been released yet.", "Academic", "Negative", "Medium", "Academic Department"),
    ("The semester results are delayed.", "Academic", "Negative", "Medium", "Academic Department"),
    ("The syllabus for the subject has not been provided.", "Academic", "Negative", "Low", "Academic Department"),
    ("There is confusion regarding the examination schedule.", "Academic", "Negative", "Medium", "Academic Department"),
    ("Classes are frequently cancelled without prior notice.", "Academic", "Negative", "Medium", "Academic Department"),
    ("The marks have not been updated in the student portal.", "Academic", "Negative", "Medium", "Academic Department"),


    # INFRASTRUCTURE
    ("There is no drinking water available in our block.", "Infrastructure", "Negative", "Medium", "Maintenance Department"),
    ("The washrooms are not cleaned properly.", "Infrastructure", "Negative", "Medium", "Maintenance Department"),
    ("The classroom fans are not working.", "Infrastructure", "Negative", "Medium", "Maintenance Department"),
    ("There is water leakage from the ceiling.", "Infrastructure", "Negative", "High", "Maintenance Department"),
    ("The lights in the classroom are not working.", "Infrastructure", "Negative", "Low", "Maintenance Department"),
    ("The lift in the academic block is not functioning.", "Infrastructure", "Negative", "Medium", "Maintenance Department"),


    # TECHNICAL
    ("Wi-Fi is not working in the classroom.", "Technical", "Negative", "Medium", "IT Support Department"),
    ("The student portal is not opening.", "Technical", "Negative", "Medium", "IT Support Department"),
    ("The biometric attendance system is not working.", "Technical", "Negative", "Medium", "IT Support Department"),
    ("The computer in the laboratory is not functioning.", "Technical", "Negative", "Medium", "IT Support Department"),
    ("I am unable to log in to the student portal.", "Technical", "Negative", "Medium", "IT Support Department"),
    ("The internet connection is very slow in the computer lab.", "Technical", "Negative", "Low", "IT Support Department"),


    # FINANCE
    ("My fee payment is not updated.", "Finance", "Negative", "Medium", "Accounts and Finance Department"),
    ("The scholarship amount has not been received.", "Finance", "Negative", "Medium", "Accounts and Finance Department"),
    ("I have not received my fee refund yet.", "Finance", "Negative", "Medium", "Accounts and Finance Department"),
    ("There is an incorrect fee amount shown in the portal.", "Finance", "Negative", "Medium", "Accounts and Finance Department"),
    ("My payment status is still showing pending.", "Finance", "Negative", "Medium", "Accounts and Finance Department"),
    ("The fee payment portal is showing an error.", "Finance", "Negative", "Medium", "Accounts and Finance Department"),


    # ADMINISTRATIVE
    ("The library is overcrowded and there are not enough study spaces.", "Administrative", "Negative", "Medium", "Administration Department"),
    ("There is not enough parking space for students.", "Administrative", "Negative", "Medium", "Administration Department"),
    ("The college bus is arriving late regularly.", "Administrative", "Negative", "Medium", "Administration Department"),
    ("The cafeteria is overcrowded during lunch time.", "Administrative", "Negative", "Low", "Administration Department"),
    ("The security staff are not available at the main gate.", "Administrative", "Negative", "Medium", "Administration Department"),
    ("There is poor management of student services.", "Administrative", "Negative", "Medium", "Administration Department"),
]


# =========================================================
# STUDENT DATA
# =========================================================

students = [

    ("22A101", "CSE", "1", "1"),
    ("22A102", "CSM", "2", "1"),
    ("22A103", "AIML", "3", "1"),
    ("22A104", "IT", "2", "1"),
    ("22A105", "AIDS", "4", "1"),
    ("22A106", "ECE", "1", "2"),
    ("22A107", "EEE", "3", "1"),
    ("22A108", "CSD", "2", "2"),
    ("22A109", "MECH", "4", "1"),
    ("22A110", "AUTOMOBILE", "1", "1"),
]


# =========================================================
# CSV HEADERS
# =========================================================

headers = [

    "Complaint_ID",
    "Date_Time",
    "Roll_Number",
    "Student_Department",
    "Year",
    "Semester",
    "Complaint",
    "Category",
    "Sentiment",
    "Priority",
    "Assigned_Department",
    "Status",
    "Suggested_Resolution"
]


# =========================================================
# RESOLUTION GENERATOR
# =========================================================

def get_resolution(category):

    resolutions = {

        "Academic":
        "The Academic Department should investigate the issue and provide a resolution.",

        "Infrastructure":
        "The Maintenance Department should inspect and resolve the issue promptly.",

        "Technical":
        "The IT Support Department should investigate and resolve the technical issue.",

        "Finance":
        "The Accounts and Finance Department should review and resolve the payment issue.",

        "Administrative":
        "The Administration Department should investigate and resolve the issue."
    }

    return resolutions.get(
        category,
        "The concerned department should investigate the issue."
    )


# =========================================================
# CREATE CSV FILE
# =========================================================

with open(
    file_path,
    mode="w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    # Write headers
    writer.writerow(headers)


    # Write 30 complaints
    for i, complaint_data in enumerate(complaints):

        complaint_text = complaint_data[0]
        category = complaint_data[1]
        sentiment = complaint_data[2]
        priority = complaint_data[3]
        department = complaint_data[4]

        # Student details
        student = students[i % len(students)]

        roll_number = student[0]
        student_department = student[1]
        year = student[2]
        semester = student[3]

        # Unique complaint ID
        complaint_id = f"CMP-20260906{100000 + i}"

        # Different timestamps
        date_time = (
            datetime.now() -
            timedelta(minutes=(30 - i) * 5)
        ).strftime("%Y-%m-%d %H:%M:%S")


        # Save row
        writer.writerow([

            complaint_id,
            date_time,
            roll_number,
            student_department,
            year,
            semester,
            complaint_text,
            category,
            sentiment,
            priority,
            department,
            "Pending",
            get_resolution(category)
        ])


print("==============================================")
print("SUCCESS!")
print("30 sample complaints have been created.")
print(f"File saved at: {file_path}")
print("==============================================")