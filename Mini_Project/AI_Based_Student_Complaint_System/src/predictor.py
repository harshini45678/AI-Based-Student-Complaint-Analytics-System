"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : predictor.py
Description : Main AI Complaint Analytics and Resolution System
=========================================================
"""

import joblib
from datetime import datetime

from src.config import MODEL_DIR
from src.sentiment import SentimentAnalyzer
from src.resolution import ResolutionRecommender
from src.storage import ComplaintStorage


class ComplaintPredictor:

    def __init__(self):

        print("\nLoading AI models...")

        # Load Category Classification Model
        self.category_model = joblib.load(
            MODEL_DIR / "category_model.pkl"
        )

        # Load Priority Prediction Model
        self.priority_model = joblib.load(
            MODEL_DIR / "priority_model.pkl"
        )

        # Initialize Sentiment Analyzer
        self.sentiment_analyzer = SentimentAnalyzer()

        # Initialize Resolution Recommender
        self.resolution_recommender = ResolutionRecommender()

        # Initialize Complaint Storage
        self.storage = ComplaintStorage()

        print("All AI models loaded successfully!")


    def adjust_category(self, complaint, ml_category):

        text = complaint.lower()

        # ==========================================
        # ACADEMIC CATEGORY
        # ==========================================

        academic_keywords = [

            "exam",
            "examination",
            "timetable",
            "exam schedule",
            "result",
            "marks",
            "grade",
            "course",
            "subject",
            "teacher",
            "professor",
            "faculty",
            "lecturer",
            "adviser",
            "advisor",
            "syllabus",
            "class schedule"

        ]

        for keyword in academic_keywords:

            if keyword in text:
                return "Academic"


        # ==========================================
        # FINANCE CATEGORY
        # ==========================================

        finance_keywords = [

            "fee",
            "fees",
            "payment",
            "scholarship",
            "refund",
            "tuition",
            "fine",
            "money"

        ]

        for keyword in finance_keywords:

            if keyword in text:
                return "Finance"


        # ==========================================
        # TECHNICAL CATEGORY
        # ==========================================

        technical_keywords = [

            "wifi",
            "wi-fi",
            "internet",
            "network",
            "computer",
            "software",
            "portal",
            "website",
            "server",
            "login",
            "password",
            "application",
            "system error",
            "biometric",
            "biometrics",
            "fingerprint",
            "attendance system",
            "biometric system"

        ]

        for keyword in technical_keywords:

            if keyword in text:
                return "Technical"


        # ==========================================
        # INFRASTRUCTURE CATEGORY
        # ==========================================

        infrastructure_keywords = [

            "water",
            "leakage",
            "leaking",
            "electricity",
            "power",
            "fan",
            "fans",
            "air conditioner",
            "washroom",
            "bathroom",
            "hostel room",
            "ceiling",
            "lift",
            "furniture",
            "building",
            "projector",
            "chair",
            "desk",
            "light",
            "lights"

        ]

        for keyword in infrastructure_keywords:

            if keyword in text:
                return "Infrastructure"


        # ==========================================
        # ADMINISTRATIVE CATEGORY
        # ==========================================

        administrative_keywords = [

            "library",
            "discipline",
            "administration",
            "security",
            "parking",
            "cafeteria",
            "canteen",
            "bus",
            "transport",
            "student services"

        ]

        for keyword in administrative_keywords:

            if keyword in text:
                return "Administrative"


        # If no keyword rule matches,
        # use Machine Learning prediction

        return ml_category


    def get_department(self, category):

        department_mapping = {

            "Academic": "Academic Department",

            "Administrative": "Administration Department",

            "Finance": "Accounts and Finance Department",

            "Infrastructure": "Maintenance Department",

            "Technical": "IT Support Department"

        }

        return department_mapping.get(
            category,
            "General Administration"
        )


    def adjust_priority(
        self,
        complaint,
        category,
        ml_priority
    ):

        text = complaint.lower()

        # ==========================================
        # URGENT SAFETY CONDITIONS
        # ==========================================

        urgent_keywords = [

            "fire",
            "smoke",
            "electric shock",
            "electrocution",
            "gas leak",
            "gas leakage",
            "collapsed",
            "collapse",
            "life threatening"

        ]

        for keyword in urgent_keywords:

            if keyword in text:
                return "Urgent"


        # ==========================================
        # HIGH PRIORITY INFRASTRUCTURE
        # ==========================================

        high_keywords = [

            "water leakage",
            "water leaking",
            "flooding",
            "flood",
            "no water",
            "water is not coming",
            "no electricity",
            "power failure",
            "short circuit",
            "broken ceiling"

        ]

        if category == "Infrastructure":

            for keyword in high_keywords:

                if keyword in text:
                    return "High"


        # ==========================================
        # MEDIUM PRIORITY ACADEMIC
        # ==========================================

        academic_medium_keywords = [

            "timetable",
            "exam timetable",
            "examination timetable",
            "result not released",
            "results not released",
            "not been released",
            "schedule delay",
            "facing difficulties"

        ]

        if category == "Academic":

            for keyword in academic_medium_keywords:

                if keyword in text:
                    return "Medium"


        # ==========================================
        # MEDIUM PRIORITY TECHNICAL
        # ==========================================

        technical_medium_keywords = [

            "biometric",
            "fingerprint",
            "attendance system",
            "system not working",
            "server down",
            "portal not working",
            "login problem"

        ]

        if category == "Technical":

            for keyword in technical_medium_keywords:

                if keyword in text:
                    return "Medium"


        # ==========================================
        # MEDIUM PRIORITY FINANCE
        # ==========================================

        finance_medium_keywords = [

            "fee problem",
            "payment problem",
            "payment issue",
            "payment not updated",
            "refund",
            "scholarship"

        ]

        if category == "Finance":

            for keyword in finance_medium_keywords:

                if keyword in text:
                    return "Medium"


        # ==========================================
        # PREVENT UNREASONABLE URGENT PREDICTION
        # ==========================================

        if ml_priority == "Urgent":

            return "Medium"


        return ml_priority


    def predict(self, complaint):

        # ==========================================
        # CATEGORY PREDICTION
        # ==========================================

        ml_category = self.category_model.predict(
            [complaint]
        )[0]

        category = self.adjust_category(
            complaint,
            ml_category
        )


        # ==========================================
        # SENTIMENT PREDICTION
        # ==========================================

        sentiment = self.sentiment_analyzer.predict_sentiment(
            complaint
        )


        # ==========================================
        # PRIORITY PREDICTION
        # ==========================================

        ml_priority = self.priority_model.predict(
            [complaint]
        )[0]

        priority = self.adjust_priority(
            complaint,
            category,
            ml_priority
        )


        # ==========================================
        # DEPARTMENT ASSIGNMENT
        # ==========================================

        department = self.get_department(
            category
        )


        # ==========================================
        # RESOLUTION RECOMMENDATION
        # ==========================================

        resolution = self.resolution_recommender.recommend(
            category,
            priority
        )


        return {

            "Complaint": complaint,

            "Category": category,

            "Sentiment": sentiment,

            "Priority": priority,

            "Department": department,

            "Suggested Resolution": resolution

        }


# =========================================================
# MAIN FUNCTION
# =========================================================

def main():

    predictor = ComplaintPredictor()

    print("\n" + "=" * 65)

    print(
        "AI-BASED STUDENT COMPLAINT ANALYTICS AND RESOLUTION SYSTEM"
    )

    print("=" * 65)


    # ==========================================
    # STUDENT DETAILS
    # ==========================================

    print("\n===== STUDENT DETAILS =====\n")


    # ------------------------------------------
    # ROLL NUMBER VALIDATION
    # ------------------------------------------

    while True:

        roll_number = input(
            "Enter Roll Number: "
        ).strip()

        if roll_number:

            break

        print(
            "\nRoll Number cannot be empty!"
        )


    # ------------------------------------------
    # STUDENT DEPARTMENT VALIDATION
    # ------------------------------------------

    valid_departments = [

        "IT",
        "CSE",
        "CSD",
        "CSM",
        "AIML",
        "AIDS",
        "EEE",
        "ECM",
        "ECE",
        "MECH",
        "AUTOMOBILE"

    ]


    while True:

        student_department = input(
            "Enter Student Department: "
        ).strip().upper()

        if student_department in valid_departments:

            break

        print("\nInvalid Department!")

        print(
            "Please enter one of the following departments:"
        )

        print(
            ", ".join(valid_departments)
        )

        print()


    # ------------------------------------------
    # YEAR VALIDATION
    # ------------------------------------------

    valid_years = [

        "1",
        "2",
        "3",
        "4"

    ]


    while True:

        year = input(
            "Enter Year (1-4): "
        ).strip()

        if year in valid_years:

            break

        print(
            "\nInvalid Year! Please enter 1, 2, 3, or 4."
        )


    # ------------------------------------------
    # SEMESTER VALIDATION
    # ------------------------------------------

    valid_semesters = [

        "1",
        "2"

    ]


    while True:

        semester = input(
            "Enter Semester (1 or 2): "
        ).strip()

        if semester in valid_semesters:

            break

        print(
            "\nInvalid Semester! Please enter 1 or 2."
        )


    # ==========================================
    # COMPLAINT DETAILS
    # ==========================================

    print("\n===== COMPLAINT DETAILS =====\n")


    # ------------------------------------------
    # COMPLAINT VALIDATION
    # ------------------------------------------

    while True:

        complaint = input(
            "Enter Student Complaint: "
        ).strip()

        if complaint:

            break

        print(
            "\nComplaint cannot be empty!"
        )


    # ==========================================
    # AI ANALYSIS
    # ==========================================

    result = predictor.predict(
        complaint
    )


    # ==========================================
    # RECORD INFORMATION
    # ==========================================

    complaint_id = predictor.storage.generate_complaint_id()

    date_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    status = "Pending"


    # ==========================================
    # CREATE COMPLETE RECORD
    # ==========================================

    record = {

        "Complaint_ID": complaint_id,

        "Date_Time": date_time,

        "Roll_Number": roll_number,

        "Student_Department": student_department,

        "Year": year,

        "Semester": semester,

        "Complaint": result["Complaint"],

        "Category": result["Category"],

        "Sentiment": result["Sentiment"],

        "Priority": result["Priority"],

        "Department": result["Department"],

        "Status": status,

        "Suggested Resolution":
            result["Suggested Resolution"]

    }


    # ==========================================
    # SAVE RECORD
    # ==========================================

    file_path = predictor.storage.save_complaint(
        record
    )


    # ==========================================
    # DISPLAY RESULT
    # ==========================================

    print("\n" + "=" * 65)

    print(
        "STUDENT COMPLAINT ANALYSIS RESULT"
    )

    print("=" * 65)


    print(f"\nComplaint ID       : {complaint_id}")

    print(f"Date & Time        : {date_time}")


    print("\n----- STUDENT DETAILS -----")

    print(f"Roll Number        : {roll_number}")

    print(
        f"Student Department : {student_department}"
    )

    print(f"Year               : {year}")

    print(f"Semester           : {semester}")


    print("\n----- COMPLAINT ANALYSIS -----")

    print(
        f"Complaint          : {result['Complaint']}"
    )

    print(
        f"Category           : {result['Category']}"
    )

    print(
        f"Sentiment          : {result['Sentiment']}"
    )

    print(
        f"Priority           : {result['Priority']}"
    )

    print(
        f"Assigned Department: {result['Department']}"
    )

    print(
        f"Status             : {status}"
    )


    print("\n----- SUGGESTED RESOLUTION -----\n")

    print(
        result["Suggested Resolution"]
    )


    print("\nComplaint saved successfully!")

    print(
        "Saved File:",
        file_path
    )


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":

    main()