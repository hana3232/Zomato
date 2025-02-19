import os
import mysql.connector
from faker import Faker
from datetime import datetime, timedelta
import random
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import base64
import time

# Install required packages
os.system("pip install mysql-connector-python faker pandas matplotlib seaborn --upgrade")
class DatabaseManager:
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
    
    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host, user=self.user, port=self.port,
            password=self.password, database=self.database
        )
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query, data=None):
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall(), [desc[0] for desc in self.cursor.description]
    
    def insert_data(self, query, data):
        self.cursor.executemany(query, data)
        self.conn.commit()
    
    def update_data(self, query, data):
        self.cursor.execute(query, data)
        self.conn.commit()
    
    def delete_data(self, query, data):
        self.cursor.execute(query, data)
        self.conn.commit()

# Database Configuration
config = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "user": "Ud6xHKHHCuFbH6f.root",
    "port": 4000,
    "password": "jwl7QF0l1usUQwNi",
    "database": "Zomato"
}

db = DatabaseManager(**config)
db.connect()

# Multi-page setup
st.set_page_config(page_title="Zomato Data Analytics", page_icon="🍽️", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠Home", "🚀App View","💡Business Insights", "📝CRUD Operations", "🔍Data Insights","📊Visualization","🎉Thank You"])

# Load and display image with enhanced animation
def load_image_with_animation(image_path, width=800):
    st.markdown(
        f"""
        <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes bounceZoom {{
            0% {{ transform: scale(0.5) translateY(-50px); opacity: 0; }}
            50% {{ transform: scale(1.1) translateY(10px); opacity: 1; }}
            100% {{ transform: scale(1) translateY(0px); }}
        }}
        .animated-image {{
            animation: fadeIn 2s ease-out, bounceZoom 1.5s ease-out;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: {width}px;
        }}
        </style>
        <img class="animated-image" src="data:image/png;base64,{base64.b64encode(open(image_path, 'rb').read()).decode()}"/>
        """,
        unsafe_allow_html=True
    )

if page == "🏠Home":
    st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 48px;
            color: #FF6347;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-size: 22px;
            color: #555;
        }
        .container {
            text-align: center;
        }
        .button-container {
            display: flex;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
                       )
    load_image_with_animation("Zomato-Logo.png")
# Main Title and Subtitl
    st.markdown('<p class="subtitle">Analyze Orders, Restaurants, and Deliveries with Interactive Visualizations!</p>', unsafe_allow_html=True)


elif page == "🚀App View":
    st.video("https://youtu.be/5Hlj_h24vvM",width=400)
    st.markdown("[Visit Zomato Website](https://www.zomato.com)")

elif page == "💡Business Insights":
    load_image_with_animation("PngItem_695722-1-1024x720.png",width=400)
    st.title("🍽️ Zomato Data Pipeline - Business Insights")
    st.write("Analyze key business metrics and gain insights from your Zomato database.")    
    st.subheader("📊 Table Explanations")
    tables = {
        "Customer_Table": "Stores customer information such as Customer_ID, Name, Contact details, and Address.",
        "Restaurant_Table": "Contains details about restaurants including Restaurant_ID, Name, Location, Cuisine Type, and Ratings.",
        "Order_Table": "Holds records of all placed orders with Order_ID, Customer_ID, Restaurant_ID, Order Time, Status, and Total Amount.",
        "Delivery_Table": "Maintains delivery details including Delivery_ID, Order_ID, Delivery Person_ID, Delivery Status, and Time Taken.",
        "Delivery_Person_Table": "Stores information about delivery personnel, including Delivery_Person_ID, Name, Contact, and Assigned Orders."
    }
    for table, description in tables.items():
        st.write(f"**{table}**: {description}")
# Define DatabaseManager class and other code here...

