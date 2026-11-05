# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
with st.form("survey_form"):
    category_input = st.text_input("Enter a category:")
    value_input = st.text_input("Enter a corresponding value:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        if category_input.strip() == "" or value_input.strip() == "":
            st.error("Please fill in both fields.")
        else:
            try:
                value = float(value_input)
            except ValueError:
                st.error("Value must be a number.")
            else:
                with open("data.csv", "a", newline="") as f:
                    csv.writer(f).writerow([category_input.strip(), value])
                st.success("Your data has been submitted!")
                st.write(f"You entered: **Category:** {category_input}, **Value:** {value}")


# DATA DISPLAY
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    current_data_df = pd.read_csv('data.csv')
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")