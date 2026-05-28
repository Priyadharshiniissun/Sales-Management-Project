import streamlit as st
from datetime import date
st.set_page_config(
    page_title="Centralised dashboard",
    page_icon="📊",
    layout="wide"
)

    
if st.session_state.role != "Super Admin":
    st.error("Access Denied")
    st.stop()

st.sidebar.title("Super Admin Dashboard")
st.sidebar.write("Welcome", st.session_state.username)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("app.py")


import pyodbc
import pandas as pd

page=st.sidebar.selectbox("Page",["Customer Sales","Payment Splits","Add Customer form","Add Payment form","SQL Analytics"])


conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=VIKRAM\\SQLEXPRESS01;"
    "DATABASE=Sales_Management;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()


if page == "Customer Sales":
    st.markdown( "<h1 style='text-align: center;'>Sales Dashboard</h1>",unsafe_allow_html=True)
    query = """SELECT  * FROM customer_sales """

    df = pd.read_sql(query, conn)
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

if page =="Add Customer form":
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

if page == "Add Payment form":
    st.markdown( "<h1 style='text-align: center;'>Sales Dashboard</h1>",unsafe_allow_html=True)
    with st.form("Add Payment"):

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

            st. success("Payment Added SUccessfullly!")

if page == "SQL Analytics":
    st.markdown( "<h1 style='text-align: center;color: green;'>SQL Analytics</h1>",unsafe_allow_html=True)
    Ques=st.selectbox("Question",[
        "Retrieve all records from the customer_sales table",
        "Retrieve all records from the branches table",
        "Retrieve all records from the payment_splits table",
        "Retrieve all sales belonging to the Chennai branch",
        "Calculate the total gross sales across all branches",
        "Calculate the total received amount across all sales",
        "Count the total number of sales per branch",
        "Find the average gross sales amount",
        "Retrieve sales details along with the branch name",
        "Retrieve sales details along with total payment received (using payment_splits)",
        "Show branch-wise total gross sales (using JOIN & GROUP BY)",
        "Display sales along with payment method used",
        "Retrieve sales along with branch admin name",
        "Retrieve top 3 highest gross sales",
        "Find the branch with highest total gross sales",
        "Calculate payment method-wise total collection (Cash / UPI / Card)"])

    if Ques == "Retrieve all records from the customer_sales table":
        st.subheader("Customer Sales Table")
        query1 = "SELECT * FROM customer_sales"
        customer_sales_df = pd.read_sql(query1, conn)
        st.dataframe(customer_sales_df)
        
    if Ques == "Retrieve all records from the branches table":
        st.subheader("Branches Table")
        query2 = "SELECT * FROM branches"
        branches_df = pd.read_sql(query2, conn)
        st.dataframe(branches_df)
        
    if Ques == "Retrieve all records from the payment_splits table":
        st.subheader("Payment Splits Table")
        query3 = "SELECT * FROM payment_splits"
        payment_splits_df = pd.read_sql(query3, conn)
        st.dataframe(payment_splits_df)
        
    if Ques == "Retrieve all sales belonging to the Chennai branch":
        st.title("Chennai Branch Sales")
        query4 = """SELECT *FROM customer_sales Where branch_id=1"""
        df = pd.read_sql(query4, conn)
        st.dataframe(df)
        
    if Ques == "Calculate the total gross sales across all branches":
        st.title("Total Gross Sales Across All Branches")
        query5 = """SELECT SUM(gross_sales) AS total_gross FROM customer_sales"""
        df = pd.read_sql(query5, conn)
        total_gross = df["total_gross"][0]
        st.metric(label="Total Gross Sales",value=f"₹ {total_gross:,.2f}")
        
    if Ques == "Calculate the total received amount across all sales":
        st.title("Total Received Amount Across All Branches")
        query6 = """SELECT SUM(received_amount) AS total_received FROM customer_sales"""
        df = pd.read_sql(query6, conn)
        total_received = df.iloc[0]["total_received"]
        st.metric(label="Total received amount",value=f"₹ {total_received:,.2f}")

    if Ques == "Count the total number of sales per branch":
        st.title("Total Sales per Branch")
        query7 = """SELECT b.branch_name,COUNT(cs.sale_id) AS total_sales FROM customer_sales cs
        INNER JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name ORDER BY b.branch_name"""
        df = pd.read_sql(query7, conn)
        st.dataframe(df)

    if Ques == "Find the average gross sales amount":
        st.title("Average Gross Sales Across All Branches")
        query8 = """SELECT Avg(gross_sales) AS avg_gross FROM customer_sales"""
        df = pd.read_sql(query8, conn)
        avg_gross = df["avg_gross"][0]
        st.metric(label="Average Gross Sales",value=f"₹ {avg_gross:,.2f}")

    if Ques == "Retrieve sales details along with the branch name":
        st.title("Sales Details With Branch Name")
        query9 = """SELECT cs.sale_id,b.branch_name,cs.name,cs.product_name,cs.gross_sales,cs.received_amount,cs.status
        FROM customer_sales cs INNER JOIN branches b ON cs.branch_id = b.branch_id"""
        df = pd.read_sql(query9, conn)
        st.dataframe(df)

    if Ques == "Retrieve sales details along with total payment received (using payment_splits)":
        st.title("Sales Details With Total Payment Received")
        query16 = """SELECT cs.sale_id,cs.name,cs.product_name,cs.gross_sales,SUM(ps.amount_paid) AS total_payment_received
        FROM customer_sales cs LEFT JOIN payment_splits ps ON cs.sale_id = ps.sale_id
        GROUP BY cs.sale_id,cs.name,cs.product_name,cs.gross_sales ORDER BY cs.sale_id"""
        df = pd.read_sql(query16, conn)
        st.dataframe(df)

    if Ques == "Show branch-wise total gross sales (using JOIN & GROUP BY)":
        st.title("Branch-wise Gross Sales")
        query10 = """SELECT b.branch_name,SUM(cs.gross_sales) AS total_gross_sales FROM customer_sales cs
        INNER JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name ORDER BY b.branch_name"""
        df = pd.read_sql(query10, conn)
        st.dataframe(df)
        
    if Ques == "Display sales along with payment method used":
        st.title("Sales With Payment Method")
        query11 = """SELECT cs.sale_id,cs.name,cs.product_name,ps.payment_method,ps.amount_paid
        FROM customer_sales cs INNER JOIN payment_splits ps ON cs.sale_id = ps.sale_id"""
        df = pd.read_sql(query11, conn)
        st.dataframe(df)

    if Ques =="Retrieve sales along with branch admin name":
        st.title("Sales Details With Branch Admin Name")
        query12 = """SELECT cs.sale_id,b.branch_name,b.branch_admin_name,cs.name,cs.product_name,cs.gross_sales,cs.received_amount,cs.status
        FROM customer_sales cs INNER JOIN branches b ON cs.branch_id = b.branch_id"""
        df = pd.read_sql(query12, conn)
        st.dataframe(df)

    if Ques == "Retrieve top 3 highest gross sales":
        st.title("Top 3 Highest Gross Sales")
        query13 = """SELECT TOP 3 sale_id,name,product_name,gross_sales
        FROM customer_sales ORDER BY gross_sales DESC"""
        df = pd.read_sql(query13, conn)
        st.dataframe(df)

    if Ques == "Find the branch with highest total gross sales":
        st.title("Branch With Highest Gross Sales")
        query14 = """SELECT TOP 1 b.branch_name,SUM(cs.gross_sales) AS total_gross_sales FROM customer_sales cs
        INNER JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name ORDER BY total_gross_sales DESC"""
        df = pd.read_sql(query14, conn)
        st.dataframe(df)

    if Ques == "Calculate payment method-wise total collection (Cash / UPI / Card)":
        st.title("Payment Method-wise Total Collection")
        query15 = """SELECT payment_method,SUM(amount_paid) AS total_collection FROM payment_splits
        GROUP BY payment_method ORDER BY payment_method"""
        df = pd.read_sql(query15, conn)
        st.dataframe(df)
conn.commit()
conn.close()









