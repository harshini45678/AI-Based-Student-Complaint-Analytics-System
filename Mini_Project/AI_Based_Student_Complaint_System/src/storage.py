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


# =========================================================
# COMPLAINT STORAGE CLASS
# =========================================================

class ComplaintStorage:

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        # Create outputs directory if it does not exist
        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        # Complaint CSV file path
        self.file_path = (
            OUTPUT_DIR / "complaint_records.csv"
        )

        # CSV Headers
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
    # GENERATE UNIQUE COMPLAINT ID
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

        # Check whether the file already exists
        file_exists = self.file_path.exists()


        # Open CSV file in append mode
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


            # Write headers if file is empty
            if (
                not file_exists
                or self.file_path.stat().st_size == 0
            ):

                writer.writeheader()


            # Write complaint record
            writer.writerow({

                "Complaint_ID":
                    record.get(
                        "Complaint_ID",
                        ""
                    ),

                "Date_Time":
                    record.get(
                        "Date_Time",
                        ""
                    ),

                "Roll_Number":
                    record.get(
                        "Roll_Number",
                        ""
                    ),

                "Student_Department":
                    record.get(
                        "Student_Department",
                        ""
                    ),

                "Year":
                    record.get(
                        "Year",
                        ""
                    ),

                "Semester":
                    record.get(
                        "Semester",
                        ""
                    ),

                "Complaint":
                    record.get(
                        "Complaint",
                        ""
                    ),

                "Category":
                    record.get(
                        "Category",
                        ""
                    ),

                "Sentiment":
                    record.get(
                        "Sentiment",
                        ""
                    ),

                "Priority":
                    record.get(
                        "Priority",
                        ""
                    ),

                "Assigned_Department":
                    record.get(
                        "Department",
                        record.get(
                            "Assigned_Department",
                            "General Administration"
                        )
                    ),

                "Assigned_Staff":
                    record.get(
                        "Assigned_Staff",
                        "Not Assigned"
                    ),

                "Status":
                    record.get(
                        "Status",
                        "Pending"
                    ),

                "Suggested_Resolution":
                    record.get(
                        "Suggested Resolution",
                        record.get(
                            "Suggested_Resolution",
                            ""
                        )
                    ),

                "Resolution_Details":
                    record.get(
                        "Resolution_Details",
                        "Not Resolved Yet"
                    )

            })


        return self.file_path