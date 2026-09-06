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
# SESSION STATE
# =========================================================

if "admin_logged_in" not in st.session_state:

    st.session_state.admin_logged_in = False


# =========================================================
# FILE PATH
# =========================================================

COMPLAINT_FILE = Path(
    "outputs/complaint_records.csv"
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


    academic_medium_keywords = [

        "timetable",
        "exam timetable",
        "examination timetable",
        "result not released",
        "not been released",
        "schedule delay"

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


    if ml_priority == "Urgent":

        return "Medium"


    return ml_priority


# =========================================================
# LOAD COMPLAINT DATA
# =========================================================

def load_complaint_data():

    if not COMPLAINT_FILE.exists():

        return None


    df = pd.read_csv(COMPLAINT_FILE)


    df.columns = (

        df.columns
        .astype(str)
        .str.strip()

    )


    # =====================================================
    # ASSIGNED STAFF
    # =====================================================

    if "Assigned_Staff" not in df.columns:

        df["Assigned_Staff"] = "Not Assigned"

    else:

        df["Assigned_Staff"] = (

            df["Assigned_Staff"]
            .fillna("Not Assigned")

        )


    # =====================================================
    # RESOLUTION DETAILS
    # =====================================================

    if "Resolution_Details" not in df.columns:

        df["Resolution_Details"] = "Not Resolved Yet"

    else:

        df["Resolution_Details"] = (

            df["Resolution_Details"]
            .fillna("Not Resolved Yet")

        )


    return df


# =========================================================
# SAVE COMPLAINT DATA
# =========================================================

def save_complaint_data(df):

    df.to_csv(

        COMPLAINT_FILE,

        index=False

    )


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


    menu_options = [

        "📝 Submit Complaint",

        "🔍 Track My Complaint",

        "🔐 Admin Login"

    ]


    if st.session_state.admin_logged_in:

        menu_options.append(
            "📊 Admin Dashboard"
        )


    page = st.sidebar.radio(

        "Select Page",

        menu_options

    )


    # =====================================================
    # ADMIN LOGOUT
    # =====================================================

    if st.session_state.admin_logged_in:


        st.sidebar.divider()


        st.sidebar.success(
            "👨‍💼 Admin Logged In"
        )


        if st.sidebar.button(
            "🚪 Logout"
        ):

            st.session_state.admin_logged_in = False

            st.rerun()


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

    if page == "📝 Submit Complaint":


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

                    get_assigned_department(
                        category
                    )

                )


                # AI RESOLUTION

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


                status = "Pending"


                # RECORD

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


                # SAVE

                storage.save_complaint(record)


                # SUCCESS

                st.success(
                    "✅ Complaint analyzed and saved successfully!"
                )


                st.info(
                    f"📌 Your Complaint ID is: **{complaint_id}**"
                )


                st.warning(
                    "Please save this Complaint ID to track your complaint."
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
                    "💡 AI Suggested Resolution"
                )


                st.success(
                    resolution
                )


    # =====================================================
    # TRACK COMPLAINT PAGE
    # =====================================================

    elif page == "🔍 Track My Complaint":


        st.header(
            "🔍 Track My Complaint"
        )


        st.write(
            "Enter your Complaint ID to check your complaint."
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


                if df is None:

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

                            complaint_data[
                                "Complaint_ID"
                            ]

                        )


                        st.write(

                            "**Complaint:**",

                            complaint_data[
                                "Complaint"
                            ]

                        )


                        # AI ANALYSIS

                        st.subheader(
                            "🤖 AI Analysis"
                        )


                        col1, col2, col3 = st.columns(3)


                        with col1:

                            st.metric(

                                "Category",

                                complaint_data[
                                    "Category"
                                ]

                            )


                        with col2:

                            st.metric(

                                "Priority",

                                complaint_data[
                                    "Priority"
                                ]

                            )


                        with col3:

                            st.metric(

                                "Sentiment",

                                complaint_data[
                                    "Sentiment"
                                ]

                            )


                        # ASSIGNMENT

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


                        # STATUS

                        st.subheader(
                            "📌 Current Status"
                        )


                        status = str(

                            complaint_data[
                                "Status"
                            ]

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


                        # RESOLUTION

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

                                str(
                                    resolution_details
                                ).strip()
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
    # ADMIN LOGIN
    # =====================================================

    elif page == "🔐 Admin Login":


        st.header(
            "🔐 Admin Login"
        )


        if st.session_state.admin_logged_in:


            st.success(
                "✅ You are already logged in."
            )


            st.info(
                "Open Admin Dashboard from the sidebar."
            )


        else:


            with st.form(
                "admin_login_form"
            ):


                username = st.text_input(
                    "Username"
                )


                password = st.text_input(

                    "Password",

                    type="password"

                )


                login = st.form_submit_button(
                    "🔐 Login"
                )


            if login:


                if (

                    username == ADMIN_USERNAME

                    and

                    password == ADMIN_PASSWORD

                ):


                    st.session_state.admin_logged_in = True


                    st.success(
                        "✅ Admin Login Successful!"
                    )


                    st.rerun()


                else:


                    st.error(
                        "❌ Invalid Username or Password."
                    )


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    elif page == "📊 Admin Dashboard":


        if not st.session_state.admin_logged_in:


            st.error(
                "❌ Access Denied."
            )


            return


        st.header(
            "📊 Admin Complaint Analytics Dashboard"
        )


        df = load_complaint_data()


        if df is None or df.empty:


            st.warning(
                "⚠️ No complaint records available."
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
        # ANALYTICS CHARTS
        # =================================================

        st.subheader(
            "📌 Complaints by Category"
        )


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


        st.subheader(
            "⚠️ Complaints by Priority"
        )


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


        st.subheader(
            "📋 Complaints by Status"
        )


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
        # COMPLAINT MANAGEMENT
        # =================================================

        st.divider()


        st.header(
            "⚙️ Manage Complaints"
        )


        selected_complaint_id = st.selectbox(

            "Select Complaint ID",

            df["Complaint_ID"].astype(str).tolist()

        )


        selected_index = df[

            df["Complaint_ID"]
            .astype(str)
            == selected_complaint_id

        ].index[0]


        complaint_data = df.loc[
            selected_index
        ]


        # =================================================
        # DISPLAY SELECTED COMPLAINT
        # =================================================

        st.subheader(
            "📋 Selected Complaint Details"
        )


        st.write(
            "**Complaint ID:**",
            complaint_data["Complaint_ID"]
        )


        st.write(
            "**Roll Number:**",
            complaint_data["Roll_Number"]
        )


        st.write(
            "**Student Department:**",
            complaint_data["Student_Department"]
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
            "**Sentiment:**",
            complaint_data["Sentiment"]
        )


        st.write(
            "**Assigned Department:**",
            complaint_data["Assigned_Department"]
        )


        st.write(
            "**Complaint:**"
        )


        st.info(
            complaint_data["Complaint"]
        )


        # =================================================
        # UPDATE FORM
        # =================================================

        st.subheader(
            "✏️ Update Complaint"
        )


        with st.form(

            "manage_complaint_form"

        ):


            staff_name = st.text_input(

                "Assign Staff Member",

                value=str(
                    complaint_data[
                        "Assigned_Staff"
                    ]
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


            if current_status in status_options:

                status_index = (

                    status_options.index(
                        current_status
                    )

                )

            else:

                status_index = 0


            new_status = st.selectbox(

                "Update Status",

                status_options,

                index=status_index

            )


            current_resolution = str(

                complaint_data[
                    "Resolution_Details"
                ]

            )


            if current_resolution == "Not Resolved Yet":

                current_resolution = ""


            resolution_details = st.text_area(

                "Resolution Details",

                value=current_resolution,

                height=120,

                placeholder=
                "Enter the action taken to resolve this complaint..."

            )


            update_button = st.form_submit_button(

                "💾 Save Changes"

            )


        # =================================================
        # SAVE UPDATES
        # =================================================

        if update_button:


            if staff_name.strip() == "":

                staff_name = "Not Assigned"


            df.loc[

                selected_index,

                "Assigned_Staff"

            ] = staff_name


            df.loc[

                selected_index,

                "Status"

            ] = new_status


            if new_status == "Resolved":


                if resolution_details.strip() == "":

                    st.warning(
                        "⚠️ Please enter Resolution Details before resolving the complaint."
                    )


                    return


                df.loc[

                    selected_index,

                    "Resolution_Details"

                ] = resolution_details


            else:


                if resolution_details.strip() == "":

                    df.loc[

                        selected_index,

                        "Resolution_Details"

                    ] = "Not Resolved Yet"


                else:

                    df.loc[

                        selected_index,

                        "Resolution_Details"

                    ] = resolution_details


            # SAVE CSV

            save_complaint_data(df)


            st.success(
                "✅ Complaint updated successfully!"
            )


            st.balloons()


            st.rerun()


        # =================================================
        # ALL COMPLAINT RECORDS
        # =================================================

        st.divider()


        st.header(
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