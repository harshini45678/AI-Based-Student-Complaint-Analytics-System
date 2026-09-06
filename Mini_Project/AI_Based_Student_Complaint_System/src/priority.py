"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : priority.py
Description : Priority Prediction using Complaint Severity
=========================================================
"""

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from src.config import (
    COMPLAINT_DATASET,
    PRIORITY_MODEL_FILE,
    RANDOM_STATE
)

from src.preprocess import TextPreprocessor


class PriorityPredictor:
    """
    Machine Learning model for predicting
    complaint priority based on Severity.
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
        Load the university student complaints dataset.
        """

        df = pd.read_csv(COMPLAINT_DATASET)

        print("\n===== PRIORITY DATASET INFORMATION =====\n")

        print("Dataset Shape:", df.shape)

        print("\nAvailable Columns:")
        print(list(df.columns))

        return df


    def prepare_dataset(self, df):
        """
        Prepare complaint descriptions and severity labels.
        """

        # Remove duplicate complaint descriptions
        df = df.drop_duplicates(
            subset=["Complaint_Description"]
        ).copy()

        # Remove missing values
        df = df.dropna(
            subset=[
                "Complaint_Description",
                "Severity"
            ]
        ).copy()

        # Preprocess complaint text
        df["Cleaned_Text"] = df[
            "Complaint_Description"
        ].apply(
            self.preprocessor.preprocess
        )

        print("\nPriority Distribution:\n")

        print(
            df["Severity"].value_counts()
        )

        return df


    def train(self):
        """
        Train the Priority Prediction Model.
        """

        df = self.load_dataset()

        df = self.prepare_dataset(df)

        X = df["Cleaned_Text"]

        # Severity becomes our Priority Label
        y = df["Severity"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=RANDOM_STATE,

            stratify=y
        )

        print("\nTraining Priority Prediction Model...\n")

        self.model.fit(
            X_train,
            y_train
        )

        predictions = self.model.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print("=" * 60)
        print("PRIORITY PREDICTION MODEL")
        print("=" * 60)

        print(f"\nAccuracy : {accuracy:.4f}")

        print("\nClassification Report:\n")

        print(
            classification_report(
                y_test,
                predictions,
                zero_division=0
            )
        )

        # Save the trained model
        joblib.dump(
            self.model,
            PRIORITY_MODEL_FILE
        )

        print("\nPriority model saved successfully!")

        print(
            "Location:",
            PRIORITY_MODEL_FILE
        )

        return accuracy


if __name__ == "__main__":

    predictor = PriorityPredictor()

    predictor.train()