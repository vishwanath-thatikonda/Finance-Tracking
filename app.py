
import streamlit as st
from database import init_db, add_transaction, get_transactions
from auth import create_user, authenticate_user
from utils import plot_expenses
import pandas as pd
from datetime import datetime

init_db()

st.title("Personal Finance Tracker")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ''

if not st.session_state.logged_in:
    option = st.selectbox("Login or Sign Up", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if option == "Sign Up":
        if st.button("Create Account"):
            if create_user(username, password):
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username already exists.")
    else:
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")
else:
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.experimental_rerun()

    st.subheader("Add New Transaction")
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Income", "Expense"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    if st.button("Add Transaction"):
        add_transaction(st.session_state.username, date.strftime("%Y-%m-%d"),
                        category, description, amount)
        st.success("Transaction added successfully!")

    st.subheader("Transaction History")
    transactions = get_transactions(st.session_state.username)
    df = pd.DataFrame(transactions, columns=['Date', 'Category', 'Description', 'Amount'])
    st.dataframe(df)

    st.subheader("Expense Analysis")
    fig = plot_expenses(transactions)
    if fig:
        st.pyplot(fig)
    else:
        st.info("No transactions to display.")
