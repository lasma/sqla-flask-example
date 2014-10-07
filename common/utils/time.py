""" Utility functions for working with date and time"""

import re
import time
import calendar
import datetime

DATETIME_PATTERN = "%Y-%m-%dT%H:%M:%S"
DATETIME_PATTERN_FORMAT = "YYYY-MM-DDTHH24:mm:ss.fffZ"
DATETIME_PATTERN_RE = re.compile(r'(\d+-\d+-\d+T\d+:\d+:\d+)\.?(\d+)?Z?', re.I)


class InvalidDateFormat(Exception):
    """
    Exception for catching incorrectly formatted datetime strings.
    """

    def __init__(self, value, error=None, message=None):
        """
        @param value - date value triggering this exception
        @param error - original exception message from the system invoked during datetime parsing.
        @param message - pretty message of the date time error for the user.
        """
        self.value = value
        self.error = error
        if not message:
            self.message = "Time string '{}' does not follow required time pattern {}".format(value, DATETIME_PATTERN)
        else:
            self.message = message


def current_utc():
    """
    Return the current UTC.
    """
    return datetime.datetime.utcnow()


def time_to_string(dt):
    """
    Format datetime instance to string.

    @param dt: datetime instance
    @return: datetime in string format YYYY-MM-DDTHH24:mm:ss.fffZ
    """

    try:
        msecs = int(round(dt.microsecond / 1000))
        datetime_string = dt.strftime(DATETIME_PATTERN) + '.{:0>3d}Z'.format(msecs)
    except ValueError as e:
        # DEBUG HACK!! just a temp fix for bad year just to get it working
        year = dt.year
        if year < 1900: year = 2014
        datetime_string = '{}-{}-{}T{}:{}:{}.{:0>3d}Z '.format(year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond / 1000)

        message = 'Invalid datetime value: '
        message += '{}-{}-{}T{}:{}:{}.{:0>3d}Z '.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond / 1000)
        message += 'Required datetime format {} where YYYY is >= 1900.'.format(DATETIME_PATTERN_FORMAT)
        print message
    except Exception as e:
        datetime_string = ''
        # TODO should we throw an error?
    return datetime_string


class UTC(datetime.tzinfo):
    """UTC tzinfo"""

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)


def string_to_time(dt_string):
    """
    Convert string to datetime object

    @param dt_string: datetime as string
    @return: datetime instance from string
    """

    def fraction(fstring):
        places = 10 ** len(fstring)
        return float(fstring) / places

    try:
        datetime_string = dt_string
        found = re.search(DATETIME_PATTERN_RE, datetime_string)
        datetime_string, msecs_string = found.groups(0)
        time_struct = time.strptime(datetime_string, DATETIME_PATTERN)
        msecs = fraction(msecs_string)
        timestamp = round(calendar.timegm(time_struct) + msecs, 5)  # smallest increment is 1/48 ms
        # return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC())    # removed because of naive time and utc time collision
        return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=None)

    except Exception as e:
        message = "Time string '{}' does not follow required time pattern {}.".format(dt_string, DATETIME_PATTERN_FORMAT)
        raise InvalidDateFormat(value=dt_string, error=e, message=message)


def convert_to_time(dt):
    """
    If not None, convert dt to a datetime instance.

    @param dt: a string, datetime instance, struct_time instance, or None.
    """

    date_time = None

    if isinstance(dt, basestring) and dt:
        date_time = string_to_time(dt)

    elif isinstance(dt, datetime.datetime):
        date_time = dt

    elif isinstance(dt, time.struct_time):
        # date_time = datetime.datetime(dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec, 0, UTC()) # removed because of naive time and utc time collision
        date_time = datetime.datetime(dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec, 0, None)

    elif dt is not None:
        message = u"Value error: {} is of type {} but requires datetime, time_struct or string formatted as 2014-03-04T23:59:59.000Z".format(
            str(dt), type(dt))
        raise InvalidDateFormat(value=dt, message=message)

    # datetime.datetime.strftime(DATETIME_PATTERN) requires year to be >1900 otherwise error is thrown
    if date_time.year < 1900:
        dt_params = {"Y":date_time.year, "m":date_time.month, "d":date_time.day, "H":date_time.hour, "M":date_time.minute,
                     "S":date_time.second, "ms":date_time.microsecond / 1000, "pattern":DATETIME_PATTERN_FORMAT}
        message = u"Invalid datetime value: {Y}-{m}-{d}T{H}:{M}:{S}.{ms}Z. YEAR must be >= 1900 and datetime should be formatted as string following pattern {pattern}".format(
            **dt_params)
        raise InvalidDateFormat(value=dt, message=message)

    return date_time