if page == "📝CRUD Operations":
    Tables = {
        "Customer_Table": "Stores customer information such as Customer_ID, Name, Contact details, and Address.",
        "Restaurant_Table": "Contains details about restaurants including Restaurant_ID, Name, Location, Cuisine Type, and Ratings.",
        "Order_Table": "Holds records of all placed orders with Order_ID, Customer_ID, Restaurant_ID, Order Time, Status, and Total Amount.",
        "Delivery_Table": "Maintains delivery details including Delivery_ID, Order_ID, Delivery Person_ID, Delivery Status, and Time Taken.",
        "Delivery_Person_Table": "Stores information about delivery personnel, including Delivery_Person_ID, Name, Contact, and Assigned Orders."
    }
    st.header("🔄 Manage Database Records")
    table = st.selectbox("Select Table", list(Tables.keys()))
    operation = st.radio("Select Operation", ["Add", "Update", "Delete"])

    if operation == "Add":
        columns = st.text_input("Enter columns (comma separated)").split(',')
        values = st.text_input("Enter values (comma separated)").split(',')
        if len(columns) == len(values):
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
            if st.button("Add Record"):
                db.insert_data(query, [tuple(values)])
                st.success("Record added successfully!")
        else:
            st.error("The number of columns and values must be the same.")

    elif operation == "Update":
        column = st.text_input("Enter column to update")
        value = st.text_input("Enter new value")
        condition = st.text_input("Enter condition (e.g., id=5)")
        if column and value and condition:
            query = f"UPDATE {table} SET {column} = %s WHERE {condition}"
            if st.button("Update Record"):
                db.update_data(query, (value,))
                st.success("Record updated successfully!")
        else:
            st.error("All fields must be filled.")

    elif operation == "Delete":
        condition = st.text_input("Enter condition for deletion (e.g., id=5)")
        if condition:
            query = f"DELETE FROM {table} WHERE {condition}"
            if st.button("Delete Record"):
                db.delete_data(query, ())
                st.success("Record deleted successfully!")
        else:
            st.error("Please provide a condition for deletion.")


elif page == "🔍Data Insights":
    queries = {
        "Total Customers": "SELECT COUNT(*) FROM Customer_Table;",
        "Total Restaurants": "SELECT COUNT(*) FROM Restaurant_Table;",
        "Total Orders": "SELECT COUNT(*) FROM Order_Table;",
        "Total Deliveries": "SELECT COUNT(*) FROM Delivery_Table;",
        "Total Revenue Per Restaurant": "SELECT Restaurant_ID, SUM(Order_Amount) FROM Order_Table GROUP BY Restaurant_ID;",
        "Average Order Value": "SELECT AVG(Order_Amount) FROM Order_Table;",
        "Most Popular Restaurant": """SELECT o.Restaurant_ID, r.Restaurant_Name, COUNT(*) AS Order_Count FROM Order_Table o 
                                      JOIN Restaurant_Table r ON o.Restaurant_ID = r.Restaurant_ID 
                                      GROUP BY o.Restaurant_ID, r.Restaurant_Name ORDER BY Order_Count DESC LIMIT 10;""",
        "Most Ordered Cuisine": "SELECT Cusine_type, COUNT(*) FROM Restaurant_Table JOIN Order_Table ON Restaurant_Table.Restaurant_ID = Order_Table.Restaurant_ID GROUP BY Cusine_type ORDER BY COUNT(*) DESC LIMIT 10;",
        "Peak Order Time": """SELECT DATE_FORMAT(Order_Date, '%h %p') AS Order_Hour_Minute_AMPM,
                              COUNT(*) AS Order_Count FROM Order_Table 
                              GROUP BY Order_Hour_Minute_AMPM ORDER BY Order_Count DESC LIMIT 10;""",
        "Highest Rated Restaurant": "SELECT Restaurant_Name, MAX(Average_rating) as High_Rating FROM Restaurant_Table GROUP BY Restaurant_Name ORDER BY High_Rating DESC LIMIT 10;",
        "Orders Per Customer": """SELECT o.Customer_ID, c.Customer_Name, COUNT(*) AS Order_Count FROM Order_Table o JOIN Customer_Table c ON o.Customer_ID = c.Customer_ID GROUP BY o.Customer_ID, c.Customer_Name ORDER BY Order_Count DESC;""",
        "Fastest Delivery": """SELECT Order_ID, Delivery_Time, Estimated_Delivery_Time,
                            FLOOR(TIMESTAMPDIFF(SECOND, Estimated_Delivery_Time, Delivery_Time) / 60) AS Minutes,
                            TIMESTAMPDIFF(SECOND, Estimated_Delivery_Time, Delivery_Time) % 60 AS Seconds 
                            FROM Delivery_Table ORDER BY Minutes ASC, Seconds ASC LIMIT 10;""",
        "Slowest Delivery": """SELECT Order_ID, Delivery_Time,Estimated_Delivery_Time,
                              FLOOR(TIMESTAMPDIFF(SECOND, Estimated_Delivery_Time, Delivery_Time) / 60) AS Minutes,
                              TIMESTAMPDIFF(SECOND, Estimated_Delivery_Time, Delivery_Time) % 60 AS Seconds
                              FROM Delivery_Table ORDER BY Minutes DESC, Seconds DESC LIMIT 10;""",
        "Total Revenue Per Customer": """SELECT o.Customer_ID, c.Customer_Name, COUNT(*) AS Order_Count FROM Order_Table o JOIN Customer_Table c ON o.Customer_ID = c.Customer_ID GROUP BY o.Customer_ID, c.Customer_Name ORDER BY Order_Count DESC;""",
        "Most Active Delivery Person": """SELECT d.Delivery_Person_ID, dp.Person_Name, COUNT(*) AS Delivery_Count FROM Delivery_Table d JOIN Delivery_Person_Table dp ON d.Delivery_Person_ID = dp.Delivery_Person_ID GROUP BY d.Delivery_Person_ID, dp.Person_Name ORDER BY Delivery_Count DESC LIMIT 10;""",
        "Most Common Payment Method": "SELECT Payment_Mode, COUNT(*) FROM Order_Table GROUP BY Payment_Mode ORDER BY COUNT(*) DESC LIMIT 10;",
        "Orders by Status": "SELECT Order_Status, COUNT(*) FROM Order_Table GROUP BY Order_Status;",
        "Restaurants With Most Orders": """SELECT Restaurant_ID, COUNT(Order_ID) AS Order_Count FROM Order_Table GROUP BY Restaurant_ID ORDER BY Order_Count DESC LIMIT 15;""",
        "Top Spending Customers": """SELECT o.Customer_ID, c.Customer_Name, SUM(o.Order_Amount) AS Total_Order_Amount FROM Order_Table o JOIN Customer_Table c ON o.Customer_ID = c.Customer_ID GROUP BY o.Customer_ID ORDER BY Total_Order_Amount DESC LIMIT 15;"""
       ,"Total Order Deliver per day":"SELECT DATE(Order_Date) AS OrderDate, COUNT(Order_ID) AS TotalOrders FROM Order_Table GROUP BY OrderDate;" }

    selected_query = st.selectbox("📜 Select a query to execute:", list(queries.keys()))
    if st.button("🔍 Run Query"):
        st.markdown(f"**📚 Query:** `{queries[selected_query]}`")
        result, columns = db.execute_query(queries[selected_query])
        df = pd.DataFrame(result, columns=columns)
        st.dataframe(df, use_container_width=True, height=400)

