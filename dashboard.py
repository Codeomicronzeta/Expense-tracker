import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import date
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from app_mengine import Expense
import dash_table
import statsmodels as sm
from statsmodels.tsa.api import ExponentialSmoothing
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, requests_pathname_prefix='/app1/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Creating a Navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="Link to Home page"),active = True),
        dbc.NavItem(dbc.NavLink("Data", href="Link to Add Expense page", active = True)),
        dbc.NavItem(dbc.NavLink("Dashboard", href="Link to the Dashboard page"),active = True),
    ],
    brand = "Navbar",
    brand_style = {"padding-left":"0", "margin-left":"-73px"},
    links_left = True,
    color="Black",
    dark=True,
)

# App Layout
app.layout = html.Div([
    navbar,
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2050, 9, 19),
        display_format='Y-M-D',
        start_date=date(2021, 8, 1),
        end_date=date(2021, 8, 25)
    ),
    dash_table.DataTable(
        id='table',
        columns = [{"name": i, "id": i} for i in ['Date', 'Expense']],
        page_current=0,
        page_size=5,
        page_action='custom'
    ),
    dcc.Graph(id = "line-chart"), 
    dcc.Graph(id = "forecast"), 
    dcc.Store(id = 'df')
])

# Callback for fetching user updated query
# Callback for Mutiple Output to different components
@app.callback(
    [Output('df', 'data'),
    Output('table', 'data')],
    [Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
    Input('table', "page_current"),
    Input('table', "page_size")]
)
def createDf(start_date, end_date, page_current, page_size):
    list_data = []
    date = Expense.objects().filter(Q(Date__gte = start_date) & Q(Date__lte = end_date)).scalar("Date", "Expense")
    for dates in date:
        list_data.append(dates)
    df = pd.DataFrame(list_data, columns=['Date', 'Expense'])
    
    # returning two objects for two different components
    return [df.to_json(date_format='iso'), df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')]

# Callback for original graph
@app.callback(
    Output("line-chart", "figure"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
    Input("df", "data")
)
def update_line_chart(start_date, end_date, df):
    df = pd.read_json(df)
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    
    fig = px.line(df, x = 'Date', y = 'Expense')
    return fig

# Callback for plotting the graph with forecast
@app.callback(
    Output("forecast", "figure"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
    Input("df", "data")
)
def update_forecast_chart(start_date, end_date, df):
    train_data = pd.read_json(df)
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)

    train_data.index = train_data.Date
    train_data.drop(['Date'], axis = 1, inplace = True)
    #print(train_data.head())

    fit = ExponentialSmoothing(train_data,
    seasonal_periods = 7,
    trend="add",
    seasonal="mul",
    use_boxcox=True,
    initialization_method="estimated",
    ).fit()

    forecast = pd.DataFrame(fit.forecast(7), columns=['Expense'])
    forecast.index = pd.date_range(start=end_date, periods = 7)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = forecast.index, y = forecast.Expense,mode='lines',name='Forecast', 
    marker = dict(
            color='Red')))
    fig.add_trace(go.Scatter(x = train_data.index, y = train_data.Expense, mode='lines',name='Original', 
    marker = dict(
            color='Blue')))
    
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.99
    ))
    return fig


if __name__ == '__main__':
    app.run_server(debug = True)

