"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : config.py
Author  : Team
=========================================================
"""

from pathlib import Path

# -----------------------------
# Project Directories
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "data_set"

MODEL_DIR = BASE_DIR / "saved_models"

OUTPUT_DIR = BASE_DIR / "outputs"


# -----------------------------
# Dataset Files
# -----------------------------

# Complaint Classification Dataset
COMPLAINT_DATASET = DATASET_DIR / "university_students_complaints.csv"

# Sentiment Analysis Dataset
SENTIMENT_DATASET = DATASET_DIR / "student_feedback_sentiment.csv"

# Priority Prediction Datasets
PRIORITY_TRAIN_DATASET = DATASET_DIR / "university_query_train.csv"

PRIORITY_TEST_DATASET = DATASET_DIR / "university_query_test.csv"


# -----------------------------
# Random State
# -----------------------------

RANDOM_STATE = 42


# -----------------------------
# Model File Names
# -----------------------------

CATEGORY_MODEL_FILE = MODEL_DIR / "category_model.pkl"

SENTIMENT_MODEL_FILE = MODEL_DIR / "sentiment_model.pkl"

PRIORITY_MODEL_FILE = MODEL_DIR / "priority_model.pkl"


# -----------------------------
# Departments
# -----------------------------

DEPARTMENTS = {
    "Academic": "Academic Department",
    "Administrative": "Administration Department",
    "Finance": "Accounts and Finance Department",
    "Infrastructure": "Maintenance Department",
    "Technical": "IT Support Department"
}


# -----------------------------
# Create Project Folders
# -----------------------------

DATASET_DIR.mkdir(exist_ok=True)

MODEL_DIR.mkdir(exist_ok=True)

OUTPUT_DIR.mkdir(exist_ok=True)


# -----------------------------
# Test Configuration
# -----------------------------

if __name__ == "__main__":

    print("\n===== PROJECT CONFIGURATION =====\n")

    print("Complaint Dataset :", COMPLAINT_DATASET)
    print("Sentiment Dataset :", SENTIMENT_DATASET)
    print("Priority Train    :", PRIORITY_TRAIN_DATASET)
    print("Priority Test     :", PRIORITY_TEST_DATASET)

    print("\nModel Directory   :", MODEL_DIR)
    print("Output Directory  :", OUTPUT_DIR)