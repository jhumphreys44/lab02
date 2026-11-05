# This creates the page for displaying data visualizations.
import matplotlib.pyplot as plt
import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
import json
import pandas as pd

with open("data.json", "r") as f:
    data = json.load(f)

weeklyHours = data["weeklyHours"]

st.subheader("Static Chart: Weekly Hours Breakdown")

df = pd.DataFrame(list(weeklyHours.items()), columns=["Activity", "Hours"])
df = df.set_index("Activity")

st.bar_chart(df)

st.subheader("Dynamic Chart: Pick Your Activities")

allActivities = []
for activity in weeklyHours:
    allActivities.append(activity)

if "selected_activities" not in st.session_state:
    st.session_state.selected_activities = allActivities

selected = st.multiselect("Choose activities to display:", allActivities, st.session_state.selected_activities)

st.session_state.selected_activities = selected

values = []
for activity in selected:
    values.append(weeklyHours[activity])

if len(selected) > 0:
    mean1 = pd.Series(values).mean()
    median1 = pd.Series(values).median()

    # Previous stats are kept in session state so the metrics can show a change
    prev_mean1 = st.session_state.get("p1_prev_mean", mean1)
    prev_median1 = st.session_state.get("p1_prev_median", median1)

    col1, col2 = st.columns(2)
    col1.metric("Mean Hours", f"{mean1:.2f}", delta=round(mean1 - prev_mean1, 2))
    col2.metric("Median Hours", f"{median1:.2f}", delta=round(median1 - prev_median1, 2))

    st.session_state.p1_prev_mean = mean1
    st.session_state.p1_prev_median = median1

    fig, ax = plt.subplots()
    ax.pie(values, labels=selected)
    ax.set_title("Hours Spent on Selected Activities")
    st.pyplot(fig)
else:
    st.info("Select at least one activity to see the chart.")

# PART 2: GRAPHS FROM data.csv
import altair as alt

st.divider()
st.header("Part 2: Survey Data")

csv_df = pd.read_csv("data.csv")
csv_df["Value"] = pd.to_numeric(csv_df["Value"], errors="coerce")
csv_df = csv_df.dropna()

if csv_df.empty:
    st.info("No survey data yet. Add some on the Survey page!")
else:
    # STATIC CHART (Altair bar chart)
    st.subheader("Static Chart: Total Value by Category")
    totals = csv_df.groupby("Category", as_index=False)["Value"].sum()
    bar = alt.Chart(totals).mark_bar().encode(
        x=alt.X("Category:N", title="Category"),
        y=alt.Y("Value:Q", title="Total Value"),
        color=alt.Color("Category:N", legend=None),
    ).properties(title="Total Value by Category")
    st.altair_chart(bar)

    # DYNAMIC CHART (Matplotlib line chart + st.metric)
    st.subheader("Dynamic Chart: Survey Entries Over Time")
    total_rows = len(csv_df)

    if total_rows < 2:
        st.info("Submit at least 2 survey entries to use this chart.")
    else:
        n = st.slider("Number of entries to show:", 1, total_rows, total_rows, key="entries_slider")
        shown = csv_df.head(n)

        mean = shown["Value"].mean()
        median = shown["Value"].median()

        # Previous stats are kept in session state so the metrics can show a change
        prev_mean = st.session_state.get("prev_mean", mean)
        prev_median = st.session_state.get("prev_median", median)

        col1, col2 = st.columns(2)
        col1.metric("Mean", f"{mean:.2f}", delta=round(mean - prev_mean, 2))
        col2.metric("Median", f"{median:.2f}", delta=round(median - prev_median, 2))

        st.session_state.prev_mean = mean
        st.session_state.prev_median = median

        fig2, ax2 = plt.subplots()
        ax2.plot(range(1, n + 1), shown["Value"], marker="o")
        ax2.set_title("Survey Values by Entry")
        ax2.set_xlabel("Entry Number")
        ax2.set_ylabel("Value")
        st.pyplot(fig2)