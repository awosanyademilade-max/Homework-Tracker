
import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(
    page_title="Homework Tracker",
    page_icon="📚",
    layout="centered"
)

FILE = "homework.csv"

COLUMNS = ["Subject", "Task", "Due Date", "Completed"]

# Create the CSV file if it does not exist
if not os.path.exists(FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(FILE, index=False)


# Load homework from CSV
def load_tasks():
    df = pd.read_csv(FILE)

    for column in COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df = df[COLUMNS]
    df["Subject"] = df["Subject"].fillna("").astype(str)
    df["Task"] = df["Task"].fillna("").astype(str)
    df["Due Date"] = df["Due Date"].fillna("").astype(str)
    df["Completed"] = (
        df["Completed"].astype(str).str.lower() == "true"
    )

    return df


# Save homework to CSV
def save_tasks(df):
    df.to_csv(FILE, index=False)


st.title("📚 Homework Tracker")
st.write("Organise your homework and keep track of deadlines.")

df = load_tasks()

# Dashboard summary
today = date.today()
due_dates = pd.to_datetime(df["Due Date"], errors="coerce").dt.date

total = len(df)
completed = int(df["Completed"].sum())
remaining = total - completed

overdue = sum(
    1
    for i in df.index
    if not df.at[i, "Completed"]
    and pd.notna(due_dates.at[i])
    and due_dates.at[i] < today
)

col1, col2 = st.columns(2)
col1.metric("📋 Total Tasks", total)
col2.metric("✅ Completed", completed)

col3, col4 = st.columns(2)
col3.metric("📝 Remaining", remaining)
col4.metric("⚠️ Overdue", overdue)

st.divider()

# Add homework
st.subheader("➕ Add Homework")

with st.form("add_homework", clear_on_submit=True):
    subject = st.text_input("Subject")
    task = st.text_input("Homework task")
    due_date = st.date_input("Due date", value=today)

    submitted = st.form_submit_button("Add Homework")

    if submitted:
        if subject.strip() and task.strip():
            new_task = pd.DataFrame([{
                "Subject": subject.strip(),
                "Task": task.strip(),
                "Due Date": due_date.isoformat(),
                "Completed": False
            }])

            df = pd.concat([df, new_task], ignore_index=True)
            save_tasks(df)

            st.success("Homework added!")
            st.rerun()
        else:
            st.error("Please enter both a subject and a task.")

st.divider()

# Display and update homework
st.subheader("📖 Your Homework")

if df.empty:
    st.info("No homework yet. Add your first task above.")
else:
    for i in df.index:
        with st.container(border=True):
            st.write(f"**{df.at[i, 'Subject']}**")
            st.write(df.at[i, "Task"])
            st.write(f"📅 Due: {df.at[i, 'Due Date']}")

            if (
                not df.at[i, "Completed"]
                and pd.notna(due_dates.at[i])
                and due_dates.at[i] < today
            ):
                st.error("Overdue!")

            is_completed = st.checkbox(
                "Completed",
                value=bool(df.at[i, "Completed"]),
                key=f"completed_{i}"
            )

            if is_completed != bool(df.at[i, "Completed"]):
                df.at[i, "Completed"] = is_completed
                save_tasks(df)
                st.rerun()

            if st.button("🗑️ Delete task", key=f"delete_{i}"):
                df = df.drop(index=i).reset_index(drop=True)
                save_tasks(df)
                st.rerun()

st.caption("Keep organised, meet deadlines and get your homework done!")
