# Expense-tracker
A simple app which stores the expense of an user and displays the data on a dashboard.

# Description
The app is built with the help of Flask and Plotly Dash library.<br>
It uses MongoEngine, a Document Object Mapper to connect the app with the NoSQL database MongoDB for storing and retrieving the data.<br>
The app also consists of a dashboard created using Plotly Dash where the user can view the data as well as the forecast of the data for the next 7 days graphically.<br>

# Files Description
`app.py` contains the basic code for setting up the web pages using Flask as well as the connection with the MongoDB database using MongoEngine.<br>

`dashboard.py` contains the code for dashboard used for fetching and displaying the query required by the user.
1. The dashboard displays the time series data in a table along with a line chart showing the data as well as the forecast for the next 7 days.
2. The method used for forecasting the data in Holt Winters Seasonal Eponential Smoothing<br>

`wsdgi.py` and `run.py` contains the code for running the Dash app along with the Flask app<br>
