import streamlit as st
import os
import subprocess
import time
import shutil
import webbrowser
st.set_page_config(layout="wide")

# Sidebar for test actions
action = st.sidebar.radio("Select Action:", ["Trigger Test", "Edit Test Data", "View Results"])

st.title("MARS QA Automation Dashboard 🤖")

if action == "Trigger Test":
    st.subheader("Run Automated Tests")
    test_options = {
        "All Tests": "tests/",
        "Smoke Tests": "tests/smoke/",
        "Regression Tests": "tests/regression/",
        "Custom Test File": "custom"
    }

    selected_test = st.selectbox("Select Test Type:", list(test_options.keys()))
     # If user selects "Custom Test File", show text input
    custom_test_path = ""
    if selected_test == "Custom Test File":
        custom_test_path = st.text_input("Enter the test file path (e.g., tests/test_brand.py):")


    if st.button("Run Tests 🚀"):
        st.write("Tests are running... Please wait!")
        test_path = test_options[selected_test] if selected_test != "Custom Test File" else custom_test_path
        if test_path:  # Ensure the path is not empty
            command = ["pytest", test_path, "--alluredir=reports/allure-results"]
            st.write(f"Running: {' '.join(command)}")  # Show executed command
            subprocess.run(command)
            st.success("Tests Triggered! Check 'View Results' for the report.")
        else:
            st.warning("Please enter a valid test file path.")

        # # Run Pytest and Generate Allure Report
        # pytest_command = "pytest tests/ --alluredir=reports/allure-results"
        # subprocess.run(pytest_command, shell=True)

        # Generate Allure report
        allure_generate_command = "allure generate --single-file reports/allure-results -o reports/allure-report --clean"
        subprocess.run(allure_generate_command, shell=True)

        st.success("Tests Completed ✅ and Allure Report Generated!")

elif action == "Edit Test Data":
    st.subheader("Modify Test Data")

    test_data_file = "test_data/sample.json"

    if os.path.exists(test_data_file):
        with open(test_data_file, "r", encoding="utf-8") as f:
            test_data = f.read()
    else:
        test_data = "{}"

    updated_data = st.text_area("Edit JSON here:", test_data, height=300)

    if st.button("Save Test Data 💾"):
        with open(test_data_file, "w", encoding="utf-8") as f:
            f.write(updated_data)
        st.success("Test data updated successfully!")

elif action == "View Results":
    ALLURE_REPORT_DIR = "reports/allure-report"
    ALLURE_ZIP_PATH = "reports/allure-report.zip"
    st.subheader("Test Reports")
     # Ensure Allure report exists before attempting to create a ZIP
    # if os.path.exists(ALLURE_REPORT_DIR) and not os.path.exists(ALLURE_ZIP_PATH):
    #     shutil.make_archive("reports/allure-report", 'zip', "reports", "allure-report")
    #     st.success("Allure report ZIP created successfully!")
    allure_report_path = "reports/allure-report/index.html"


    # Ensure Allure report directory exists before creating ZIP
    if os.path.exists(ALLURE_REPORT_DIR):
        if not os.path.exists(ALLURE_ZIP_PATH):
            shutil.make_archive(ALLURE_REPORT_DIR, 'zip', ALLURE_REPORT_DIR)
            st.success("✅ Allure report ZIP created successfully!")


        with open(allure_report_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            st.components.v1.html(html_content, height=800, scrolling=True)
        # Provide a download button for the Allure report ZIP





        with open(ALLURE_ZIP_PATH, "rb") as f:
            st.download_button(
                label="📥 Download Allure Report",
                data=f,
                file_name="allure-report.zip",
                mime="application/zip"
            )
        



        # Display the Allure     report in an iframe
        # st.write

    else:
        st.error("⚠️ No Allure reports found! Run tests first.")

