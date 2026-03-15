import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load trained model
model = joblib.load("smart-expense-tracker/expense_model.pkl")
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
from streamlit_lottie import st_lottie

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

# -------- LOAD MODEL --------
model = joblib.load("expense_model.pkl")

# -------- LOAD ANIMATION --------
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie(
    "https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json"
)

# -------- HEADER SECTION --------
col1, col2 = st.columns(2)

with col1:
    st.title("💰 Smart Expense Tracker with Analytics")
    st.write("This app predicts the expense category using Machine Learning.")
    st.write("Enter your expense details in the sidebar.")

with col2:
    st_lottie(lottie_animation, height=250)

# -------- IMAGE --------
st.image("expense.png", caption="Manage your expenses smartly", use_container_width=True)

# -------- SIDEBAR INPUT --------
st.sidebar.header("Enter Expense Details")

account = st.sidebar.number_input("Account ID", min_value=0)

amount = st.sidebar.number_input("Expense Amount", min_value=0.0)

transaction = st.sidebar.selectbox(
    "Transaction Type",
    ["Expense", "Income"]
)

# Encode value
if transaction == "Expense":
    transaction = 0
else:
    transaction = 1

# -------- PREDICTION --------
if st.sidebar.button("Predict Category"):

    data = np.array([[account, amount, transaction]])

    prediction = model.predict(data)

    st.success(f"Predicted Expense Category Code: {prediction[0]}")

# -------- ANALYTICS SECTION --------
st.subheader("📊 Expense Analytics")

df = pd.read_csv("dataset.csv")

chart = df['Category'].value_counts()

st.bar_chart(chart)

# -------- PIE CHART --------
st.subheader("Expense Distribution")

st.write(df['Category'].value_counts())

# -------- DATA PREVIEW --------
st.subheader("Dataset Preview")

st.dataframe(df.head())
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

st.title("💰 Smart Expense Tracker with Analytics")

st.write("Predict the expense category using Machine Learning")

st.sidebar.header("Enter Expense Details")

# User Inputs
account = st.sidebar.number_input("Account ID", min_value=0)

amount = st.sidebar.number_input("Expense Amount", min_value=0.0)

transaction = st.sidebar.selectbox(
    "Transaction Type",
    ["Expense", "Income"]
)

# Encode transaction type
if transaction == "Expense":
    transaction = 0
else:
    transaction = 1

# Prediction Button
if st.sidebar.button("Predict Category"):

    data = np.array([[account, amount, transaction]])

    prediction = model.predict(data)

    st.success(f"Predicted Expense Category Code: {prediction[0]}")

# Analytics Section
st.subheader("📊 Expense Analytics")

df = pd.read_csv("smart-expense-tracker/dataset.csv")

category_counts = df['Category'].value_counts()

st.bar_chart(category_counts)

st.subheader("Dataset Preview")
st.dataframe(df.head())
