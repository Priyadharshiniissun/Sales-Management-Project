import streamlit as st
from datetime import date

st.set_page_config(page_title="Centralised dashboard",page_icon="📊",layout="wide")

if st.session_state.role != "Admin":
    st.error("Access Denied")
    st.stop()

st.sidebar.title("Admin Dashboard")
st.sidebar.write("Welcome!", st.session_state.username)
st.sidebar.write("Branch ID:", st.session_state.branch_id)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("app.py")

import pyodbc
import pandas as pd

page=st.sidebar.selectbox("Page",["Customer Sales","Payment Splits","Add Customer form","Add Payment form"])

branch_id = st.session_state.branch_id
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=VIKRAM\\SQLEXPRESS01;"
    "DATABASE=Sales_Management;"
    "Trusted_Connection=yes;")
cursor = conn.cursor()

if page == "Customer Sales":
    st.markdown( "<h1 style='text-align: center;'>Sales Dashboard</h1>",unsafe_allow_html=True)
    query = """SELECT  * FROM customer_sales WHERE branch_id = ?"""

    df = pd.read_sql(query, conn, params=[branch_id])
    df["date"] = pd.to_datetime(df["date"])
    col1, col2, col3 = st.columns(3)


    with col1:
       date_range = st.date_input("Select Date Range",[])
    with col2:
        branch_list = ["All"] + sorted(df["branch_id"].unique().tolist())
        selected_branch = st.selectbox("Select Branch",branch_list)
    with col3:
        product_list = ["All"] + list(df["product_name"].unique())
        selected_product = st.selectbox("Select Product",product_list)

    filtered_df = df.copy()

    if len(date_range) == 2:

        start_date, end_date = date_range

        start_date = pd.Timestamp(start_date)

        end_date = pd.Timestamp(end_date)

        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date) &
            (filtered_df["date"] <= end_date)
        ]

    if selected_branch != "All":

        filtered_df = filtered_df[filtered_df["branch_id"] == selected_branch]

    if selected_product != "All":
        filtered_df = filtered_df[filtered_df["product_name"] == selected_product]


    total_sales = filtered_df["gross_sales"].sum()
    total_received = filtered_df["received_amount"].sum()
    total_pending = filtered_df["pending_amount"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Sales",value=f"₹{total_sales:,}")
    with col2:
        st.metric(label="Received Amount",value=f"{total_received:,}")
    with col3:
        st.metric(label="Pending Amount",value=f"₹{total_pending:,}")
        
    st.divider()

    edited_df = st.dataframe(filtered_df)

if page == "Payment Splits":
    st.markdown( "<h1 style='text-align: center;'>Sales Dashboard</h1>",unsafe_allow_html=True)
    query = """SELECT * FROM payment_splits"""
    df = pd.read_sql(query, conn)
    st.dataframe(df)
    
if page=="Add Customer form":
    st.markdown( "<h1 style='text-align: center;'>Sales Dashboard</h1>",unsafe_allow_html=True)
    with st.form("Add Customer"):
    
        branch_id = st.selectbox("Branch ID",[1,2,3])
        sales_date = st.date_input("Date",value=date.today())
        customer_name = st.text_input("Customer Name")
        mobile_number = st.text_input("Mobile Number")
        product_name = st.text_input("Product Name")
        gross_sales = st.text_input("Gross Sales")
        status=st.selectbox("Status",["Open","Close"])
        
        submit = st.form_submit_button("Add Sales")


        if submit:
            query = """INSERT INTO customer_sales(branch_id,[date],name,mobile_number,product_name,gross_sales,status)
            VALUES (?, ?, ?, ?, ?, ?, ?)"""
            
            values = (branch_id,sales_date,customer_name,mobile_number,product_name,gross_sales,status)

            cursor.execute(query, values)
            conn.commit()

            st.success("Sales Record Added Successfully!")

if page=="Add Payment form":

    with st.form("Add Payment"):
        st.markdown( "<h1 style='text-align: center;'>Sales Dashboard</h1>",unsafe_allow_html=True)
        sale_id=st.text_input("Sale ID")
        payment_date=st.date_input("Date",value=date.today())
        amount_paid=st.text_input("Amount Paid")
        payment_method=st.selectbox("Payment Methof",["Cash","UPI","Card"])
        
        submit = st.form_submit_button("Add Payment")

        if submit:
            query = """INSERT INTO payment_splits(sale_id,payment_date,amount_paid,payment_method)
            VALUES (?, ?, ?, ?)"""

            values=(sale_id,payment_date,amount_paid,payment_method)

            cursor.execute(query, values)
            conn.commit()

            st. success("Payment Added Successfullly!")
    

conn.close()
