# -*- coding: utf-8 -*-


""" OK """

# Standard response for successful HTTP requests. The actual response will depend on the request method used.
# In a GET request, the response will contain an entity corresponding to the requested resource.
# In a POST request the response will contain an entity describing or containing the result of the action.
HTTP_OK_CODE = 200
HTTP_OK_MSG = "OK"

# The request has been fulfilled and resulted in a new resource being created
HTTP_CREATED_CODE = 201
HTTP_CREATED_MSG = "CREATED"

# The server successfully processed the request, but is not returning any content.
# Usually used as a response to a successful delete request.
# Also returned for requests containing the If-Modified-Since header if the document is up-to-date.
HTTP_NO_CONTENT_CODE = 204
HTTP_NO_CONTENT_MSG = "NO CONTENT"

""" BAD """

HTTP_BAD_REQUEST_CODE = 400
HTTP_BAD_REQUEST_MSG = "BAD REQUEST"

HTTP_NOT_FOUND_CODE = 404
HTTP_NOT_FOUND_MSG = "NOT FOUND"

HTTP_NOT_ALLOWED_CODE = 405
HTTP_NOT_ALLOWED_MSG = "METHOD NOT ALLOWED"

#The server timed out waiting for the request
HTTP_REQUEST_TIMEOUT_CODE = 408
HTTP_REQUEST_TIMEOUT_MSG = "REQUEST TIMEOUT"

# Indicates that the request could not be processed because of conflict in the request,
# such as an edit conflict in the case of multiple updates.
HTTP_CONFLICT_CODE = 409
HTTP_CONFLICT_MSG = "CONFLICT"

""" ERROR """

# A generic error message, given when an unexpected condition was encountered and no more specific message is suitable.
HTTP_INTERNAL_ERROR_CODE = 500
HTTP_INTERNAL_ERROR_MSG = "INTERNAL SERVER ERROR"

# The server either does not recognize the request method, or it lacks the ability to fulfill the request.
# Usually this implies future availability (e.g., a new feature of a web-service API).
HTTP_NOT_IMPLEMENTED_CODE = 501
HTTP_NOT_IMPLEMENTED_MSG = "NOT IMPLEMENTED"

""" CUSTOM CODES >1000 """

# Request was executed OK but result might be unexpected to the requester due to silent warnings
HTTP_OK_WITH_WARNING_CODE = 1200
HTTP_OK_WITH_WARNING_MSG = "OK WITH WARNING"

HTTP_CREATED_WITH_WARNING_CODE = 1201
HTTP_CREATED_WITH_WARNING_MSG = "CREATED WITH WARNING"

# Request encountered an internal error relating to the integration between an external system.
HTTP_SERVER_INTEGRATION_ERROR = 1500
HTTP_SERVER_INTEGRATION_ERROR_MSG = "INTERNAL SERVER INTEGRATION ERROR"