"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : train_sentiment.py
Description : Train Sentiment Classification Model
=========================================================
"""

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from src.config import (
    SENTIMENT_DATASET,
    SENTIMENT_MODEL_FILE,
    RANDOM_STATE
)

from src.preprocess import TextPreprocessor


class SentimentClassifier:

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

        df = pd.read_csv(SENTIMENT_DATASET)

        print("\nDataset loaded successfully!")
        print("Dataset Shape:", df.shape)

        print("\nAvailable Columns:")
        print(df.columns.tolist())

        return df


    def prepare_dataset(self, df):

        print("\n" + "=" * 60)
        print("Sentiment Dataset Preparation")
        print("=" * 60)

        # Remove missing values
        df = df.dropna(
            subset=["text", "sentiment"]
        ).copy()

        total = len(df)

        # Remove duplicate text records
        df = df.drop_duplicates(
            subset=["text"],
            keep="first"
        ).copy()

        remaining = len(df)

        print(f"Total Records         : {total}")
        print(f"Duplicate Records     : {total - remaining}")
        print(f"Remaining Records     : {remaining}")

        print("=" * 60)

        # Preprocess text
        df["Cleaned_Text"] = df["text"].apply(
            self.preprocessor.preprocess
        )

        # Remove empty text
        df = df[
            df["Cleaned_Text"].str.strip() != ""
        ]

        return df


    def train(self):

        # Load dataset
        df = self.load_dataset()

        # Prepare dataset
        df = self.prepare_dataset(df)

        # Input
        X = df["Cleaned_Text"]

        # Target
        y = df["sentiment"]

        print("\nSentiment Distribution:")
        print(y.value_counts())

        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=RANDOM_STATE,

            stratify=y
        )

        # Train model
        print("\nTraining Sentiment Classification Model...\n")

        self.model.fit(
            X_train,
            y_train
        )

        # Predictions
        predictions = self.model.predict(X_test)

        # Accuracy
        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print("=" * 60)
        print("Sentiment Classification Model")
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

        print("\nConfusion Matrix:\n")

        print(
            confusion_matrix(
                y_test,
                predictions
            )
        )

        # Save model
        joblib.dump(
            self.model,
            SENTIMENT_MODEL_FILE
        )

        print("\nSentiment model saved successfully!")
        print("Location:", SENTIMENT_MODEL_FILE)

        return accuracy


if __name__ == "__main__":

    classifier = SentimentClassifier()

    classifier.train()