# Zomato
🚀 Zomato Delivery Insights Dashboard 📊🍽️  An interactive analytics dashboard built with Python, SQL, and Streamlit, providing deep insights into customer orders, restaurant performance, delivery trends, and more!  ✨ Key Features: ✅ SQL-powered analytics for data-driven decisions ✅ Peak order times, revenue insights &amp; delivery efficiency
##Zomato Delivery Insight
Project Overview
The Zomato Delivery Insight project is a data analytics and visualization application aimed at providing insightful data analysis on delivery operations. The project utilizes Python for data generation, SQL for querying, and Streamlit for interactive data visualization. The main goal is to explore delivery patterns, customer preferences, restaurant performance, and delivery times.

**Features**
Database Design: Utilizes normalized SQL tables for storing and analyzing restaurant and delivery data.
Dynamic Querying: Predefined queries that allow for analysis of customer orders, delivery times, and revenue insights.
Streamlit Dashboard: Interactive dashboard to visualize key insights like total revenue, popular restaurants, delivery efficiency, and more.
Synthetic Data Generation: Python's Faker library is used to generate synthetic customer, order, and delivery data for testing and analysis.
Technologies Used
Python: Used for data manipulation and generation (Faker, Pandas).
SQL: MySQL for querying data from the database.
Streamlit: Used to create the interactive web interface for visualizing the data.
Matplotlib / Seaborn: Used for data visualization.
TiDB Cloud: Cloud-based MySQL-compatible database to run queries.
**Project Structure**
                              Zomato-Delivery-Insight/
                              │
                              ├── main.py               # Main Streamlit app file for the dashboard
                              ├── Zomato.py             # Python file to handle SQL connections and queries
                              ├── requirements.txt      # List of required Python libraries
                              ├── README.md             # This README file
                              └── LICENSE               # Project license file
**Installation**
Step 1: Clone the Repository
Start by cloning this repository to your local machine.


                              git clone https:/hana3232/github.com//Zomato.git
                              cd Zomato-Delivery-Insight
Step 2: Install Dependencies
Create a virtual environment and install the required dependencies using requirements.txt.


                              python -m venv venv
                              source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
                              pip install -r requirements.txt
Step 3: Set Up Database
Ensure you have access to TiDB Cloud or a local MySQL database to execute the SQL queries. If you're using a local MySQL setup, modify the database.py to point to your database credentials.

Step 4: Run the App
To start the interactive dashboard, run the Streamlit app.


                            streamlit run main.py
Visit http://localhost:8501 in your browser to access the dashboard.



**Queries and Insights**
**Here are some of the predefined queries you can select in the dashboard for analysis:**


Total Revenue Per Restaurant: Displays the total revenue generated by each restaurant.
Average Order Value: Shows the average order amount across all customers.
Most Popular Restaurant: Lists the top 10 most popular restaurants based on the number of orders.
Most Ordered Cuisine: Displays the most ordered cuisines from the restaurant.
Peak Order Time: Identifies the busiest times for orders.
Highest Rated Restaurant: Displays the highest-rated restaurants based on customer reviews.
Orders Per Customer: Shows the total number of orders placed by each customer.
Total Revenue Per Customer: Displays the total revenue generated by each customer.
Delivery Efficiency: Shows insights on the fastest and slowest deliveries.
