from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from dashboard import app as app1
from app import server as flask_app
from data_ops import app as app2

application = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
    '/app2': app2.server
})

if __name__ == '__main__':
    run_simple('localhost', "user_port_no", application) 
