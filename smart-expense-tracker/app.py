import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load trained model
model = joblib.load("expense_model.pkl")

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

df = pd.read_csv("dataset.csv")

category_counts = df['Category'].value_counts()

st.bar_chart(category_counts)

st.subheader("Dataset Preview")
st.dataframe(df.head())