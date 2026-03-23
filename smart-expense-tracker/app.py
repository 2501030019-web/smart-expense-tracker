import streamlit as st
import pandas as pd
import requests
import base64
import os
import plotly.express as px
import pickle

# ---------- Load Model ----------
try:
    model = pickle.load(open("expense_model.pkl", "rb"))
except:
    model = None

# ---------- Prediction Function ----------
def predict_category(amount, note):
    try:
        if model is None:
            return "Other"

        # 👉 Adjust according to your training
        input_data = pd.DataFrame({
            "Amount": [amount],
            "Note": [note]
        })

        return model.predict(input_data)[0]

    except:
        return "Other"

# ---------- Page Config ----------
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

# ---------- Background ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://images.unsplash.com/photo-1554224155-6726b3ff858f");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}
[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("💰 Smart Expense Tracker with AI 🤖")
st.write("Track & predict your expenses automatically")

# ---------- Session ----------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# =========================================================
# 🔹 SECTION 1: MANUAL ENTRY
# =========================================================
st.subheader("➕ Add New Expense")

col1, col2, col3 = st.columns(3)

with col1:
    date = st.date_input("Date")

with col2:
    st.write("🤖 Category will be predicted")

with col3:
    amount = st.number_input("Amount", min_value=0)

note = st.text_input("Note")

if st.button("Add Expense"):

    category = predict_category(amount, note)

    new_expense = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Note": note
    }

    st.session_state.expenses.append(new_expense)

    st.success(f"Added under '{category}' ✅")

# =========================================================
# 🔹 SECTION 2: CSV UPLOAD
# =========================================================
st.subheader("📂 Upload CSV for Bulk Prediction")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:

    df_csv = pd.read_csv(uploaded_file)

    st.write("### 📄 Uploaded Data")
    st.dataframe(df_csv)

    try:
        # 👉 Adjust according to your model
        if "Amount" in df_csv.columns and "Note" in df_csv.columns:
            input_data = df_csv[["Amount", "Note"]]
        elif "Amount" in df_csv.columns:
            input_data = df_csv[["Amount"]]
        else:
            st.error("CSV must contain 'Amount' column")
            st.stop()

        df_csv["Category"] = model.predict(input_data)

        st.success("✅ Prediction Done!")

        st.write("### 📊 Predicted Data")
        st.dataframe(df_csv)

        # Add to session data
        st.session_state.expenses.extend(df_csv.to_dict("records"))

    except Exception as e:
        st.error(f"Prediction Error: {e}")

# =========================================================
# 🔹 SECTION 3: DASHBOARD
# =========================================================
df = pd.DataFrame(st.session_state.expenses)

if not df.empty:

    st.subheader("📊 Dashboard")

    total = df["Amount"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total Expense", f"₹ {total}")

    food_total = df[df["Category"]=="Food"]["Amount"].sum()
    col2.metric("🍔 Food", f"₹ {food_total}")

    travel_total = df[df["Category"]=="Travel"]["Amount"].sum()
    col3.metric("🚕 Travel", f"₹ {travel_total}")

    # ---------- Charts ----------
    st.subheader("📈 Analytics")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(df, values="Amount", names="Category", title="Category Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(df, x="Category", y="Amount", color="Category", title="Expense by Category")
        st.plotly_chart(fig2, use_container_width=True)

    # ---------- Summary ----------
    st.subheader("📊 Category-wise Summary")

    summary = df.groupby("Category")["Amount"].sum()
    st.bar_chart(summary)

    # ---------- History ----------
    st.subheader("🧾 Expense History")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No data available yet.")
