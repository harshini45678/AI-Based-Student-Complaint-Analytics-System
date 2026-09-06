"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : preprocess.py
Description : NLP Text Preprocessing using NLTK
=========================================================
"""

import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer


class TextPreprocessor:
    """
    Performs text preprocessing for complaint data.

    Steps:
    1. Lowercase conversion
    2. Remove URLs
    3. Remove email addresses
    4. Remove numbers & special characters
    5. Remove extra spaces
    6. Tokenization
    7. Stopword removal
    8. Lemmatization
    """

    def __init__(self):
        """
        Initialize NLP tools.
        """

        # Initialize tokenizer
        self.tokenizer = TreebankWordTokenizer()

        # Load English stopwords
        self.stop_words = set(stopwords.words("english"))

        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text: str) -> str:
        """
        Clean raw complaint text.
        """

        # Handle missing values
        if not isinstance(text, str):
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r"http\S+", "", text)

        # Remove email addresses
        text = re.sub(r"\S+@\S+", "", text)

        # Remove numbers and special characters
        text = re.sub(r"[^a-zA-Z\s]", " ", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def tokenize(self, text: str):
        """
        Tokenize text into words.
        """

        return self.tokenizer.tokenize(text)

    def remove_stopwords(self, tokens):
        """
        Remove English stopwords.
        """

        return [
            word
            for word in tokens
            if word not in self.stop_words and len(word) > 2
        ]

    def lemmatize(self, tokens):
        """
        Convert words to their base form.
        """

        return [
            self.lemmatizer.lemmatize(word)
            for word in tokens
        ]

    def preprocess(self, text: str) -> str:
        """
        Complete preprocessing pipeline.

        Returns:
            Cleaned complaint text.
        """

        # Clean text
        text = self.clean_text(text)

        # Tokenize
        tokens = self.tokenize(text)

        # Remove stopwords
        tokens = self.remove_stopwords(tokens)

        # Lemmatize
        tokens = self.lemmatize(tokens)

        # Join tokens back into a sentence
        return " ".join(tokens)