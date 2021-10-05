from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app_mengine import server as flask_app
from dashboard import app as app1

application = DispatcherMiddleware(flask_app, {
    '/app1': app_1.server
}) 