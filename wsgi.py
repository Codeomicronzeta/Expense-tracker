from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app import server as flask_app
from dashboard import app as app1
from data_ops import app as app2

application = DispatcherMiddleware(flask_app, {
    '/app1': app_1.server
    '/app2': app_2.server
}) 
