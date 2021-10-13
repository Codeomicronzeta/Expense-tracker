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
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, requests_pathname_prefix='/app2/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Date components for date_tab
date_pick = dbc.FormGroup([
    dbc.Label("Date", html_for="date_pick", style={"margin-left":"35%"}),
    dcc.DatePickerSingle(
                    id = "date",
                    date=date(2021, 6, 21),
                    display_format='Y-M-D',
         style={"margin-left":"3%", "margin-top":"10%"}
        )
    ]
)


# Date Component for filter by date in deleting tab
date_pick_3= dbc.FormGroup([
    dbc.Label("Date", html_for="date_pick_3", style={"margin-left":"35%"}),
    dcc.DatePickerRange(
                    id = "date_3",
                    start_date=date(2021, 10, 1),
                    end_date = date(2021, 12, 31),
                    display_format='Y-M-D',
         style={"margin-left":"3%", "margin-top":"10%"}
        )
    ]
)

fill_date_comp = html.Div([
    date_pick_3,
    html.Button("Submit", 
            id="sub-date_del", n_clicks=0, 
            style = {"margin-left":"35%", "width":"30%"},
            formMethod = "POST", type = "submit")
    
])

# Expense Components for add_form
exp = dbc.FormGroup([
    dbc.Label("Expense", html_for="exp", style={"margin-left":"35%"}),
    dbc.Input(id="exp", type="number", step="any", bs_size='md',
         style={"margin-left":"35%", "width":"20%"}
        )
    ]
)

# Expense Components for Delete Tab
exp_3 = dbc.FormGroup([
    dbc.Label("Expense", html_for="exp", style={"margin-left":"35%", "margin-top":"9%"}),
    dbc.Input(id="exp_lo", type="number", step="any", bs_size='md',
         style={"margin-left":"35%", "width":"20%"}, placeholder = "lo"),
    dbc.Input(id="exp_hi", type="number", step="any", bs_size='md',
         style={"margin-left":"35%", "width":"20%"}, placeholder = "hi")
    ]
)

fill_exp_comp = html.Div([
    exp_3,
    html.Button("Submit", 
            id="sub-exp_del", n_clicks=0, 
            style = {"margin-left":"35%", "width":"30%"},
            formMethod = "POST", type = "submit"),
    html.Div(id="fill_exp_dummy", )

])

# Comment Components for add_form
comment = dbc.FormGroup([
    dbc.Label("Comment", html_for="comment", style={"margin-left":"35%"}),
    dbc.Input(id="comment", type="text", bs_size='md',
         style={"margin-left":"35%", "width":"20%"}
        )
    ]
)


# Comment components for Filter by Comment
comment_3 = dbc.FormGroup([
        dbc.Label("Comments", html_for="exp", style={"margin-left":"35%", "margin-top":"9%"}),
        dbc.Input(id="comment_3", type="text", step="any", bs_size='md',
         style={"margin-left":"35%", "width":"20%"}
        )
    ]
)

fill_comm_comp = html.Div([
    comment_3,
    html.Button("Submit", 
            id="sub-comm_del", n_clicks=0, 
            style = {"margin-left":"35%", "width":"30%"},
            formMethod = "POST", type = "submit")

])


# Form
form_add = dbc.Form([date_pick, exp, comment])

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="http://localhost:8050/"),active = True),
        dbc.NavItem(dbc.NavLink("Data", href="http://localhost:8050/app2", active = True)),
        dbc.NavItem(dbc.NavLink("Dashboard", href="http://localhost:8050/app1"),active = True),
    ],
    brand = "Navbar",
    brand_style = {"padding-left":"0", "margin-left":"-73px"},
    links_left = True,
    color="Black",
    dark=True,
)

tab1_content = html.Div([
    form_add,
    html.Button("Submit", 
            id="sub-add", n_clicks=0, 
            style = {"margin-left":"35%", "width":"30%"},
            formMethod = "POST", type = "submit")

])


tab_date_content = html.Div([
    fill_date_comp,
    dash_table.DataTable(
                id='date_data_table',
                columns = [{"name": i, "id": i} for i in ['Date', 'Expense', 'Comment']],
                page_current=0,
                page_size=5,
                page_action='custom')
])

tab_exp_content = html.Div([
    fill_exp_comp,
    dash_table.DataTable(
                id='date_exp_table',
                columns = [{"name": i, "id": i} for i in ['Date', 'Expense', 'Comment']],
                page_current=0,
                page_size=5,
                page_action='custom',
                )
])