elif page=="📊Visualization":

    st.title("📊 Zomato Data Visualization")

# Load your SQL queries dictionary
    queries = {
    "Total Revenue Per Restaurant": "SELECT Restaurant_ID, SUM(Order_Amount) FROM Order_Table GROUP BY Restaurant_ID;",
    "Average Order Value": "SELECT AVG(Order_Amount) FROM Order_Table;",
    "Most Popular Restaurant": """SELECT o.Restaurant_ID, r.Restaurant_Name, COUNT(*) AS Order_Count 
                                  FROM Order_Table o 
                                  JOIN Restaurant_Table r ON o.Restaurant_ID = r.Restaurant_ID 
                                  GROUP BY o.Restaurant_ID, r.Restaurant_Name 
                                  ORDER BY Order_Count DESC LIMIT 10;""",
    "Most Ordered Cuisine": """SELECT Cusine_type,COUNT(*) AS Order_Count
                               FROM Restaurant_Table 
                               JOIN Order_Table ON Restaurant_Table.Restaurant_ID = Order_Table.Restaurant_ID 
                               GROUP BY Cusine_type 
                               ORDER BY COUNT(*) DESC LIMIT 10;""",
    "Peak Order Time": """SELECT DATE_FORMAT(Order_Date, '%h %p') AS Order_Hour, COUNT(*) AS Order_Count 
                          FROM Order_Table GROUP BY Order_Hour ORDER BY Order_Count DESC LIMIT 10;""",
    "Highest Rated Restaurant": """SELECT Restaurant_Name, MAX(Average_Rating) AS High_Rating 
                                   FROM Restaurant_Table GROUP BY Restaurant_Name 
                                   ORDER BY High_Rating DESC LIMIT 10;""",
    "Orders Per Customer": """SELECT o.Customer_ID, c.Customer_Name, COUNT(*) AS Order_Count, o.Order_Date 
                              FROM Order_Table o 
                              JOIN Customer_Table c ON o.Customer_ID = c.Customer_ID 
                              GROUP BY o.Customer_ID, c.Customer_Name, o.Order_Date 
                              ORDER BY o.Order_Date;""",
    "Total Revenue Per Customer": """SELECT o.Customer_ID, c.Customer_Name, SUM(o.Order_Amount) AS Total_Revenue 
                                     FROM Order_Table o 
                                     JOIN Customer_Table c ON o.Customer_ID = c.Customer_ID 
                                     GROUP BY o.Customer_ID, c.Customer_Name 
                                     ORDER BY Total_Revenue DESC;""",
    "Most Active Delivery Person": """SELECT d.Delivery_Person_ID, dp.Person_Name, COUNT(*) AS Delivery_Count 
                                      FROM Delivery_Table d 
                                      JOIN Delivery_Person_Table dp ON d.Delivery_Person_ID = dp.Delivery_Person_ID 
                                      GROUP BY d.Delivery_Person_ID, dp.Person_Name 
                                      ORDER BY Delivery_Count DESC LIMIT 10;""",
    "Most Common Payment Method": "SELECT Payment_Mode, COUNT(*) FROM Order_Table GROUP BY Payment_Mode ORDER BY COUNT(*) DESC LIMIT 10;",
    "Orders by Status": "SELECT Order_Status, COUNT(*) FROM Order_Table GROUP BY Order_Status;",
    "Restaurants With Most Orders": """SELECT Restaurant_ID, COUNT(Order_ID) AS Order_Count 
                                       FROM Order_Table 
                                       GROUP BY Restaurant_ID 
                                       ORDER BY Order_Count DESC LIMIT 15;""",
    "Top Spending Customers": """SELECT o.Customer_ID, c.Customer_Name, SUM(o.Order_Amount) AS Total_Order_Amount 
                                 FROM Order_Table o 
                                 JOIN Customer_Table c ON o.Customer_ID = c.Customer_ID 
                                 GROUP BY o.Customer_ID 
                                 ORDER BY Total_Order_Amount DESC LIMIT 15;"""
     }

