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
# SESSION STATE
# =========================================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login():

    st.header("🔐 Admin Login")

    st.info(
        "Only administrators can access and manage complaints."
    )

    with st.form("admin_login_form"):

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        login_button = st.form_submit_button("🔐 Login")

    if login_button:

        if (
            username.strip() == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            st.session_state.admin_logged_in = True

            st.success("✅ Login Successful!")

            st.rerun()

        else:

            st.error("❌ Invalid Username or Password")


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

    if (
        "Assigned_Department" not in df.columns
        and "Department" in df.columns
    ):
        df["Assigned_Department"] = df["Department"]

    if "Assigned_Staff" not in df.columns:
        df["Assigned_Staff"] = "Not Assigned"

    df["Assigned_Staff"] = (
        df["Assigned_Staff"]
        .fillna("Not Assigned")
    )

    if "Resolution_Details" not in df.columns:
        df["Resolution_Details"] = "Not Resolved Yet"

    df["Resolution_Details"] = (
        df["Resolution_Details"]
        .fillna("Not Resolved Yet")
    )

    if "Status" not in df.columns:
        df["Status"] = "Pending"

    return df


# =========================================================
# SAVE COMPLAINT DATA
# =========================================================

def save_complaint_data(storage, df):

    df.to_csv(
        storage.file_path,
        index=False
    )


# =========================================================
# CATEGORY ADJUSTMENT
# =========================================================

def adjust_category(complaint, ml_category):

    text = complaint.lower()

    categories = {

        "Academic": [
            "exam",
            "examination",
            "timetable",
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
            "class"
        ],

        "Finance": [
            "fee",
            "fees",
            "payment",
            "scholarship",
            "refund",
            "tuition",
            "fine",
            "money"
        ],

        "Technical": [
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
            "system",
            "biometric",
            "fingerprint",
            "keyboard",
            "mouse"
        ],

        "Infrastructure": [
            "water",
            "leakage",
            "leaking",
            "electricity",
            "power",
            "fan",
            "air conditioner",
            "washroom",
            "bathroom",
            "hostel",
            "ceiling",
            "lift",
            "furniture",
            "building",
            "projector",
            "chair",
            "desk",
            "light"
        ],

        "Administrative": [
            "library",
            "discipline",
            "administration",
            "security",
            "parking",
            "cafeteria",
            "canteen",
            "bus",
            "transport"
        ]
    }

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in text:
                return category

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
        "collapsed",
        "collapse",
        "life threatening"
    ]

    for keyword in urgent_keywords:

        if keyword in text:
            return "Urgent"

    high_keywords = [
        "water leakage",
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
    # HEADER
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

            if not roll_number.strip():

                st.error(
                    "❌ Please enter your Roll Number."
                )

            elif not complaint.strip():

                st.error(
                    "❌ Please enter a complaint."
                )

            else:

                # AI CATEGORY

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

                    "Complaint_ID":
                        complaint_id,

                    "Date_Time":
                        date_time,

                    "Roll_Number":
                        roll_number.strip(),

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
                        "Pending",

                    "Suggested Resolution":
                        resolution
                }


                # SAVE

                storage.save_complaint(record)


                # SUCCESS

                st.success(
                    "✅ Complaint submitted successfully!"
                )

                st.subheader(
                    "📊 Complaint Analysis Result"
                )

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
                    "**Assigned Department:**",
                    assigned_department
                )

                st.write(
                    "**Status:** Pending"
                )

                st.subheader(
                    "💡 Suggested Resolution"
                )

                st.success(resolution)

                st.warning(
                    "📌 Save your Complaint ID for tracking."
                )


    # =====================================================
    # TRACK COMPLAINT
    # =====================================================

    elif page == "Track Complaint":

        st.header("🔍 Track Your Complaints")

        roll_number_input = st.text_input(
            "Enter Your Roll Number"
        )

        if st.button("🔍 Track Complaints"):

            if not roll_number_input.strip():

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

                        roll_number_input
                        .strip()
                        .lower()

                    ]


                    if student_complaints.empty:

                        st.error(
                            "❌ No complaints found."
                        )

                    else:

                        st.success(
                            f"✅ Found {len(student_complaints)} complaint(s)."
                        )

                        for _, complaint_data in (
                            student_complaints.iterrows()
                        ):

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

                            if (
                                str(
                                    complaint_data["Status"]
                                ).strip().lower()
                                == "resolved"
                            ):

                                st.subheader(
                                    "✅ Resolution Details"
                                )

                                details = (
                                    complaint_data[
                                        "Resolution_Details"
                                    ]
                                )

                                if (
                                    str(details).strip()
                                    != "Not Resolved Yet"
                                ):

                                    st.success(details)


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    elif page == "Complaint Dashboard":

        if not st.session_state.admin_logged_in:

            admin_login()

            return


        # LOGOUT

        col1, col2 = st.columns([8, 2])

        with col1:
            st.header(
                "📊 Admin Complaint Analytics Dashboard"
            )

        with col2:

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

        total = len(df)

        pending = len(
            df[
                df["Status"]
                .astype(str)
                .str.lower()
                == "pending"
            ]
        )

        progress = len(
            df[
                df["Status"]
                .astype(str)
                .str.lower()
                == "in progress"
            ]
        )

        resolved = len(
            df[
                df["Status"]
                .astype(str)
                .str.lower()
                == "resolved"
            ]
        )


        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Complaints", total)
        c2.metric("Pending", pending)
        c3.metric("In Progress", progress)
        c4.metric("Resolved", resolved)


        st.divider()


        # =================================================
        # CHARTS
        # =================================================

        st.subheader("📊 Complaint Analytics")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

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
                y="Count"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )


        with chart_col2:

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
                y="Count"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )


        # =================================================
        # COMPLAINT MANAGEMENT
        # =================================================

        st.divider()

        st.header("🛠️ Complaint Management")

        complaint_ids = df["Complaint_ID"].astype(str).tolist()

        selected_id = st.selectbox(
            "Select Complaint ID",
            complaint_ids
        )

        selected_index = df[
            df["Complaint_ID"].astype(str)
            == selected_id
        ].index[0]

        complaint_data = df.loc[selected_index]

        st.subheader("📋 Selected Complaint")

        st.write(
            "**Student Roll Number:**",
            complaint_data["Roll_Number"]
        )

        st.write(
            "**Complaint:**",
            complaint_data["Complaint"]
        )

        st.write(
            "**Category:**",
            complaint_data["Category"]
        )

        st.write(
            "**Priority:**",
            complaint_data["Priority"]
        )

        st.write(
            "**Assigned Department:**",
            complaint_data["Assigned_Department"]
        )


        # =================================================
        # ADMIN UPDATE FORM
        # =================================================

        st.subheader("✏️ Update Complaint")

        with st.form("update_complaint_form"):

            staff_name = st.text_input(
                "Assign Staff Member",
                value=str(
                    complaint_data["Assigned_Staff"]
                )
            )

            status_options = [
                "Pending",
                "In Progress",
                "Resolved"
            ]

            current_status = str(
                complaint_data["Status"]
            ).strip()

            status_index = (
                status_options.index(current_status)
                if current_status in status_options
                else 0
            )

            new_status = st.selectbox(
                "Update Status",
                status_options,
                index=status_index
            )

            current_resolution = str(
                complaint_data["Resolution_Details"]
            )

            resolution_details = st.text_area(
                "Resolution Details",
                value=(
                    ""
                    if current_resolution
                    == "Not Resolved Yet"
                    else current_resolution
                ),
                height=120
            )

            update_button = st.form_submit_button(
                "💾 Save Changes"
            )


        if update_button:

            # STAFF

            if staff_name.strip():
                df.loc[
                    selected_index,
                    "Assigned_Staff"
                ] = staff_name.strip()

            else:
                df.loc[
                    selected_index,
                    "Assigned_Staff"
                ] = "Not Assigned"


            # STATUS

            df.loc[
                selected_index,
                "Status"
            ] = new_status


            # RESOLUTION

            if new_status == "Resolved":

                if resolution_details.strip():

                    df.loc[
                        selected_index,
                        "Resolution_Details"
                    ] = resolution_details.strip()

                else:

                    st.error(
                        "❌ Please enter resolution details before resolving."
                    )

                    return

            else:

                df.loc[
                    selected_index,
                    "Resolution_Details"
                ] = "Not Resolved Yet"


            # SAVE

            save_complaint_data(
                storage,
                df
            )

            st.success(
                "✅ Complaint updated successfully!"
            )

            st.rerun()


        # =================================================
        # ALL RECORDS
        # =================================================

        st.divider()

        st.header("📋 All Complaint Records")

        st.dataframe(
            df,
            width="stretch"
        )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    main()