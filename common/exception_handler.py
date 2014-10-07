# -*- coding: utf-8 -*-

class ExceptionHandler(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, **kwargs):
        try:
            return self.f(self, **kwargs)

        # Anything else that might go wrong     will be caught here
        except Exception as e:
            return "server error", 500

