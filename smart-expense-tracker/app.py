import streamlit as st
import pandas as pd
import requests
import base64
import os
import plotly.express as px
import pickle

# ---------- Load Model ----------
model = pickle.load(open("expense_model.pkl", "rb"))

# ---------- Prediction Function ----------
def predict_category(amount, note):
    try:
        # ⚠️ Change this according to your training
        input_data = pd.DataFrame({
            "Amount": [amount],
            "Note": [note]
        })

        prediction = model.predict(input_data)[0]
        return prediction

    except:
        return "Other"

# ---------- Lottie ----------
try:
    from streamlit_lottie import st_lottie
except:
    st_lottie = None

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

# ---------- Lottie Function ----------
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_money = load_lottie(
"https://assets9.lottiefiles.com/packages/lf20_tutvdkg0.json"
)

# ---------- Header ----------
col1, col2 = st.columns([2,1])

with col1:
    st.title("💰 Smart Expense Tracker")
    st.write("Track your daily expenses with AI-powered category prediction 🤖")

with col2:
    if st_lottie and lottie_money:
        st_lottie(lottie_money, height=200)

# ---------- Session ----------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ---------- Form ----------
st.subheader("➕ Add New Expense")

col1, col2, col3 = st.columns(3)

with col1:
    date = st.date_input("Date")

with col2:
    st.write("🤖 Category will be predicted automatically")

with col3:
    amount = st.number_input("Amount", min_value=0)

note = st.text_input("Note")

# ---------- Add Button ----------
if st.button("Add Expense"):

    predicted_category = predict_category(amount, note)

    new_expense = {
        "Date": date,
        "Category": predicted_category,
        "Amount": amount,
        "Note": note
    }

    st.session_state.expenses.append(new_expense)

    st.success(f"Expense Added under '{predicted_category}' ✅")

# ---------- Data ----------
df = pd.DataFrame(st.session_state.expenses)

# ---------- Dashboard ----------
if not df.empty:

    st.subheader("📊 Dashboard")

    total_expense = df["Amount"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total Expense", f"₹ {total_expense}")

    # Category-wise totals
    food_total = df[df["Category"]=="Food"]["Amount"].sum()
    col2.metric("🍔 Food Expense", f"₹ {food_total}")

    travel_total = df[df["Category"]=="Travel"]["Amount"].sum()
    col3.metric("🚕 Travel Expense", f"₹ {travel_total}")

    # ---------- Analytics ----------
    st.subheader("📈 Expense Analytics")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            df,
            values="Amount",
            names="Category",
            title="Predicted Category Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            df,
            x="Category",
            y="Amount",
            color="Category",
            title="Predicted Expense by Category"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---------- Summary (IMPORTANT FOR MAM) ----------
    st.subheader("📊 Category-wise Prediction Summary")

    summary = df.groupby("Category")["Amount"].sum()
    st.bar_chart(summary)

    # ---------- History ----------
    st.subheader("🧾 Expense History")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No expenses added yet.")
