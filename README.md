# Expense-tracker
A simple app which stores the daily expense of an user and displays the data on a dashboard.

# Description
The app is built with the help of Flask and Plotly Dash library.<br>
It uses MongoEngine, a Document Object Mapper to connect the app with the NoSQL database MongoDB for storing and retrieving the data.<br>
Tha app allows for creating and storing the data in the database as well as displaying the data with option of filtered the data by Date, Expense or Comment.<br>
The app also consists of a dashboard created using Plotly Dash where the user can view the data as well as the forecast of the data for the next 7 days graphically.<br>

**Adding Expense:** <br>   
 ![add_trimmed_gif](https://user-images.githubusercontent.com/63745797/137253217-b1bea64b-f697-4111-876d-22b850b97323.gif)<br>

**Filtering Expense:**<br>
 ![filter_trimmed_gif](https://user-images.githubusercontent.com/63745797/137253272-f55c3710-f826-4a02-a550-ddeeb0ddf2fc.gif)<br>

**Dashboard:**<br>
 ![Untitled_new (4)](https://user-images.githubusercontent.com/63745797/136266806-d68f3eed-6f4e-47eb-b15d-8082936cabe0.gif)

# Files Description
`app.py` contains the basic code for setting up the web pages using Flask as well as the connection with the MongoDB database using MongoEngine.<br>

`dashboard.py` contains the code for dashboard used for fetching and displaying the query required by the user.
1. The dashboard displays the time series data in a table along with a line chart showing the data as well as the forecast for the next 7 days.
2. The method used for forecasting the data in Holt Winters Seasonal Exponential Smoothing<br>

`data_ops.py` contains the code for:
1. Adding the data
2. Fetching and displaying the data filtered by Date
3. Fetching and displaying the data filtered by Expense
4. Fetching and displaying the data filtered by Comment

`wsdgi.py` and `run.py` contains the code for running the Dash app along with the Flask app<br>
