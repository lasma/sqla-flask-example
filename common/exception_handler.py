# -*- coding: utf-8 -*-
from flask import request

from config import app_logging

from common.dao.filtering import UnknownFilterError
from common.properties import PROPS_JSON
from common.rest.exceptions import RestError, UnknownUrlParameterError
from common.service.exceptions import ServiceError, ServiceTimeoutError
from common.dao.exceptions import ItemNotFoundDaoError, DaoError
import common.rest.http_responses as http_responses
from integration.exceptions import IntegrationError

logger = app_logging.get_app_logger(__name__)

def log_500_error():
    """Log Flask request when server error encountered"""
    #r = request
    logger.error("INTERNAL SERVER ERROR while processing request: {} {}\n"
                 "request content: {}".format(request.method, request.url, request.data))


class ExceptionHandler(object):
    """We are taking Alex's exception handler as example and rewriting it to return error wrapped in meta block"""

    def __init__(self, f):
        self.f = f

    def __call__(self, **kwargs):
        try:
            return self.f(self, **kwargs)

        # TODO: must be rewritten!
        # # Client attempted to update an entity that doesn't exist
        # except RecordNotFoundException as e:
        #     logger.exception(e)
        #     return ErrorResponseBuilder.build_404_resource_not_found_response(e.message)
        #
        # # Client attempted to create an entity that already exist
        # except DuplicateRecordException as e:
        #     logger.exception(e)
        #     return ErrorResponseBuilder.build_409_conflict_response(e.message)
        #
        # # One or more objects in the request or response couldn't be serialized
        # except NotSerializableException as e:
        #     stackTrace = traceback.format_exc()
        #     logger.exception(e)
        #     return ErrorResponseBuilder.build_500_internal_server_error_response(e.message, stackTrace)
        #
        # # Request validation failed
        # except RequestValidationException as e:
        #     logger.exception(e)
        #     return ErrorResponseBuilder.build_400_bad_request_response(e.message)
        #
        # # Invalid JSON in the request
        # except InvalidFormatRequestException as e:
        #     logger.exception(e)
        #     return ErrorResponseBuilder.build_400_bad_request_response(e.message)
        #
        # # Database constraint violations
        # except exc.IntegrityError as e:
        #     logger.exception(e)
        #     return ErrorResponseBuilder.build_400_bad_request_response(e.message)
        #
        # # Data type of field doesn't match with db table field type
        # except exc.DataError as e:
        #     logger.exception(e)
        #     return ErrorResponseBuilder.build_400_bad_request_response(e.message)

        except UnknownFilterError as e:
            response, http_code = http_responses.bad_request(e.message, url=request.url)
            response[PROPS_JSON.PAYLOAD] = e.get_filter_list()
            return response, http_code

        except UnknownUrlParameterError as e:
            response, http_code = http_responses.bad_request(e.message, url=request.url)
            response[PROPS_JSON.PAYLOAD] = e.get_known_parameters()
            return response, http_code

        # Item requested/referenced by ID but was not found
        except ItemNotFoundDaoError as e:
            return http_responses.not_found(description=e.message, url=request.url)

        except ServiceTimeoutError as e:
            return http_responses.request_timeout(description=e.message)

        except (RestError, ServiceError, DaoError) as e:
            return http_responses.bad_request(description=e.message, url=request.url, exception=e)

        except IntegrationError as e:
            return http_responses.internal_server_integration_error(description=e.message, url = request.url, exception=e)

        # incorrect use of values (types) etc.
        except ValueError as e:
            log_500_error()
            return http_responses.internal_error(description=e.message, url=request.url, exception=e)

        # Anything else that might go wrong     will be caught here
        except Exception as e:
            log_500_error()
            return http_responses.internal_error(description=e.message, url=request.url, exception=e)

