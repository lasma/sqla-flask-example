class InternalError(Exception):
    """Internal error class. Use this to flag unknown internal errors that
    should trigger HTTP status 500."""
    def __init__(self, message, inner_error=None):
        """
        :param inner_error {Exception}: parent exception triggering this exception
        """
        self.message = message
        self.inner_error = inner_error

