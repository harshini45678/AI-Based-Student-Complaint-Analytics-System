"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : app.py
Description : Streamlit Web Application
=========================================================
"""

import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

from datetime import datetime
from pathlib import Path

from src.config import MODEL_DIR
from src.sentiment import SentimentAnalyzer
from src.resolution import ResolutionRecommender
from src.storage import ComplaintStorage


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Complaint Analytics System",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# STUDENT DEPARTMENTS
# =========================================================

STUDENT_DEPARTMENTS = [
    "IT",
    "CSE",
    "CSD",
    "CSM",
    "AIML",
    "AIDS",
    "EEE",
    "ECM",
    "ECE",
    "MECH",
    "AUTOMOBILE"
]


# =========================================================
# LOAD AI MODELS
# =========================================================

@st.cache_resource
def load_models():

    category_model = joblib.load(
        MODEL_DIR / "category_model.pkl"
    )

    priority_model = joblib.load(
        MODEL_DIR / "priority_model.pkl"
    )

    sentiment_analyzer = SentimentAnalyzer()

    resolution_recommender = ResolutionRecommender()

    storage = ComplaintStorage()

    return (
        category_model,
        priority_model,
        sentiment_analyzer,
        resolution_recommender,
        storage
    )


# =========================================================
# CATEGORY ADJUSTMENT
# =========================================================

def adjust_category(complaint, ml_category):

    text = complaint.lower()

    academic_keywords = [
        "exam",
        "examination",
        "timetable",
        "exam schedule",
        "result",
        "marks",
        "grade",
        "course",
        "subject",
        "teacher",
        "professor",
        "faculty",
        "lecturer",
        "adviser",
        "advisor",
        "syllabus",
        "class schedule"
    ]

    for keyword in academic_keywords:
        if keyword in text:
            return "Academic"


    finance_keywords = [
        "fee",
        "fees",
        "payment",
        "scholarship",
        "refund",
        "tuition",
        "fine",
        "money"
    ]

    for keyword in finance_keywords:
        if keyword in text:
            return "Finance"


    technical_keywords = [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "computer",
        "software",
        "portal",
        "website",
        "server",
        "login",
        "password",
        "application",
        "system error",
        "biometric",
        "fingerprint",
        "attendance system",
        "mouse",
        "keyboard",
        "lab computer"
    ]

    for keyword in technical_keywords:
        if keyword in text:
            return "Technical"


    infrastructure_keywords = [
        "water",
        "drinking water",
        "leakage",
        "leaking",
        "electricity",
        "power",
        "fan",
        "air conditioner",
        "washroom",
        "washrooms",
        "bathroom",
        "hostel room",
        "ceiling",
        "lift",
        "furniture",
        "building",
        "projector",
        "chair",
        "desk",
        "light",
        "lights"
    ]

    for keyword in infrastructure_keywords:
        if keyword in text:
            return "Infrastructure"


    administrative_keywords = [
        "library",
        "discipline",
        "administration",
        "security",
        "parking",
        "cafeteria",
        "canteen",
        "bus",
        "transport",
        "student services"
    ]

    for keyword in administrative_keywords:
        if keyword in text:
            return "Administrative"


    return ml_category


# =========================================================
# DEPARTMENT ASSIGNMENT
# =========================================================

def get_assigned_department(category):

    department_mapping = {

        "Academic": "Academic Department",

        "Administrative": "Administration Department",

        "Finance": "Accounts and Finance Department",

        "Infrastructure": "Maintenance Department",

        "Technical": "IT Support Department"
    }

    return department_mapping.get(
        category,
        "General Administration"
    )


# =========================================================
# PRIORITY ADJUSTMENT
# =========================================================

def adjust_priority(
    complaint,
    category,
    ml_priority
):

    text = complaint.lower()


    urgent_keywords = [
        "fire",
        "smoke",
        "electric shock",
        "electrocution",
        "gas leak",
        "gas leakage",
        "collapsed",
        "collapse",
        "life threatening"
    ]

    for keyword in urgent_keywords:
        if keyword in text:
            return "Urgent"


    high_keywords = [
        "water leakage",
        "water leaking",
        "flooding",
        "flood",
        "no water",
        "water is not coming",
        "no electricity",
        "power failure",
        "short circuit",
        "broken ceiling"
    ]

    if category == "Infrastructure":

        for keyword in high_keywords:
            if keyword in text:
                return "High"


    academic_medium_keywords = [
        "timetable",
        "exam timetable",
        "examination timetable",
        "result not released",
        "results not released",
        "not been released",
        "schedule delay",
        "facing difficulties"
    ]

    if category == "Academic":

        for keyword in academic_medium_keywords:
            if keyword in text:
                return "Medium"


    technical_medium_keywords = [
        "biometric",
        "fingerprint",
        "attendance system",
        "system not working",
        "server down",
        "portal not working",
        "login problem",
        "wifi not working",
        "wi-fi is not working",
        "internet not working"
    ]

    if category == "Technical":

        for keyword in technical_medium_keywords:
            if keyword in text:
                return "Medium"


    finance_medium_keywords = [
        "fee problem",
        "payment problem",
        "payment issue",
        "payment not updated",
        "refund",
        "scholarship"
    ]

    if category == "Finance":

        for keyword in finance_medium_keywords:
            if keyword in text:
                return "Medium"


    if ml_priority == "Urgent":
        return "Medium"


    return ml_priority


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    (
        category_model,
        priority_model,
        sentiment_analyzer,
        resolution_recommender,
        storage
    ) = load_models()


    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.title("🎓 Navigation")

    page = st.sidebar.radio(

        "Select Page",

        [
            "Submit Complaint",
            "Complaint Dashboard"
        ]
    )


    # =====================================================
    # APPLICATION HEADER
    # =====================================================

    st.title(
        "🎓 AI-Based Student Complaint Analytics and Resolution System"
    )

    st.markdown(
        "### Intelligent Complaint Classification, "
        "Priority Prediction and Resolution Recommendation"
    )


    # =====================================================
    # SUBMIT COMPLAINT PAGE
    # =====================================================

    if page == "Submit Complaint":

        st.header("📝 Submit Student Complaint")


        with st.form(
            "complaint_form",
            clear_on_submit=True
        ):

            st.subheader("👨‍🎓 Student Details")

            col1, col2 = st.columns(2)


            with col1:

                roll_number = st.text_input(
                    "Roll Number"
                )

                student_department = st.selectbox(
                    "Student Department",
                    STUDENT_DEPARTMENTS
                )


            with col2:

                year = st.selectbox(
                    "Year",
                    ["1", "2", "3", "4"]
                )

                semester = st.selectbox(
                    "Semester",
                    ["1", "2"]
                )


            st.subheader("📝 Complaint Details")

            complaint = st.text_area(
                "Enter Student Complaint",
                height=150,
                placeholder="Describe your complaint clearly..."
            )


            submitted = st.form_submit_button(
                "🔍 Analyze Complaint"
            )


        # =================================================
        # FORM SUBMISSION
        # =================================================

        if submitted:

            if roll_number.strip() == "":

                st.error(
                    "❌ Please enter the Roll Number."
                )

            elif complaint.strip() == "":

                st.error(
                    "❌ Please enter a Student Complaint."
                )

            else:

                # CATEGORY

                ml_category = category_model.predict(
                    [complaint]
                )[0]

                category = adjust_category(
                    complaint,
                    ml_category
                )


                # SENTIMENT

                sentiment = (
                    sentiment_analyzer.predict_sentiment(
                        complaint
                    )
                )


                # PRIORITY

                ml_priority = priority_model.predict(
                    [complaint]
                )[0]

                priority = adjust_priority(
                    complaint,
                    category,
                    ml_priority
                )


                # DEPARTMENT

                assigned_department = (
                    get_assigned_department(category)
                )


                # RESOLUTION

                resolution = (
                    resolution_recommender.recommend(
                        category,
                        priority
                    )
                )


                # COMPLAINT ID

                complaint_id = (
                    storage.generate_complaint_id()
                )


                # DATE TIME

                date_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )


                status = "Pending"


                # CREATE RECORD

                record = {

                    "Complaint_ID": complaint_id,

                    "Date_Time": date_time,

                    "Roll_Number": roll_number,

                    "Student_Department":
                        student_department,

                    "Year": year,

                    "Semester": semester,

                    "Complaint": complaint,

                    "Category": category,

                    "Sentiment": sentiment,

                    "Priority": priority,

                    "Department":
                        assigned_department,

                    "Status": status,

                    "Suggested Resolution":
                        resolution
                }


                # SAVE

                storage.save_complaint(
                    record
                )


                # SUCCESS

                st.success(
                    "✅ Complaint analyzed and saved successfully!"
                )


                # RESULTS

                st.header(
                    "📊 Complaint Analysis Result"
                )


                col1, col2, col3 = st.columns(3)


                with col1:
                    st.metric(
                        "Category",
                        category
                    )


                with col2:
                    st.metric(
                        "Sentiment",
                        sentiment
                    )


                with col3:
                    st.metric(
                        "Priority",
                        priority
                    )


                st.divider()


                # STUDENT INFORMATION

                st.subheader(
                    "👨‍🎓 Student Information"
                )

                info_col1, info_col2 = st.columns(2)


                with info_col1:

                    st.write(
                        "**Complaint ID:**",
                        complaint_id
                    )

                    st.write(
                        "**Roll Number:**",
                        roll_number
                    )

                    st.write(
                        "**Student Department:**",
                        student_department
                    )


                with info_col2:

                    st.write(
                        "**Date & Time:**",
                        date_time
                    )

                    st.write(
                        "**Year:**",
                        year
                    )

                    st.write(
                        "**Semester:**",
                        semester
                    )


                # COMPLAINT

                st.subheader(
                    "📝 Student Complaint"
                )

                st.info(complaint)


                # DEPARTMENT

                st.subheader(
                    "🏢 Assigned Department"
                )

                st.write(
                    assigned_department
                )


                # STATUS

                st.subheader(
                    "⏳ Complaint Status"
                )

                st.warning(status)


                # RESOLUTION

                st.subheader(
                    "💡 Suggested Resolution"
                )

                st.success(resolution)


    # =====================================================
    # COMPLAINT DASHBOARD
    # =====================================================

    elif page == "Complaint Dashboard":

        st.header(
            "📊 Complaint Analytics Dashboard"
        )


        output_file = Path(
            "outputs/complaint_records.csv"
        )


        if not output_file.exists():

            st.warning(
                "⚠️ No complaint records available yet."
            )


        else:

            df = pd.read_csv(
                output_file
            )

            df.columns = (
                df.columns.astype(str).str.strip()
            )


            if df.empty:

                st.warning(
                    "⚠️ No complaint records available."
                )


            else:

                # =========================================
                # METRICS
                # =========================================

                total_complaints = len(df)


                pending_complaints = 0

                if "Status" in df.columns:

                    pending_complaints = len(

                        df[
                            df["Status"]
                            .astype(str)
                            .str.strip()
                            .str.lower()
                            == "pending"
                        ]
                    )


                urgent_complaints = 0

                if "Priority" in df.columns:

                    urgent_complaints = len(

                        df[
                            df["Priority"]
                            .astype(str)
                            .str.strip()
                            .str.lower()
                            == "urgent"
                        ]
                    )


                col1, col2, col3 = st.columns(3)


                with col1:
                    st.metric(
                        "Total Complaints",
                        total_complaints
                    )


                with col2:
                    st.metric(
                        "Pending Complaints",
                        pending_complaints
                    )


                with col3:
                    st.metric(
                        "Urgent Complaints",
                        urgent_complaints
                    )


                st.divider()


                # =========================================
                # CATEGORY CHART
                # =========================================

                if "Category" in df.columns:

                    st.subheader(
                        "📌 Complaints by Category"
                    )

                    category_counts = (
                        df["Category"]
                        .dropna()
                        .value_counts()
                        .reset_index()
                    )

                    category_counts.columns = [
                        "Category",
                        "Count"
                    ]


                    fig = px.bar(
                        category_counts,
                        x="Category",
                        y="Count",
                        text="Count"
                    )

                    fig.update_layout(
                        yaxis=dict(
                            tickmode="linear",
                            dtick=1,
                            title="Number of Complaints"
                        ),
                        xaxis_title="Category"
                    )

                    st.plotly_chart(
                        fig,
                        width="stretch"
                    )


                # =========================================
                # PRIORITY CHART
                # =========================================

                if "Priority" in df.columns:

                    st.subheader(
                        "⚠️ Complaints by Priority"
                    )

                    priority_counts = (
                        df["Priority"]
                        .dropna()
                        .value_counts()
                        .reset_index()
                    )

                    priority_counts.columns = [
                        "Priority",
                        "Count"
                    ]


                    fig = px.bar(
                        priority_counts,
                        x="Priority",
                        y="Count",
                        text="Count"
                    )

                    fig.update_layout(
                        yaxis=dict(
                            tickmode="linear",
                            dtick=1,
                            title="Number of Complaints"
                        ),
                        xaxis_title="Priority"
                    )

                    st.plotly_chart(
                        fig,
                        width="stretch"
                    )


                # =========================================
                # SENTIMENT CHART
                # =========================================

                if "Sentiment" in df.columns:

                    st.subheader(
                        "😊 Sentiment Analysis"
                    )

                    sentiment_order = [
                        "Negative",
                        "Neutral",
                        "Positive"
                    ]

                    sentiment_counts = (
                        df["Sentiment"]
                        .astype(str)
                        .str.strip()
                        .value_counts()
                        .reindex(
                            sentiment_order,
                            fill_value=0
                        )
                        .reset_index()
                    )

                    sentiment_counts.columns = [
                        "Sentiment",
                        "Count"
                    ]


                    fig = px.bar(
                        sentiment_counts,
                        x="Sentiment",
                        y="Count",
                        text="Count"
                    )

                    fig.update_layout(
                        yaxis=dict(
                            tickmode="linear",
                            dtick=1,
                            title="Number of Complaints"
                        ),
                        xaxis_title="Sentiment"
                    )

                    st.plotly_chart(
                        fig,
                        width="stretch"
                    )


                # =========================================
                # DEPARTMENT CHART
                # =========================================

                st.subheader(
                    "🏢 Complaints by Assigned Department"
                )


                department_column = None


                if "Department" in df.columns:
                    department_column = "Department"

                elif "Assigned_Department" in df.columns:
                    department_column = "Assigned_Department"

                elif "Assigned Department" in df.columns:
                    department_column = "Assigned Department"


                if department_column:

                    department_counts = (
                        df[department_column]
                        .dropna()
                        .value_counts()
                        .reset_index()
                    )

                    department_counts.columns = [
                        "Department",
                        "Count"
                    ]


                    fig = px.bar(
                        department_counts,
                        x="Department",
                        y="Count",
                        text="Count"
                    )

                    fig.update_layout(
                        yaxis=dict(
                            tickmode="linear",
                            dtick=1,
                            title="Number of Complaints"
                        ),
                        xaxis_title="Assigned Department"
                    )

                    st.plotly_chart(
                        fig,
                        width="stretch"
                    )

                else:

                    st.warning(
                        "Department information is not available."
                    )


                # =========================================
                # ALL COMPLAINT RECORDS
                # =========================================

                st.divider()

                st.subheader(
                    "📋 All Complaint Records"
                )


                # CREATE SERIAL NUMBER STARTING FROM 1

                display_df = df.copy()

                display_df.index = range(
                    1,
                    len(display_df) + 1
                )

                display_df.index.name = "S.No"


                # DISPLAY TABLE

                st.dataframe(
                    display_df,
                    width="stretch"
                )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    main()