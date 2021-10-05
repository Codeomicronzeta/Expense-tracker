from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from dashboard import app as app1
from app_mengine import server as flask_app


application = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application) 