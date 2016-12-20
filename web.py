import tornado.ioloop
import tornado.web
from tornado import httpserver
from api import ClassesHandler, UnhandledExceptionHandler, HandledException, BadDataHandler
from tornado.options import define, options
from tornado.log import enable_pretty_logging
#test of deploy

enable_pretty_logging()
define("port", default=8888)
import os
import bugsnag
from bugsnag.tornado import BugsnagRequestHandler
#change api_key to Markable key

bugsnag.configure(
    api_key="16a92cf41c182a50aee6ca80fae9d65d",
    project_root="/home/markable/py-features-api",
)

class MainHandler(BugsnagRequestHandler):
    """mainhandler"""

    def get(self):
        self.write('Welcome!')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/classes", ClassesHandler),
        (r"/bad_error", UnhandledExceptionHandler),
        (r"/handled", HandledException)
    ])

if __name__ == "__main__":
    options.parse_command_line()
    app = make_app()
    port = options.port
    server = httpserver.HTTPServer(app, xheaders=True)
    server.listen(port)
    print 'Listening on port {}'.format(port)
    tornado.ioloop.IOLoop.current().start()
    bugsnag.notify()

