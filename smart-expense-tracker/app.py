import streamlit as st
import requests
import pandas as pd

# Safe import for lottie
try:
    from streamlit_lottie import st_lottie
except:
    st_lottie = None

st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

# Load lottie animation
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_animation = load_lottie("https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json")

# Title
st.title("💰 Smart Expense Tracker")

# Show animation if available
if st_lottie and lottie_animation:
    st_lottie(lottie_animation, height=300)

st.write("Track your daily expenses easily.")

# Input form
st.header("Add Expense")

col1, col2, col3 = st.columns(3)

with col1:
    date = st.date_input("Date")

with col2:
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )

with col3:
    amount = st.number_input("Amount", min_value=0)

note = st.text_input("Note")

if st.button("Add Expense"):
    st.success("Expense Added Successfully!")

# Example table
data = {
    "Date": ["2026-03-15", "2026-03-16"],
    "Category": ["Food", "Travel"],
    "Amount": [200, 500]
}

df = pd.DataFrame(data)

st.header("Expense History")
st.dataframe(df)

st.write("Total Expense:", df["Amount"].sum())