tab_comm_content = html.Div([
    fill_comm_comp,
    dash_table.DataTable(
                id='date_comm_table',
                columns = [{"name": i, "id": i} for i in ['Date', 'Expense', 'Comment']],
                page_current=0,
                page_size=5,
                page_action='custom',
                )
])

# Tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Add an Expense", tab_id="add"),
        dbc.Tab(tab_date_content, label="Filter by Date", tab_id="date"),
        dbc.Tab(tab_exp_content, label = "Filter by Expense", tab_id = "val"),
        dbc.Tab(tab_comm_content, label="Filter by Comments", tab_id="comments"),
    ],
    id = "tabs",
    active_tab = "add",
    card = False,
)

# App layout
app.layout = html.Div([
    navbar,
    tabs,
    html.Div(id="hidden_div", style={"display":"none"}),
    html.Div(id = "hidden_div_2", style = {"display":"none"})
])
#------------------------------------------------------

# Callback for adding the data
@app.callback(
    Output("hidden_div", "children"),
    [Input("tabs", "active_tab"),
    Input("sub-add", "n_clicks"),
    State("date", "value"),
    State("exp", "value"),
    State("comment", "value")]
)
def add_expense(at, n, date, exp, comment):
    if(at == "add"):
        print(at)
        if(n != 0):
            exp = Expense(
                Date = date,
                Expense = exp,
                Comment = comment
            )
            exp.save()
            print("Saved!")
            return n

# Callback for displaying data filtered by Date
@app.callback(
    Output("date_data_table", "data"),
    Input("tabs", "active_tab"),
    Input("sub-date_del", "n_clicks"),
    Input("date_3", "start_date"),
    Input("date_3", "end_date"),
    Input("date_data_table", "page_current"),
    Input("date_data_table", "page_size")
)
def display_date(at, click_1, start, end, page_current, page_size):
    if(at == "date"):
        if(click_1 != 0):
            list_date = []
            date_data = Expense.objects().filter(Q(Date__gte = start) & Q(Date__lte = end)).scalar("Date", "Expense", "Comment")
            for data in date_data:
                list_date.append(data)
            df_date = pd.DataFrame(list_date, columns = ['Date', 'Expense', 'Comment'])
            #df_date = df_date.drop(['id'], axis = 1)
            print(df_date)
            return df_date.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

# Callback for displaying data filtered by Expense
@app.callback(
    Output("date_exp_table", "data"),
    Input("tabs", "active_tab"),
    Input("sub-exp_del", "n_clicks"),
    State("exp_lo", "value"),
    State("exp_hi", "value"),
    Input("date_exp_table", "page_current"),
    Input("date_exp_table", "page_size")
)
def display_expense(at, click_1, lo, hi, page_current, page_size):
    if(at == "val"):
        if(click_1 != 0):
            print(lo, hi, click_1)
            list_exp = []
            exp_data = Expense.objects().filter(Q(Expense__gte = float(lo)) & Q(Expense__lte = float(hi))).scalar("Date", "Expense", "Comment")
            print(exp_data)
            for data in exp_data:
                list_exp.append(data)
            df_exp = pd.DataFrame(list_exp, columns = ['Date', 'Expense', 'Comment'])
            #df_date = df_date.drop(['id'], axis = 1)
            print(df_exp)
            return df_exp.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

# Callback for data filtered by Comments
@app.callback(
    Output("date_comm_table", "data"),
    Input("tabs", "active_tab"),
    Input("sub-comm_del", "n_clicks"),
    State("comment_3", "value"),
    Input("date_comm_table", "page_current"),
    Input("date_comm_table", "page_size")
)
def display_comment(at, click_3, value, page_current, page_size):
    if(at == "comments"):
        if(click_3 != 0):
            list_comm = []
            comm_data= Expense.objects().filter(Q(Comment__icontains = str(value))).scalar("Date", "Expense", "Comment")
            print(comm_data)
            for data in comm_data:
                list_comm.append(data)
            df_comm = pd.DataFrame(list_comm, columns = ['Date', 'Expense', 'Comment'])
            #df_comm = df_date.drop(['id'], axis = 1)
            print(df_comm)
            return df_comm.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')


#Expense.objects().filter(Q(Date__gte = start_date) & Q(Date__lte = end_date)).scalar("Date", "Expense")


if __name__ == '__main__':
    app.run_server(debug = True)