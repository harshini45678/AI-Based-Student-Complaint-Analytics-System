"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : storage.py
Description : Complaint Record Storage Module
=========================================================
"""

import csv
import pandas as pd
from datetime import datetime

from src.config import OUTPUT_DIR


class ComplaintStorage:

    def __init__(self):

        # Make sure outputs directory exists
        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file_path = (
            OUTPUT_DIR / "complaint_records.csv"
        )

        # CSV headers
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
            "Status",
            "Suggested_Resolution"
        ]

        # Create file with headers if it does not exist
        if not self.file_path.exists():

            with open(
                self.file_path,
                mode="w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(self.headers)


    # =====================================================
    # GENERATE COMPLAINT ID
    # =====================================================

    def generate_complaint_id(self):

        """
        Generate a unique complaint ID.
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

        return f"CMP-{timestamp}"


    # =====================================================
    # SAVE COMPLAINT
    # =====================================================

    def save_complaint(self, record):

        """
        Save complaint information into CSV.
        """

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

            # Write headers if file is new or empty
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

                "Status":
                    record["Status"],

                "Suggested_Resolution":
                    record["Suggested Resolution"]
            })

        return self.file_path


    # =====================================================
    # UPDATE COMPLAINT STATUS
    # =====================================================

    def update_status(
        self,
        complaint_id,
        new_status
    ):

        """
        Update the status of a complaint.
        """

        # Check whether the file exists
        if not self.file_path.exists():

            return False


        # Read CSV file
        df = pd.read_csv(
            self.file_path
        )


        # Check Complaint_ID column
        if "Complaint_ID" not in df.columns:

            return False


        # Find complaint
        matching_rows = (
            df["Complaint_ID"].astype(str)
            == str(complaint_id)
        )


        # Complaint not found
        if not matching_rows.any():

            return False


        # Update status
        df.loc[
            matching_rows,
            "Status"
        ] = new_status


        # Save updated CSV
        df.to_csv(
            self.file_path,
            index=False
        )


        return True