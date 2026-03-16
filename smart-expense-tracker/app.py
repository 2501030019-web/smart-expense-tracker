import streamlit as st
import pandas as pd
import requests
import base64
import os
import plotly.express as px

# Safe import
try:
    from streamlit_lottie import st_lottie
except:
    st_lottie = None

st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

# ---------- Background Function ----------
def set_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        # Background CSS
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

[data-testid="stToolbar"]{
right: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- Lottie Animation ----------
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
    st.write("Track your daily expenses with a modern dashboard")

with col2:
    if st_lottie and lottie_money:
        st_lottie(lottie_money, height=200)

# ---------- Session State ----------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ---------- Expense Form ----------
st.subheader("➕ Add New Expense")

col1, col2, col3 = st.columns(3)

with col1:
    date = st.date_input("Date")

with col2:
    category = st.selectbox(
        "Category",
        ["Food","Travel","Shopping","Bills","Entertainment","Other"]
    )

with col3:
    amount = st.number_input("Amount", min_value=0)

note = st.text_input("Note")

if st.button("Add Expense"):

    new_expense = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Note": note
    }

    st.session_state.expenses.append(new_expense)

    st.success("Expense Added Successfully ✅")

# ---------- Data ----------
df = pd.DataFrame(st.session_state.expenses)

# ---------- Dashboard ----------
if not df.empty:

    st.subheader("📊 Dashboard")

    total_expense = df["Amount"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total Expense", f"₹ {total_expense}")

    food_total = df[df["Category"]=="Food"]["Amount"].sum()
    col2.metric("🍔 Food Expense", f"₹ {food_total}")

    travel_total = df[df["Category"]=="Travel"]["Amount"].sum()
    col3.metric("🚕 Travel Expense", f"₹ {travel_total}")

    # ---------- Charts ----------
    st.subheader("📈 Expense Analytics")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            df,
            values="Amount",
            names="Category",
            title="Expense Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            df,
            x="Category",
            y="Amount",
            color="Category",
            title="Expense by Category"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---------- Expense History ----------
    st.subheader("🧾 Expense History")

    st.dataframe(df, use_container_width=True)

else:
    st.info("No expenses added yet.")
