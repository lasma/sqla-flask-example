# -*- coding: utf-8 -*-

class ExceptionHandler(object):
    """Use this class to catch any sort of flask api call exception and return server error rather
    than crash the flask server and display stack trace
    """

    def __init__(self, f):
        self.f = f

    def __call__(self, **kwargs):
        try:
            return self.f(self, **kwargs)

        except Exception as e:
            return "server error", 500

