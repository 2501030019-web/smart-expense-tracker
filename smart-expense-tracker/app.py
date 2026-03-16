import streamlit as st
import pandas as pd
import requests
import base64
import plotly.express as px
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

# ---------- Background Image ----------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    bg = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        background: rgba(0,0,0,0.6);
        padding: 2rem;
        border-radius: 15px;
    }}

    .card {{
        background: rgba(255,255,255,0.1);
        padding:20px;
        border-radius:15px;
        backdrop-filter: blur(10px);
        box-shadow:0 0 15px rgba(0,0,0,0.3);
    }}
    </style>
    """
    st.markdown(bg, unsafe_allow_html=True)

set_bg("background.jpg")

# ---------- Load Lottie ----------
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_money = load_lottie(
"https://assets9.lottiefiles.com/packages/lf20_tutvdkg0.json"
)

# ---------- Header ----------
col1, col2 = st.columns([2,1])

with col1:
    st.title("💰 Smart Expense Tracker")
    st.write("Track your daily expenses in a beautiful dashboard")

with col2:
    st_lottie(lottie_money, height=200)

# ---------- Session Storage ----------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ---------- Add Expense ----------
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
    new_data = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Note": note
    }

    st.session_state.expenses.append(new_data)
    st.success("Expense Added Successfully ✅")

# ---------- DataFrame ----------
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
            title="Category Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            df,
            x="Category",
            y="Amount",
            title="Expense by Category",
            color="Category"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---------- History ----------
    st.subheader("🧾 Expense History")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No expenses added yet.")
