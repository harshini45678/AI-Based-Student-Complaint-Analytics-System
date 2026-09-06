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
# ADMIN LOGIN DETAILS
# =========================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


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
# INITIALIZE SESSION STATE
# =========================================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login():

    st.header("🔐 Admin Login")

    st.info(
        "Only administrators can access the Complaint Dashboard."
    )

    with st.form("admin_login_form"):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_button = st.form_submit_button(
            "🔐 Login"
        )

    if login_button:

        if (
            username.strip() == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            st.session_state.admin_logged_in = True

            st.success(
                "✅ Login Successful!"
            )

            st.rerun()

        else:

            st.error(
                "❌ Invalid Username or Password"
            )


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
# LOAD COMPLAINT DATA
# =========================================================

def load_complaint_data(storage):

    file_path = storage.file_path

    if not file_path.exists():

        return pd.DataFrame()

    try:

        df = pd.read_csv(file_path)

    except pd.errors.EmptyDataError:

        return pd.DataFrame()

    if df.empty:

        return df

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # Handle old column name
    if (
        "Assigned_Department" not in df.columns
        and "Department" in df.columns
    ):

        df["Assigned_Department"] = df["Department"]

    # Add Assigned Staff
    if "Assigned_Staff" not in df.columns:

        df["Assigned_Staff"] = "Not Assigned"

    else:

        df["Assigned_Staff"] = (
            df["Assigned_Staff"]
            .fillna("Not Assigned")
        )

    # Add Resolution Details
    if "Resolution_Details" not in df.columns:

        df["Resolution_Details"] = "Not Resolved Yet"

    else:

        df["Resolution_Details"] = (
            df["Resolution_Details"]
            .fillna("Not Resolved Yet")
        )

    return df


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
        "fans",
        "air conditioner",
        "washroom",
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

        "Academic":
            "Academic Department",

        "Administrative":
            "Administration Department",

        "Finance":
            "Accounts and Finance Department",

        "Infrastructure":
            "Maintenance Department",

        "Technical":
            "IT Support Department"
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
        "no electricity",
        "power failure",
        "short circuit",
        "broken ceiling"
    ]

    if category == "Infrastructure":

        for keyword in high_keywords:

            if keyword in text:
                return "High"

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
            "Track Complaint",
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
    # SUBMIT COMPLAINT
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
                "🔍 Analyze and Submit Complaint"
            )


        if submitted:

            if roll_number.strip() == "":

                st.error(
                    "❌ Please enter your Roll Number."
                )

            elif complaint.strip() == "":

                st.error(
                    "❌ Please enter a complaint."
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

                # DATE
                date_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                # RECORD
                record = {

                    "Complaint_ID": complaint_id,
                    "Date_Time": date_time,
                    "Roll_Number": roll_number.strip(),
                    "Student_Department": student_department,
                    "Year": year,
                    "Semester": semester,
                    "Complaint": complaint,
                    "Category": category,
                    "Sentiment": sentiment,
                    "Priority": priority,
                    "Department": assigned_department,
                    "Status": "Pending",
                    "Suggested Resolution": resolution
                }

                # SAVE
                storage.save_complaint(record)

                st.success(
                    "✅ Complaint submitted successfully!"
                )

                st.subheader("📊 Complaint Analysis Result")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Category", category)

                with col2:
                    st.metric("Sentiment", sentiment)

                with col3:
                    st.metric("Priority", priority)

                st.divider()

                st.subheader("📋 Complaint Information")

                st.write(
                    "**Complaint ID:**",
                    complaint_id
                )

                st.write(
                    "**Roll Number:**",
                    roll_number
                )

                st.write(
                    "**Assigned Department:**",
                    assigned_department
                )

                st.write(
                    "**Status:** Pending"
                )

                st.subheader("💡 Suggested Resolution")

                st.success(resolution)

                st.info(
                    "📌 Remember your Roll Number. "
                    "You can use it to track your complaints."
                )


    # =====================================================
    # TRACK COMPLAINT USING ROLL NUMBER
    # =====================================================

    elif page == "Track Complaint":

        st.header("🔍 Track Your Complaints")

        st.write(
            "Enter your Roll Number to view your submitted complaints."
        )

        roll_number_input = st.text_input(
            "Enter Your Roll Number"
        )

        if st.button("🔍 Track Complaints"):

            if roll_number_input.strip() == "":

                st.warning(
                    "⚠️ Please enter your Roll Number."
                )

            else:

                df = load_complaint_data(storage)

                if df.empty:

                    st.warning(
                        "⚠️ No complaint records found."
                    )

                else:

                    student_complaints = df[
                        df["Roll_Number"]
                        .astype(str)
                        .str.strip()
                        .str.lower()
                        ==
                        roll_number_input.strip().lower()
                    ]

                    if student_complaints.empty:

                        st.error(
                            "❌ No complaints found for this Roll Number."
                        )

                    else:

                        st.success(
                            f"✅ Found {len(student_complaints)} complaint(s)."
                        )

                        for _, complaint_data in student_complaints.iterrows():

                            st.divider()

                            st.subheader(
                                f"📌 {complaint_data['Complaint_ID']}"
                            )

                            st.write(
                                "**Complaint:**",
                                complaint_data["Complaint"]
                            )

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric(
                                    "Category",
                                    complaint_data["Category"]
                                )

                            with col2:
                                st.metric(
                                    "Priority",
                                    complaint_data["Priority"]
                                )

                            with col3:
                                st.metric(
                                    "Status",
                                    complaint_data["Status"]
                                )

                            st.write(
                                "**Assigned Department:**",
                                complaint_data["Assigned_Department"]
                            )

                            st.write(
                                "**Assigned Staff:**",
                                complaint_data["Assigned_Staff"]
                            )

                            # Show resolution only if resolved
                            if (
                                str(
                                    complaint_data["Status"]
                                ).strip().lower()
                                == "resolved"
                            ):

                                st.subheader(
                                    "✅ Resolution Details"
                                )

                                resolution_details = (
                                    complaint_data[
                                        "Resolution_Details"
                                    ]
                                )

                                if (
                                    pd.isna(resolution_details)
                                    or
                                    str(resolution_details).strip()
                                    == ""
                                    or
                                    str(resolution_details).strip()
                                    == "Not Resolved Yet"
                                ):

                                    st.info(
                                        "Resolution details are not available yet."
                                    )

                                else:

                                    st.success(
                                        resolution_details
                                    )


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    elif page == "Complaint Dashboard":

        # LOGIN CHECK
        if not st.session_state.admin_logged_in:

            admin_login()

            return


        # DASHBOARD HEADER
        col1, col2 = st.columns([8, 2])

        with col1:

            st.header(
                "📊 Admin Complaint Analytics Dashboard"
            )

        with col2:

            st.write("")

            if st.button("🚪 Logout"):

                st.session_state.admin_logged_in = False

                st.rerun()


        # LOAD DATA
        df = load_complaint_data(storage)


        if df.empty:

            st.warning(
                "⚠️ No complaint records available yet."
            )

            return


        # =================================================
        # METRICS
        # =================================================

        total_complaints = len(df)

        pending_complaints = len(
            df[
                df["Status"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "pending"
            ]
        )

        in_progress_complaints = len(
            df[
                df["Status"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "in progress"
            ]
        )

        resolved_complaints = len(
            df[
                df["Status"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "resolved"
            ]
        )


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Complaints",
                total_complaints
            )

        with col2:
            st.metric(
                "Pending",
                pending_complaints
            )

        with col3:
            st.metric(
                "In Progress",
                in_progress_complaints
            )

        with col4:
            st.metric(
                "Resolved",
                resolved_complaints
            )


        st.divider()


        # =================================================
        # CATEGORY CHART
        # =================================================

        st.subheader("📌 Complaints by Category")

        category_counts = (
            df["Category"]
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

        st.plotly_chart(
            fig,
            width="stretch"
        )


        # =================================================
        # PRIORITY CHART
        # =================================================

        st.subheader("⚠️ Complaints by Priority")

        priority_counts = (
            df["Priority"]
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

        st.plotly_chart(
            fig,
            width="stretch"
        )


        # =================================================
        # STATUS CHART
        # =================================================

        st.subheader("📋 Complaints by Status")

        status_counts = (
            df["Status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Count"
        ]

        fig = px.bar(
            status_counts,
            x="Status",
            y="Count",
            text="Count"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


        # =================================================
        # SENTIMENT CHART
        # =================================================

        st.subheader("😊 Sentiment Analysis")

        sentiment_counts = (
            df["Sentiment"]
            .value_counts()
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

        st.plotly_chart(
            fig,
            width="stretch"
        )


        # =================================================
        # DEPARTMENT CHART
        # =================================================

        st.subheader(
            "🏢 Complaints by Assigned Department"
        )

        department_counts = (
            df["Assigned_Department"]
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

        st.plotly_chart(
            fig,
            width="stretch"
        )


        # =================================================
        # ALL COMPLAINT RECORDS
        # =================================================

        st.divider()

        st.subheader("📋 All Complaint Records")

        display_df = df.copy()

        display_df.index = range(
            1,
            len(display_df) + 1
        )

        display_df.index.name = "S.No"

        st.dataframe(
            display_df,
            width="stretch"
        )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    main()