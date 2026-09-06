"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : storage.py
Description : Complaint Record Storage Module
=========================================================
"""

import csv
from datetime import datetime

from src.config import OUTPUT_DIR


class ComplaintStorage:

    def __init__(self):

        # Create outputs directory if it does not exist
        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file_path = (
            OUTPUT_DIR / "complaint_records.csv"
        )

        self.headers = [

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
            "Assigned_Staff",
            "Status",
            "Suggested_Resolution",
            "Resolution_Details"

        ]

        # Create CSV file if it does not exist
        if not self.file_path.exists():

            with open(
                self.file_path,
                mode="w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    self.headers
                )


    # =====================================================
    # GENERATE COMPLAINT ID
    # =====================================================

    def generate_complaint_id(self):

        timestamp = datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

        return f"CMP-{timestamp}"


    # =====================================================
    # SAVE COMPLAINT
    # =====================================================

    def save_complaint(self, record):

        file_exists = self.file_path.exists()

        with open(
            self.file_path,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.headers
            )

            if (
                not file_exists
                or self.file_path.stat().st_size == 0
            ):

                writer.writeheader()


            writer.writerow({

                "Complaint_ID":
                    record["Complaint_ID"],

                "Date_Time":
                    record["Date_Time"],

                "Roll_Number":
                    record["Roll_Number"],

                "Student_Department":
                    record["Student_Department"],

                "Year":
                    record["Year"],

                "Semester":
                    record["Semester"],

                "Complaint":
                    record["Complaint"],

                "Category":
                    record["Category"],

                "Sentiment":
                    record["Sentiment"],

                "Priority":
                    record["Priority"],

                "Assigned_Department":
                    record["Department"],

                "Assigned_Staff":
                    "Not Assigned",

                "Status":
                    record["Status"],

                "Suggested_Resolution":
                    record["Suggested Resolution"],

                "Resolution_Details":
                    "Not Resolved Yet"

            })

        return self.file_path