# Select query from dropdown
    selected_query = st.selectbox("📜 Select a query to execute:", list(queries.keys()))

# Execute the selected query
# Assuming db.execute_query(query) returns (result, columns)
    result, columns = db.execute_query(queries[selected_query])
    df = pd.DataFrame(result, columns=columns)

# Check if the DataFrame is empty
    if df.empty:
        st.warning("No data available for this query!")
    else:
        st.subheader(f"📊 Visualization for: {selected_query}")

    # Convert date columns to datetime format (if applicable)
        if "Order_Date" in df.columns:
            df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

    # --- Handling Different Visualizations ---

        if selected_query in ["Orders Per Customer"]:
        # Time Series Line Chart (Orders per Customer)
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df, x="Order_Date", y="Order_Count", hue="Customer_ID", marker="o")
            plt.xlabel("Order Date")
            plt.ylabel("Total Orders per Day")
            plt.title("Orders Per Customer")
            plt.xticks(rotation=45)
            st.pyplot(plt)
        elif selected_query == "Average Order Value":
            if not df.empty and df.shape[1] >= 1:  # Ensure df has at least 1 column
               plt.figure(figsize=(5, 5))  # A smaller plot for the average value
               sns.barplot(x=["Average Order Value"], y=[df.iloc[0, 0]], palette="viridis")  # A single bar for AOV
               plt.xlabel("Average Order Value")
               plt.ylabel("Value")
               plt.title("Average Order Value")
               st.pyplot(plt)
            else:
               st.warning("⚠ Data is missing for Average Order Value.")
               st.write("🔍 Data Preview:", df.head())  # Debugging output to see the first few rows

        elif selected_query in ["Total Revenue Per Customer", "Top Spending Customers"]:
    # Bar Plot for Revenue/Spending
             plt.figure(figsize=(12, 6))  # Increase figure size
             sns.barplot(x=df.iloc[:, 1], y=df.iloc[:, 2], palette="viridis")
             plt.xlabel("Customer Name")
             plt.ylabel("Total Revenue")
             plt.title(selected_query)
    
    # Adjust x-axis labels
             plt.xticks(rotation=45, ha='right')  # Rotate and align
    
           # Show fewer labels (optional)
             step = max(1, len(df) // 20)  # Show approximately 20 labels
             plt.xticks(ticks=range(0, len(df), step), labels=df.iloc[::step, 1])

             st.pyplot(plt)

        elif selected_query == "Restaurants With Most Orders":
            if not df.empty and df.shape[1] >= 2:  # Ensure df has at least 2 columns
               plt.figure(figsize=(12, 6))
               sns.barplot(x=df.iloc[:, 0], y=df.iloc[:, 1], palette="coolwarm")  # Restaurant_ID vs. Order_Count
               plt.xlabel(df.columns[0])  # Restaurant_ID
               plt.ylabel(df.columns[1])  # Order_Count
               plt.title("Restaurants With Most Orders")
               plt.xticks(rotation=45)
               st.pyplot(plt)
            else:
              st.warning("⚠ Data is missing or does not have enough columns for visualization.")
              st.write("🔍 Data Preview:", df.head())  # Debugging output to see the first few rows


        elif selected_query in ["Most Popular Restaurant", "Most Active Delivery Person"]:
        # Bar Chart for Top Categories
            plt.figure(figsize=(12, 6))
            sns.barplot(x=df.iloc[:, 1], y=df.iloc[:, 2], palette="coolwarm")
            plt.xlabel(df.columns[1])
            plt.ylabel(df.columns[2])
            plt.title(selected_query)
            plt.xticks(rotation=45)
            st.pyplot(plt)
        elif selected_query == "Most Ordered Cuisine":
            if not df.empty and df.shape[1] >= 2:  # Ensure df has at least 2 columns
             plt.figure(figsize=(12, 6))
             sns.barplot(x=df.iloc[:, 0], y=df.iloc[:, 1], palette="coolwarm")  # Cusine_type vs. Order_Count
             plt.xlabel(df.columns[0])  # Cusine_type
             plt.ylabel(df.columns[1])  # Order_Count
             plt.title("Most Ordered Cuisine")
             plt.xticks(rotation=45)
             st.pyplot(plt)
            else:
                st.warning("⚠ Data is missing or does not have enough columns for visualization.")
                st.write("🔍 Data Preview:", df.head())  # Debugging output

        elif selected_query in ["Orders by Status", "Most Common Payment Method"]:
        # Pie Chart for Category Distribution
            plt.figure(figsize=(8, 8))
            plt.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct="%1.1f%%", colors=sns.color_palette("pastel"))
            plt.title(selected_query)
            st.pyplot(plt)

        elif selected_query in ["Peak Order Time"]:
        # Line Chart for Peak Order Time
            plt.figure(figsize=(10, 5))
            sns.lineplot(x=df.iloc[:, 0], y=df.iloc[:, 1], marker="o", color="green")
            plt.xlabel("Order Hour")
            plt.ylabel("Order Count")
            plt.title("Peak Order Time")
            plt.xticks(rotation=45)
            st.pyplot(plt)

        else:
        # Generic Bar Plot for Other Queries
            plt.figure(figsize=(12, 6))
            sns.barplot(x=df.iloc[:, 0], y=df.iloc[:, 1], palette="magma")
            plt.xlabel(df.columns[0])
            plt.ylabel(df.columns[1])
            plt.title(selected_query)
            plt.xticks(rotation=45)
            st.pyplot(plt)

    
elif page == "🎉Thank You":
# Add a "Thank You" message with emojis and style
# Display a Thank You message with styling
    st.markdown("""
    <h1 style='text-align: center; color: #FF6347;'>🎉 Thank You! 🎉</h1>
    <p style='text-align: center; font-size: 20px;'>We appreciate your time and effort! 😊</p>
    <h2 style='text-align: center; color: #4CAF50;'>Your support means a lot to us!</h2>
    <p style='text-align: center; font-size: 18px;'>We hope you found the insights useful. Stay tuned for more updates! 🚀</p>
    <br>
""", unsafe_allow_html=True)

# Trigger Streamlit effects
    st.balloons()  # Balloons effect

# Optionally, add a confetti effect using time delay
    time.sleep(2)
    st.snow()  # Snow/confetti effect

# Animated progress bar for a smooth transition
    with st.spinner('Finalizing...'):
        time.sleep(2)
    st.success("🎯 Done! Thank you for using the dashboard. Have a great day! 😊")

# Display an exit message or navigation button
    if st.button("Go Back to Home 🏠"):
       st.write("Redirecting to the main page...")

