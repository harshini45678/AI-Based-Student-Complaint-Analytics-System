"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : train_classifier.py
Description : Train Priority Classification Model
=========================================================
"""

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from src.config import (
    DATASET_FILE,
    MODEL_DIR,
    RANDOM_STATE
)

from src.preprocess import TextPreprocessor


class ComplaintClassifier:
    """
    Train Machine Learning model for Priority Prediction.
    """

    def __init__(self):

        self.preprocessor = TextPreprocessor()

        self.model = Pipeline([

            (
                "tfidf",
                TfidfVectorizer(
                    max_features=5000
                )
            ),

            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    random_state=RANDOM_STATE,
                    class_weight="balanced"
                )
            )
        ])

    def load_dataset(self):
        """
        Load complaint dataset.
        """

        return pd.read_csv(DATASET_FILE)

    def prepare_dataset(self, df):
        """
        Remove duplicate complaints and prepare
        combined text using category, sentiment,
        and complaint description.
        """

        print("=" * 60)
        print("Duplicate Complaint Report")
        print("=" * 60)

        total_complaints = len(df)

        # Remove duplicate complaint descriptions
        df = df.drop_duplicates(
            subset=["Complaint_Description"],
            keep="first"
        ).copy()

        remaining_complaints = len(df)

        duplicate_records = (
            total_complaints - remaining_complaints
        )

        print(
            f"Total Complaints      : {total_complaints}"
        )

        print(
            f"Duplicate Records     : {duplicate_records}"
        )

        print(
            f"Remaining Complaints  : {remaining_complaints}"
        )

        print("=" * 60)

        # Preprocess complaint description
        df["Cleaned_Description"] = df[
            "Complaint_Description"
        ].apply(
            self.preprocessor.preprocess
        )

        # Combine useful features
        df["Combined_Text"] = (
            df["Complaint_Category"].astype(str)
            + " "
            + df["Sentiment"].astype(str)
            + " "
            + df["Cleaned_Description"]
        )

        return df

    def train(self):

        # Load dataset
        df = self.load_dataset()

        # Prepare dataset
        df = self.prepare_dataset(df)

        # Input features
        X = df["Combined_Text"]

        # Target
        y = df["Priority"]

        # Train/Test split
        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=RANDOM_STATE,

            stratify=y
        )

        # Train model
        self.model.fit(
            X_train,
            y_train
        )

        # Predictions
        predictions = self.model.predict(
            X_test
        )

        # Accuracy
        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print("=" * 60)
        print("Priority Prediction Model - Model 2")
        print("=" * 60)

        print(
            f"Accuracy : {accuracy:.4f}"
        )

        print("\nClassification Report\n")

        print(
            classification_report(
                y_test,
                predictions,
                zero_division=0
            )
        )

        print("\nConfusion Matrix\n")

        print(
            confusion_matrix(
                y_test,
                predictions
            )
        )

        # Save model
        MODEL_DIR.mkdir(
            exist_ok=True
        )

        joblib.dump(
            self.model,
            MODEL_DIR / "priority_model.pkl"
        )

        print("\nModel saved successfully.")

        return accuracy


if __name__ == "__main__":

    classifier = ComplaintClassifier()

    classifier.train()