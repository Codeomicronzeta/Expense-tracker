from flask import Flask, render_template, request, flash
from flask_mongoengine import MongoEngine
import datetime
from flask import jsonify
from mongoengine.fields import DateTimeField, ReferenceField, StringField, FloatField
from flask_bootstrap import Bootstrap
from mongoengine.queryset.visitor import Q
import dash

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Initializing the app
server = Flask(__name__)
server.config['SECRET_KEY'] = "The_Secret_Key" 
bootstrap = Bootstrap(server)

# Creating a dictionary for connection parameters for MongoDB
server.config['MONGODB_SETTINGS'] = {
    'db': 'database_name',
    'host': 'host_url'
}

db = MongoEngine(server)


# Creating a class for expense input
class Expense(db.Document):
    Date = db.DateTimeField(default = datetime.datetime.now)
    Expense = db.FloatField(required = False, min_value = 0)
    Comment = db.StringField(required = False)

def display_data(from_date, to_date):
    for obj in Expense.objects:
        print(obj.date(Q(date__gte = from_date) & Q(date__lte = to_date)), obj.daily_expense(Q(date__gte = from_date) & Q(date__lte = to_date)))

@server.route('/')
def index():
    return render_template('index.html')

@server.route('/add_expense', methods = ['GET', 'POST'])
def add_expense():
    if request.method == "POST":
        exp = Expense(
        date = request.form["date"],
        daily_expense = request.form["daily_expense"],
        comment = request.form["comment"]   
        )
        exp.save()

    return render_template('add_expense.html')

if __name__ == '__main__':
    server.run(debug = True)
        

