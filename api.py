import json
import tornado.web
import nets
import bugsnag
from bugsnag.tornado import BugsnagRequestHandler
import logging
import sys
import tornado.log
import traceback

#redirect logger to stdout
logging.getLogger("tornado.access").addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger("tornado.access").propagate = False

class FriendlyError(Exception):
    """used for handled exceptions"""

class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler to be used instead of RequestHandler
    """
    
    def write_error(self, status_code, **kwargs):
        if status_code in [403, 404, 500, 503]:
            self.write('Error %s' % status_code)
        else:
            self.write('other error')

class ErrorHandler(tornado.web.ErrorHandler, BaseHandler):
    """
    Default handler to be used in case of 404 error
    """
    pass

class ClassesHandler(BugsnagRequestHandler):

    def prepare(self):
        logging.info(str(self.request.headers))
	try:
            if self.request.headers["Content-Type"].startswith("application/json"):
                self.json_args = json.loads(self.request.body)
            else:
                self.json_args = None
        except:
            self.json_args = None

    def post(self):
        logging.error("this is an error")
	# Get a convenient handle on the given base64 string
        req_data = self.json_args.get('data')
        try:
            # pass the base64 enc string to classifier
            classes = nets.classify(image_file=req_data['image_file'])
        except KeyError as e:
            bugsnag.notify(e)
            try:
                classes = nets.classify(url=req_data['image_uri'])
            except KeyError as e:
                bugsnag.notify(e)
        # Send the extracted features back in the response
        try:
            self.write(dict(data=classes))
        except TypeError as e:
            bugsnag.notify(e)
            self.write(str(e))


class UnhandledExceptionHandler(BugsnagRequestHandler):

    def get(self):
        r = 1/0
        self.write(r)


class HandledException(BugsnagRequestHandler):

    def get(self):
        try:
            1+'1'
        except TypeError as e:
            print traceback.format_exc()
            logging.error(e)
            self.write('this is a handled exception ')








