import streamlit as st
import pandas as pd
from datetime import date

st.title("📚 Homework Tracker")

# Create storage
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Add homework
st.header("Add Homework")

subject = st.text_input("Subject")
task = st.text_input("Homework Task")
due_date = st.date_input("Due Date", min_value=date.today())

if st.button("Add Homework"):
    if subject and task:
        st.session_state.tasks.append({
            "Subject": subject,
            "Task": task,
            "Due Date": due_date,
            "Completed": False
        })
        st.success("Homework added!")

# Display homework
st.header("Homework List")

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)

    for i, row in df.iterrows():
        completed = st.checkbox(
            f"{row['Subject']} - {row['Task']} (Due: {row['Due Date']})",
            value=row["Completed"],
            key=i
        )
        st.session_state.tasks[i]["Completed"] = completed

    st.subheader("Summary")
    total = len(st.session_state.tasks)
    completed = sum(task["Completed"] for task in st.session_state.tasks)

    st.metric("Total Homework", total)
    st.metric("Completed", completed)
    st.metric("Remaining", total - completed)

else:
    st.info("No homework added yet.")  