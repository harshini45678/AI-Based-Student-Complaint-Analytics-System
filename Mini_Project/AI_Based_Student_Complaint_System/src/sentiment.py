"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : sentiment.py
Description : Complaint-Aware Sentiment Analysis
=========================================================
"""

from textblob import TextBlob


class SentimentAnalyzer:
    """
    Performs sentiment analysis specifically
    for student complaints.
    """

    def __init__(self):

        # ==========================================
        # NEGATIVE COMPLAINT KEYWORDS AND PHRASES
        # ==========================================

        self.negative_keywords = [

            # General problems
            "not working",
            "not functioning",
            "not coming",
            "not available",
            "unavailable",
            "not updated",
            "not received",
            "not provided",
            "not resolved",
            "not repaired",
            "cannot",
            "can't",
            "unable",

            # Problems and issues
            "problem",
            "issue",
            "error",
            "failed",
            "failure",
            "malfunction",

            # Damage and faults
            "broken",
            "damage",
            "damaged",
            "faulty",

            # Delays
            "delay",
            "delayed",
            "late",
            "pending",

            # Poor service
            "poor",
            "bad",
            "worst",

            # Cleanliness and hygiene
            "dirty",
            "not cleaned",
            "not clean",
            "unclean",
            "uncleaned",
            "not maintained",
            "poor hygiene",
            "hygiene problem",

            # Shortage and insufficient facilities
            "insufficient",
            "inadequate",
            "lack of",
            "lacking",
            "shortage",
            "not enough",
            "limited",
            "missing",
            "overcrowded",

            # Water problems
            "no water",
            "no drinking water",
            "no drinking water available",
            "water not available",
            "without water",
            "lack of water",
            "water problem",
            "water leakage",
            "leakage",
            "leaking",

            # Electricity and technical problems
            "no electricity",
            "no internet",
            "power failure",
            "system down",
            "server down",
            "wifi not working",
            "internet not working",

            # Finance problems
            "payment not updated",
            "fee payment not updated",
            "payment not received",
            "scholarship not received",
            "refund not received",
            "fee problem",
            "payment problem",

            # Complaint dissatisfaction
            "complaint",
            "disturbance",
            "difficulty",
            "difficulties",
            "inconvenience",
            "disappointed",
            "dissatisfied",
            "frustrated",

            # Academic problems
            "not released",
            "not been released",
            "result not released",
            "results not released",
            "timetable not released"
        ]


        # ==========================================
        # POSITIVE EXPRESSIONS
        # ==========================================

        self.positive_keywords = [

            "thank you",
            "excellent",
            "good service",
            "great service",
            "helpful",
            "resolved",
            "fixed",
            "working well",
            "satisfied",
            "happy",
            "appreciate",
            "successfully resolved",
            "problem solved"

        ]


    def predict_sentiment(self, text: str) -> str:
        """
        Predict Positive, Neutral, or Negative sentiment.
        """

        if not isinstance(text, str):

            return "Neutral"


        text_lower = text.lower().strip()


        if text_lower == "":

            return "Neutral"


        # ==========================================
        # NEGATIVE CHECK FIRST
        # ==========================================

        for keyword in self.negative_keywords:

            if keyword in text_lower:

                return "Negative"


        # ==========================================
        # POSITIVE CHECK
        # ==========================================

        for keyword in self.positive_keywords:

            if keyword in text_lower:

                return "Positive"


        # ==========================================
        # TEXTBLOB FALLBACK
        # ==========================================

        polarity = TextBlob(
            text_lower
        ).sentiment.polarity


        if polarity > 0.15:

            return "Positive"


        elif polarity < -0.15:

            return "Negative"


        # ==========================================
        # DEFAULT SENTIMENT
        # ==========================================

        return "Neutral"


    def predict_score(self, text: str) -> float:
        """
        Return TextBlob polarity score.
        """

        if not isinstance(text, str):

            return 0.0


        return TextBlob(
            text.lower()
        ).sentiment.polarity