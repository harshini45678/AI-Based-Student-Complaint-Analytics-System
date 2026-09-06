"""
Common utility functions
"""

from pathlib import Path
import pandas as pd


def create_directory(path: Path):
    """
    Creates directory if it doesn't exist.
    """
    path.mkdir(parents=True, exist_ok=True)


def save_dataframe(df: pd.DataFrame, filepath: Path):
    """
    Save dataframe as CSV.
    """
    df.to_csv(filepath, index=False)


def load_dataframe(filepath: Path):
    """
    Load CSV into DataFrame.
    """
    return pd.read_csv(filepath)


def print_title(title):
    print("=" * 60)
    print(title)
    print("=" * 60)