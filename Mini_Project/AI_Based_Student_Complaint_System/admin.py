import pandas as pd
from pathlib import Path
from datetime import datetime


# =========================================================
# DATASET
# =========================================================

DATASET_FILE = Path(
    "data_set/student_complaints.csv"
)


# =========================================================
# HEADER
# =========================================================

print("=" * 70)
print("AI STUDENT COMPLAINT - ADMIN PANEL")
print("=" * 70)


# =========================================================
# CHECK DATASET
# =========================================================

if not DATASET_FILE.exists():

    print("\nNo complaint database found.")
    exit()


# =========================================================
# LOAD COMPLAINTS
# =========================================================

df = pd.read_csv(
    DATASET_FILE
)


if df.empty:

    print("\nNo complaints available.")
    exit()


# =========================================================
# DISPLAY COMPLAINTS
# =========================================================

print(
    f"\nTotal Complaints: {len(df)}"
)

display_columns = [
    "Complaint_ID",
    "Student_ID",
    "Complaint_Category",
    "Priority",
    "Sentiment",
    "Status",
    "Assigned_To"
]

print("\n" + "=" * 70)

print(
    df[display_columns].to_string(
        index=False
    )
)

print("\n" + "=" * 70)


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
        "Invalid Complaint ID."
        "\nPlease enter an ID from the list above."
    )


# =========================================================
# FIND COMPLAINT
# =========================================================

index = df[
    df["Complaint_ID"].astype(str)
    == complaint_id
].index[0]


# =========================================================
# DISPLAY SELECTED COMPLAINT
# =========================================================

print("\n" + "=" * 70)
print("SELECTED COMPLAINT")
print("=" * 70)

print(
    "\nComplaint ID:",
    df.loc[index, "Complaint_ID"]
)

print(
    "\nStudent ID:",
    df.loc[index, "Student_ID"]
)

print(
    "\nCategory:",
    df.loc[index, "Complaint_Category"]
)

print(
    "\nPriority:",
    df.loc[index, "Priority"]
)

print(
    "\nSentiment:",
    df.loc[index, "Sentiment"]
)

print(
    "\nCurrent Status:",
    df.loc[index, "Status"]
)

print(
    "\nCurrent Assigned To:",
    df.loc[index, "Assigned_To"]
)


# =========================================================
# ASSIGN STAFF
# =========================================================

assigned_to = input(
    "\nEnter staff member name: "
).strip()


if not assigned_to:

    assigned_to = "Unassigned"


df.loc[
    index,
    "Assigned_To"
] = assigned_to


# =========================================================
# UPDATE STATUS
# =========================================================

print("\nSelect New Status:")

print("1. Open")
print("2. In Progress")
print("3. Resolved")


while True:

    status_choice = input(
        "\nEnter status number: "
    ).strip()


    statuses = {
        "1": "Open",
        "2": "In Progress",
        "3": "Resolved"
    }


    if status_choice in statuses:

        new_status = statuses[
            status_choice
        ]

        break


    print(
        "Invalid choice."
        "\nPlease enter 1, 2, or 3."
    )


df.loc[
    index,
    "Status"
] = new_status

# =========================================================
# RESOLUTION TIME
# =========================================================

if new_status == "Resolved":

    date_reported = pd.to_datetime(
        df.loc[index, "Date_Reported"]
    )

    date_resolved = datetime.now()

    resolution_days = (
        date_resolved.date()
        - date_reported.date()
    ).days

    df.loc[
        index,
        "Resolution_Time_Days"
    ] = resolution_days


# =========================================================
# SAVE CHANGES
# =========================================================

df.to_csv(
    DATASET_FILE,
    index=False
)


# =========================================================
# CONFIRMATION
# =========================================================

print("\n" + "=" * 70)
print("COMPLAINT UPDATED SUCCESSFULLY")
print("=" * 70)

print(
    "\nComplaint ID:",
    complaint_id
)

print(
    "\nAssigned To:",
    assigned_to
)

print(
    "\nStatus:",
    new_status
)

if new_status == "Resolved":

    print(
        "\nResolution Time:",
        int(df.loc[index, "Resolution_Time_Days"]),
        "days"
    )

print("\nChanges saved successfully.")

print("=" * 70)