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
# ADMIN LOGIN FUNCTION
# =========================================================

def admin_login():

    if "admin_logged_in" not in st.session_state:

        st.session_state.admin_logged_in = False


    if st.session_state.admin_logged_in:

        return True


    st.header("🔐 Admin Login")

    st.write(
        "Please enter your administrator credentials "
        "to access the Complaint Dashboard."
    )


    username = st.text_input(
        "Username",
        key="admin_username"
    )


    password = st.text_input(
        "Password",
        type="password",
        key="admin_password"
    )


    if st.button("🔐 Login"):


        if (

            username == ADMIN_USERNAME
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


    return False


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


    resolution_recommender = (
        ResolutionRecommender()
    )


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

def load_complaint_data():

    output_file = Path(
        "outputs/complaint_records.csv"
    )


    if not output_file.exists():

        return pd.DataFrame()


    df = pd.read_csv(
        output_file
    )


    df.columns = (

        df.columns
        .astype(str)
        .str.strip()

    )


    # -----------------------------------------------------
    # HANDLE OLD / NEW COLUMN NAMES
    # -----------------------------------------------------

    if (
        "Assigned_Department" not in df.columns
        and "Department" in df.columns
    ):

        df["Assigned_Department"] = (
            df["Department"]
        )


    # -----------------------------------------------------
    # ASSIGNED STAFF
    # -----------------------------------------------------

    if "Assigned_Staff" not in df.columns:

        df["Assigned_Staff"] = (
            "Not Assigned"
        )


    else:

        df["Assigned_Staff"] = (

            df["Assigned_Staff"]
            .fillna("Not Assigned")

        )


    # -----------------------------------------------------
    # RESOLUTION DETAILS
    # -----------------------------------------------------

    if "Resolution_Details" not in df.columns:

        df["Resolution_Details"] = (
            "Not Resolved Yet"
        )


    else:

        df["Resolution_Details"] = (

            df["Resolution_Details"]
            .fillna("Not Resolved Yet")

        )


    return df


# =========================================================
# CATEGORY ADJUSTMENT
# =========================================================

def adjust_category(
    complaint,
    ml_category
):

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


    # =====================================================
    # LOAD MODELS
    # =====================================================

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

    st.sidebar.title(
        "🎓 Navigation"
    )


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
    # SUBMIT COMPLAINT PAGE
    # =====================================================

    if page == "Submit Complaint":


        st.header(
            "📝 Submit Student Complaint"
        )


        with st.form(
            "complaint_form",
            clear_on_submit=True
        ):


            st.subheader(
                "👨‍🎓 Student Details"
            )


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


            st.subheader(
                "📝 Complaint Details"
            )


            complaint = st.text_area(

                "Enter Student Complaint",

                height=150,

                placeholder=
                "Describe your complaint clearly..."

            )


            submitted = st.form_submit_button(
                "🔍 Analyze Complaint"
            )


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


                # SUGGESTED RESOLUTION

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


                # DATE AND TIME

                date_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )


                # STATUS

                status = "Pending"


                # CREATE RECORD

                record = {

                    "Complaint_ID":
                        complaint_id,

                    "Date_Time":
                        date_time,

                    "Roll_Number":
                        roll_number,

                    "Student_Department":
                        student_department,

                    "Year":
                        year,

                    "Semester":
                        semester,

                    "Complaint":
                        complaint,

                    "Category":
                        category,

                    "Sentiment":
                        sentiment,

                    "Priority":
                        priority,

                    "Department":
                        assigned_department,

                    "Status":
                        status,

                    "Suggested Resolution":
                        resolution

                }


                # SAVE RECORD

                storage.save_complaint(
                    record
                )


                # SUCCESS

                st.success(
                    "✅ Complaint analyzed and saved successfully!"
                )


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


                st.subheader(
                    "📝 Student Complaint"
                )

                st.info(
                    complaint
                )


                st.subheader(
                    "🏢 Assigned Department"
                )

                st.write(
                    assigned_department
                )


                st.subheader(
                    "⏳ Complaint Status"
                )

                st.warning(
                    status
                )


                st.subheader(
                    "💡 Suggested Resolution"
                )

                st.success(
                    resolution
                )


    # =====================================================
    # TRACK COMPLAINT PAGE
    # =====================================================

    elif page == "Track Complaint":


        st.header(
            "🔍 Track Your Complaint"
        )


        st.write(
            "Enter your Complaint ID to check "
            "the current status."
        )


        complaint_id_input = st.text_input(
            "Enter Complaint ID"
        )


        if st.button(
            "🔍 Track Complaint"
        ):


            if complaint_id_input.strip() == "":

                st.warning(
                    "⚠️ Please enter your Complaint ID."
                )


            else:


                df = load_complaint_data()


                if df.empty:

                    st.error(
                        "❌ No complaint records found."
                    )


                else:


                    result = df[

                        df["Complaint_ID"]
                        .astype(str)
                        == complaint_id_input.strip()

                    ]


                    if result.empty:

                        st.error(
                            "❌ Complaint ID not found."
                        )


                    else:


                        complaint_data = result.iloc[0]


                        st.success(
                            "✅ Complaint Found!"
                        )


                        st.subheader(
                            "📋 Complaint Details"
                        )


                        st.write(
                            "**Complaint ID:**",
                            complaint_data["Complaint_ID"]
                        )


                        st.write(
                            "**Complaint:**",
                            complaint_data["Complaint"]
                        )


                        st.subheader(
                            "🤖 AI Analysis"
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
                                "Sentiment",
                                complaint_data["Sentiment"]
                            )


                        st.subheader(
                            "👨‍💼 Complaint Assignment"
                        )


                        st.write(
                            "**Assigned Department:**",
                            complaint_data[
                                "Assigned_Department"
                            ]
                        )


                        st.write(
                            "**Assigned Staff:**",
                            complaint_data[
                                "Assigned_Staff"
                            ]
                        )


                        st.subheader(
                            "📌 Current Status"
                        )


                        status = str(
                            complaint_data["Status"]
                        ).strip()


                        if status == "Resolved":

                            st.success(
                                f"✅ {status}"
                            )


                        elif status == "In Progress":

                            st.info(
                                f"🔄 {status}"
                            )


                        else:

                            st.warning(
                                f"⏳ {status}"
                            )


                        if status == "Resolved":


                            st.subheader(
                                "✅ Resolution Details"
                            )


                            resolution_details = (
                                complaint_data[
                                    "Resolution_Details"
                                ]
                            )


                            if (

                                pd.isna(
                                    resolution_details
                                )

                                or

                                str(
                                    resolution_details
                                ).strip() == ""

                                or

                                str(
                                    resolution_details
                                ).strip()
                                == "Not Resolved Yet"

                            ):


                                st.info(
                                    "Resolution details are "
                                    "not available yet."
                                )


                            else:

                                st.success(
                                    resolution_details
                                )


    # =====================================================
    # ADMIN COMPLAINT DASHBOARD
    # =====================================================

    elif page == "Complaint Dashboard":


        # -------------------------------------------------
        # ADMIN LOGIN PROTECTION
        # -------------------------------------------------

        if not admin_login():

            st.stop()


        # -------------------------------------------------
        # LOGOUT
        # -------------------------------------------------

        logout_col1, logout_col2 = st.columns(
            [8, 2]
        )


        with logout_col1:

            st.header(
                "📊 Admin Complaint Analytics Dashboard"
            )


        with logout_col2:

            if st.button(
                "🚪 Logout"
            ):

                st.session_state.admin_logged_in = False

                st.rerun()


        # -------------------------------------------------
        # LOAD DATA
        # -------------------------------------------------

        df = load_complaint_data()


        if df.empty:

            st.warning(
                "⚠️ No complaint records available yet."
            )


        else:


            # =============================================
            # METRICS
            # =============================================

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


            # =============================================
            # CATEGORY CHART
            # =============================================

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


            st.plotly_chart(
                fig,
                width="stretch"
            )


            # =============================================
            # PRIORITY CHART
            # =============================================

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


            st.plotly_chart(
                fig,
                width="stretch"
            )


            # =============================================
            # STATUS CHART
            # =============================================

            st.subheader(
                "📋 Complaints by Status"
            )


            status_counts = (

                df["Status"]
                .dropna()
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


            # =============================================
            # SENTIMENT CHART
            # =============================================

            st.subheader(
                "😊 Sentiment Analysis"
            )


            sentiment_counts = (

                df["Sentiment"]
                .dropna()
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


            # =============================================
            # DEPARTMENT CHART
            # =============================================

            st.subheader(
                "🏢 Complaints by Assigned Department"
            )


            department_counts = (

                df["Assigned_Department"]
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


            st.plotly_chart(
                fig,
                width="stretch"
            )


            # =============================================
            # STAFF ASSIGNMENT
            # =============================================

            st.subheader(
                "👨‍💼 Staff Assignment Details"
            )


            assigned_staff_count = len(

                df[

                    df["Assigned_Staff"]
                    .astype(str)
                    .str.strip()
                    != "Not Assigned"

                ]

            )


            unassigned_count = (

                total_complaints
                - assigned_staff_count

            )


            staff_col1, staff_col2 = st.columns(2)


            with staff_col1:

                st.metric(
                    "Assigned Complaints",
                    assigned_staff_count
                )


            with staff_col2:

                st.metric(
                    "Not Assigned",
                    unassigned_count
                )


            # =============================================
            # RESOLVED COMPLAINTS
            # =============================================

            st.divider()


            st.subheader(
                "✅ Resolved Complaints and Resolution Details"
            )


            resolved_df = df[

                df["Status"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "resolved"

            ].copy()


            if resolved_df.empty:

                st.info(
                    "No resolved complaints available yet."
                )


            else:


                resolution_columns = [

                    "Complaint_ID",
                    "Roll_Number",
                    "Complaint",
                    "Category",
                    "Assigned_Department",
                    "Assigned_Staff",
                    "Status",
                    "Resolution_Details"

                ]


                available_columns = [

                    column

                    for column in resolution_columns

                    if column in resolved_df.columns

                ]


                st.dataframe(

                    resolved_df[
                        available_columns
                    ],

                    width="stretch"

                )


            # =============================================
            # ALL COMPLAINT RECORDS
            # =============================================

            st.divider()


            st.subheader(
                "📋 All Complaint Records"
            )


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