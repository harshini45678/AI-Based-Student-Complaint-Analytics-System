"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : duplicate.py
Description : Duplicate Complaint Detection and Removal
=========================================================
"""

import pandas as pd


class DuplicateRemover:
    """
    Detect duplicate complaint records.
    """

    def __init__(self):
        pass

    def count_duplicates(self, df: pd.DataFrame) -> int:
        """
        Count duplicate complaint descriptions.
        """

        return df.duplicated(
            subset=["Complaint_Description"]
        ).sum()

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove only completely identical records.
        """


        total = len(df)

        duplicates = df.duplicated().sum()

        print("=" * 60)
        print("Duplicate Complaint Report")
        print("=" * 60)
        print(f"Total Complaints      : {total}")
        print(f"Duplicate Records     : {duplicates}")

        df = df.drop_duplicates()

        print(f"Remaining Complaints  : {len(df)}")
        print("=" * 60)

        return df.reset_index(drop=True)