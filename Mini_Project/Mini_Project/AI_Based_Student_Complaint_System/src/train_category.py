"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : train_category.py
Description : Train Complaint Category Classification Model
=========================================================
"""

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report

from src.config import (
    COMPLAINT_DATASET,
    CATEGORY_MODEL_FILE,
    RANDOM_STATE
)

from src.preprocess import TextPreprocessor
from src.duplicate import DuplicateRemover


class CategoryClassifier:
    """
    Train Machine Learning model for Complaint Category Prediction.
    """

    def __init__(self):

        self.preprocessor = TextPreprocessor()

        self.duplicate = DuplicateRemover()

        # TF-IDF + LinearSVC is effective for text classification
        self.model = Pipeline([

            (
                "tfidf",
                TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    sublinear_tf=True
                )
            ),

            (
                "classifier",
                LinearSVC(
                    class_weight="balanced",
                    random_state=RANDOM_STATE
                )
            )
        ])


    def load_dataset(self):
        """
        Load complaint dataset.
        """

        df = pd.read_csv(COMPLAINT_DATASET)

        print("\nDataset loaded successfully!")
        print("Dataset Shape:", df.shape)

        print("\nAvailable Columns:")
        print(df.columns.tolist())

        return df


    def prepare_dataset(self, df):
        """
        Clean and preprocess dataset.
        """

        # Remove missing records
        df = df.dropna(
            subset=[
                "Complaint_Description",
                "Category"
            ]
        ).copy()

        # Remove duplicates
        df = self.duplicate.remove_duplicates(df)

        # Preprocess complaint text
        df["Cleaned_Text"] = df[
            "Complaint_Description"
        ].apply(
            self.preprocessor.preprocess
        )

        # Remove empty text
        df = df[
            df["Cleaned_Text"].str.strip() != ""
        ].copy()

        return df


    def train(self):

        # Load dataset
        df = self.load_dataset()

        # Prepare dataset
        df = self.prepare_dataset(df)

        print("\nDataset after preprocessing:", df.shape)

        # Input and target
        X = df["Cleaned_Text"]
        y = df["Category"]

        print("\nCategories found:")
        print(y.value_counts())

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=RANDOM_STATE,

            stratify=y
        )

        print("\nTraining Category Classification Model...\n")

        # Train
        self.model.fit(
            X_train,
            y_train
        )

        # Test predictions
        predictions = self.model.predict(
            X_test
        )

        # Accuracy
        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print("=" * 60)
        print("COMPLAINT CATEGORY CLASSIFICATION MODEL")
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

        # Save model
        joblib.dump(
            self.model,
            CATEGORY_MODEL_FILE
        )

        print("\nCategory model saved successfully!")
        print("Location:", CATEGORY_MODEL_FILE)

        return accuracy


if __name__ == "__main__":

    classifier = CategoryClassifier()

    classifier.train()