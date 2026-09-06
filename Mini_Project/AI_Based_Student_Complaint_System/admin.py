"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : admin.py
Description : Admin Complaint Management Panel
=========================================================
"""

import pandas as pd
from pathlib import Path


# =========================================================
# COMPLAINT FILE
# =========================================================

COMPLAINT_FILE = Path(
    "outputs/complaint_records.csv"
)


# =========================================================
# HEADER
# =========================================================

print("\n" + "=" * 75)
print("AI-BASED STUDENT COMPLAINT ANALYTICS SYSTEM")
print("ADMIN COMPLAINT MANAGEMENT PANEL")
print("=" * 75)


# =========================================================
# CHECK FILE
# =========================================================

if not COMPLAINT_FILE.exists():

    print("\n❌ No complaint records found.")

    exit()


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(COMPLAINT_FILE)

df.columns = (
    df.columns.astype(str).str.strip()
)


# =========================================================
# CHECK EMPTY
# =========================================================

if df.empty:

    print("\n⚠️ No complaints available.")

    exit()


# =========================================================
# ADD ASSIGNED STAFF COLUMN IF MISSING
# =========================================================

if "Assigned_Staff" not in df.columns:

    df["Assigned_Staff"] = "Not Assigned"

else:

    df["Assigned_Staff"] = (
        df["Assigned_Staff"]
        .fillna("Not Assigned")
    )


# =========================================================
# ADD RESOLUTION DETAILS COLUMN IF MISSING
# =========================================================

if "Resolution_Details" not in df.columns:

    df["Resolution_Details"] = "Not Resolved"

else:

    df["Resolution_Details"] = (
        df["Resolution_Details"]
        .fillna("Not Resolved")
    )


# =========================================================
# DISPLAY COMPLAINTS
# =========================================================

print(f"\nTotal Complaints: {len(df)}")

print("\n" + "=" * 75)
print("ALL COMPLAINT RECORDS")
print("=" * 75)


display_columns = [

    "Complaint_ID",
    "Roll_Number",
    "Student_Department",
    "Category",
    "Priority",
    "Sentiment",
    "Assigned_Department",
    "Assigned_Staff",
    "Status"

]


available_columns = [

    column

    for column in display_columns

    if column in df.columns
]


print(

    df[available_columns].to_string(
        index=False
    )

)


print("\n" + "=" * 75)


# =========================================================
# SELECT COMPLAINT
# =========================================================

while True:

    complaint_id = input(
        "\nEnter Complaint ID to manage: "
    ).strip()


    if complaint_id in df["Complaint_ID"].astype(str).values:

        break


    print(
        "\n❌ Invalid Complaint ID."
    )


# =========================================================
# FIND COMPLAINT
# =========================================================

index = df[

    df["Complaint_ID"]
    .astype(str)
    == complaint_id

].index[0]


# =========================================================
# DISPLAY COMPLAINT DETAILS
# =========================================================

print("\n" + "=" * 75)
print("SELECTED COMPLAINT")
print("=" * 75)


print(
    "\nComplaint ID:",
    df.loc[index, "Complaint_ID"]
)

print(
    "Roll Number:",
    df.loc[index, "Roll_Number"]
)

print(
    "Student Department:",
    df.loc[index, "Student_Department"]
)

print(
    "Category:",
    df.loc[index, "Category"]
)

print(
    "Priority:",
    df.loc[index, "Priority"]
)

print(
    "Sentiment:",
    df.loc[index, "Sentiment"]
)

print(
    "Assigned Department:",
    df.loc[index, "Assigned_Department"]
)

print(
    "Assigned Staff:",
    df.loc[index, "Assigned_Staff"]
)

print(
    "Current Status:",
    df.loc[index, "Status"]
)

print(
    "\nComplaint:",
    df.loc[index, "Complaint"]
)


# =========================================================
# DISPLAY RESOLUTION DETAILS
# =========================================================

if str(df.loc[index, "Status"]).strip() == "Resolved":

    print(
        "\nResolution Details:",
        df.loc[index, "Resolution_Details"]
    )


# =========================================================
# ASSIGN STAFF
# =========================================================

print("\n" + "=" * 75)
print("ASSIGN STAFF MEMBER")
print("=" * 75)


current_staff = df.loc[
    index,
    "Assigned_Staff"
]


print(
    "\nCurrent Staff:",
    current_staff
)


staff_name = input(
    "\nEnter Staff Member Name: "
).strip()


# Keep current staff if empty

if staff_name == "":

    staff_name = current_staff


df.loc[
    index,
    "Assigned_Staff"
] = staff_name


# =========================================================
# UPDATE STATUS
# =========================================================

print("\n" + "=" * 75)
print("SELECT NEW STATUS")
print("=" * 75)

print("\n1. Pending")
print("2. In Progress")
print("3. Resolved")


statuses = {

    "1": "Pending",

    "2": "In Progress",

    "3": "Resolved"

}


while True:

    status_choice = input(
        "\nEnter status number (1-3): "
    ).strip()


    if status_choice in statuses:

        new_status = statuses[
            status_choice
        ]

        break


    print(
        "\n❌ Invalid choice."
    )


# =========================================================
# UPDATE STATUS
# =========================================================

df.loc[
    index,
    "Status"
] = new_status


# =========================================================
# ENTER RESOLUTION DETAILS
# =========================================================

if new_status == "Resolved":

    print("\n" + "=" * 75)
    print("ENTER RESOLUTION DETAILS")
    print("=" * 75)


    while True:

        resolution_details = input(
            "\nEnter Resolution Details: "
        ).strip()


        if resolution_details != "":

            break


        print(
            "\n❌ Resolution details cannot be empty."
        )


    df.loc[
        index,
        "Resolution_Details"
    ] = resolution_details


else:

    # If complaint is not resolved,
    # keep Resolution Details as Not Resolved

    if str(
        df.loc[index, "Resolution_Details"]
    ).strip() == "":

        df.loc[
            index,
            "Resolution_Details"
        ] = "Not Resolved"


# =========================================================
# SAVE DATA
# =========================================================

df.to_csv(
    COMPLAINT_FILE,
    index=False
)


# =========================================================
# SUCCESS MESSAGE
# =========================================================

print("\n" + "=" * 75)
print("✅ COMPLAINT UPDATED SUCCESSFULLY")
print("=" * 75)


print(
    "\nComplaint ID:",
    complaint_id
)

print(
    "Assigned Staff:",
    staff_name
)

print(
    "New Status:",
    new_status
)


if new_status == "Resolved":

    print(
        "Resolution Details:",
        resolution_details
    )


print(
    "\nChanges saved successfully!"
)

print(
    "\nThe updated information will now appear"
)

print(
    "in the Complaint Dashboard."
)

print("=" * 75)