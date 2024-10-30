import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Set up title
st.title("Site Incident Report")

# Initialize the reports DataFrame in session state
if "reports" not in st.session_state:
    st.session_state["reports"] = []

# Create tabs for "New Report", "View Reports", and "Statistics"
tab1, tab2, tab3 = st.tabs(["New Report", "View Reports", "Statistics"])

with tab1:
    st.subheader("Fill in the form below to submit an incident report.")

    # Input fields for new report
    name = st.text_input("Attendee")
    incident_date = st.date_input("Date of Incident")
    site_name = st.text_input("Site")
    state = st.selectbox("State", ["Perlis", "Kedah", "Pulau Pinang", "Perak", "Selangor", "Kelantan", "Terengganu", "Negeri Sembilan", "Melaka", "Johor", "Sabah", "Sarawak"])
    priority = st.selectbox("Issue Level", ["1", "2", "3"])
    issue_info = st.text_input("Issue Info (User/BD)")
    general_issue = st.text_input("General Issue (Potential)")
    issue_cat = st.selectbox("Issue Category", ["Hardware", "Software", "Connectivity"])
    diagnose = st.text_input("Diagnose (Actual Issue)")
    solution = st.text_area("Solution")
    status = st.selectbox("Status", ["Open", "Closed"])
    comments = st.text_area("Comments")

    # Required fields check
    if st.button("Submit Report"):
        if not name or not incident_date or not site_name or not state or not priority or not issue_info or not issue_cat or not status:
            st.error("Please fill in all required fields: Attendee, Date of Incident, Site, State, Priority, Issue Info, Issue Category, and Status.")
        else:
            # Add new report to session state
            report = {
                "Name": name,
                "Date": incident_date,
                "Site": site_name,
                "State": state,
                "Priority": priority,
                "Issue Info": issue_info,
                "General Issue": general_issue,
                "Issue Category": issue_cat,
                "Diagnose": diagnose,
                "Solution": solution,
                "Status": status,
                "Comments": comments
            }
            st.session_state["reports"].append(report)
            st.success("Report submitted successfully!")

with tab2:
    st.subheader("Submitted Reports")

    # Check if there are any reports
    if st.session_state["reports"]:
        # Convert reports to DataFrame
        reports_df = pd.DataFrame(st.session_state["reports"])

        # Display submitted reports in a compact format with only "Site" and "Date"
        for i, report in enumerate(st.session_state["reports"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Site:** {report['Site']}  |  **Date:** {report['Date']}")
            with col2:
                # Only the "Complete" button
                if report["Status"] == "Open":
                    if st.button(f"Complete", key=f"complete_{i}"):
                        st.session_state["reports"][i]["Status"] = "Closed"
                        st.success(f"Report {i + 1} marked as Completed.")
                        st.experimental_rerun()  # Reload to show updated status

            st.write("---")  # Divider between reports

        # Download button for all reports
        csv_data = reports_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download All Reports",
            data=csv_data,
            file_name="incident_reports.csv",
            mime="text/csv"
        )
    else:
        st.write("No reports submitted yet.")

with tab3:
    st.subheader("Report Statistics")

    if st.session_state["reports"]:
        # Convert reports to DataFrame
        reports_df = pd.DataFrame(st.session_state["reports"])

        # Ensure the Date column is in datetime format
        reports_df["Date"] = pd.to_datetime(reports_df["Date"])

        # Chart 1: Total Issues Reported by Month using Plotly
        reports_df['Month'] = reports_df['Date'].dt.to_period('M').astype(str)
        monthly_counts = reports_df.groupby('Month').size().reset_index(name='Count')
        fig1 = px.bar(monthly_counts, x='Month', y='Count', title="Total Issues Reported by Month")
        st.plotly_chart(fig1, use_container_width=True)

        # Chart 2: Issues by Category using Plotly
        category_counts = reports_df["Issue Category"].value_counts().reset_index()
        category_counts.columns = ["Issue Category", "Count"]
        fig2 = px.bar(category_counts, x='Issue Category', y='Count', title="Issues by Category")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.write("No reports submitted yet.")
