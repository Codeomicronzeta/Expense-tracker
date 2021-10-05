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


app = dash.Dash(__name__, requests_pathname_prefix='/app1/')

# Creating a function for creating a dynamic user defined dataframe

app.layout = html.Div([
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

# Callback for graph
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

    #fig = px.line(data, x=data['Date'][(data['Date'] >= start_date) & (data['Date'] <= end_date)],
     #y = data['Expense'][(data['Date'] >= start_date) & (data['Date'] <= end_date)])
    fig = px.line(df, x = 'Date', y = 'Expense')
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)
