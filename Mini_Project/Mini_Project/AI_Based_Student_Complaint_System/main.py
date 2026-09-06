import joblib
import pandas as pd

from datetime import datetime
from pathlib import Path

from src.config import MODEL_DIR
from src.preprocess import TextPreprocessor


# =========================================================
# INITIALIZATION
# =========================================================

preprocessor = TextPreprocessor()


# =========================================================
# LOAD TRAINED MODELS
# =========================================================

category_model = joblib.load(
    MODEL_DIR / "category_model.pkl"
)

sentiment_model = joblib.load(
    MODEL_DIR / "sentiment_model.pkl"
)

priority_model = joblib.load(
    MODEL_DIR / "priority_model.pkl"
)


# =========================================================
# DATASET FILE
# =========================================================

DATASET_FILE = Path(
    "data_set/student_complaints.csv"
)


# =========================================================
# SYSTEM HEADER
# =========================================================

print("=" * 60)
print("AI STUDENT COMPLAINT ANALYSIS SYSTEM")
print("=" * 60)


# =========================================================
# STUDENT ID
# =========================================================

while True:

    student_id = input(
        "\nEnter Student ID: "
    ).strip()

    if student_id:

        break

    print(
        "Student ID cannot be empty."
    )


# =========================================================
# YEAR
# =========================================================

while True:

    year = input(
        "Enter Year (1-4): "
    ).strip()

    if year in ["1", "2", "3", "4"]:

        break

    print(
        "Invalid year. Please enter 1, 2, 3, or 4."
    )


# =========================================================
# COMPLAINT INPUT VALIDATION
# =========================================================

while True:

    complaint = input(
        "\nEnter your complaint: "
    ).strip()


    # Minimum length validation

    if len(complaint) < 10:

        print(
            "\nInvalid complaint."
            "\nPlease enter a meaningful complaint "
            "with at least 10 characters."
        )

        continue


    # Check whether complaint contains letters

    if not any(
        character.isalpha()
        for character in complaint
    ):

        print(
            "\nInvalid complaint."
            "\nPlease enter a complaint using meaningful text."
        )

        continue


    break


# =========================================================
# TEXT PREPROCESSING
# =========================================================

processed = preprocessor.preprocess(
    complaint
)


# =========================================================
# AI CATEGORY PREDICTION
# =========================================================

category = category_model.predict(
    [processed]
)[0]


# =========================================================
# AI SUPPORT TEAM ASSIGNMENT
# =========================================================

support_teams = {

    "Academic":
        "Academic Support",

    "Hostel":
        "Hostel Support",

    "Transport":
        "Transport Support",

    "Library":
        "Library Support",

    "Canteen":
        "Canteen Support",

    "Infrastructure":
        "Infrastructure Support",

    "Laboratory":
        "Laboratory Support",

    "Examination":
        "Examination Support",

    "Placement":
        "Placement Support",

    "IT Support":
        "IT Support Team"
}


assigned_team = support_teams.get(
    category,
    "General Support"
)


# =========================================================
# AI SENTIMENT PREDICTION
# =========================================================

sentiment = sentiment_model.predict(
    [processed]
)[0]


# =========================================================
# AI PRIORITY PREDICTION
# =========================================================

combined_text = (
    category
    + " "
    + sentiment
    + " "
    + processed
)


priority = priority_model.predict(
    [combined_text]
)[0]


# =========================================================
# COMPLAINT DETAILS
# =========================================================

complaint_id = (
    "CMP-"
    + datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )
)


date_reported = datetime.now().strftime(
    "%Y-%m-%d"
)


# =========================================================
# INITIAL STATUS
# =========================================================
# Status is NOT decided by AI.
# Every new complaint starts as Open.
# Admin changes it later.

status = "Open"


# =========================================================
# RESOLUTION INFORMATION
# =========================================================
# These values are filled by the Admin
# when the complaint is resolved.

resolution_time = None

feedback_rating = None


# =========================================================
# CREATE NEW COMPLAINT RECORD
# =========================================================

new_complaint = {

    "Complaint_ID":
        complaint_id,

    "Student_ID":
        student_id,

    "Department":
        category,

    "Year":
        int(year),

    "Complaint_Category":
        category,

    "Complaint_Description":
        complaint,

    "Priority":
        priority,

    "Sentiment":
        sentiment,

    "Status":
        status,

    "Assigned_To":
        assigned_team,

    "Date_Reported":
        date_reported,

    "Resolution_Time_Days":
        resolution_time,

    "Feedback_Rating":
        feedback_rating

}


# =========================================================
# SAVE COMPLAINT TO CSV
# =========================================================

if DATASET_FILE.exists():

    existing_data = pd.read_csv(
        DATASET_FILE
    )

    # Add the new complaint directly
    existing_data.loc[
        len(existing_data)
    ] = new_complaint

    updated_data = existing_data

else:

    updated_data = pd.DataFrame(
        [new_complaint]
    )

# =========================================================
# SAVE COMPLAINT TO CSV
# =========================================================

if DATASET_FILE.exists():

    existing_data = pd.read_csv(
        DATASET_FILE
    )

    # Add the new complaint directly
    existing_data.loc[
        len(existing_data)
    ] = new_complaint

    updated_data = existing_data

else:

    updated_data = pd.DataFrame(
        [new_complaint]
    )


# =========================================================
# SAVE DATASET
# =========================================================

updated_data.to_csv(
    DATASET_FILE,
    index=False
)

# =========================================================
# DISPLAY RESULT
# =========================================================

print(
    "\n"
    + "=" * 60
)

print(
    "COMPLAINT ANALYSIS RESULT"
)

print(
    "=" * 60
)


print(
    "\nComplaint ID:"
)

print(
    complaint_id
)


print(
    "\nStudent ID:"
)

print(
    student_id
)


print(
    "\nYear:"
)

print(
    year
)


print(
    "\nOriginal Complaint:"
)

print(
    complaint
)


print(
    "\nPredicted Category:"
)

print(
    category
)


print(
    "\nPredicted Sentiment:"
)

print(
    sentiment
)


print(
    "\nPredicted Priority:"
)

print(
    priority
)


print(
    "\nAI Assigned Support Team:"
)

print(
    assigned_team
)


print(
    "\nStatus:"
)

print(
    status
)


print(
    "\nDate Reported:"
)

print(
    date_reported
)


print(
    "\nComplaint saved successfully."
)


print(
    "=" * 60
)