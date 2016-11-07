
import traceback
import logging

logger = logging.getLogger('exp')


class ExpError (Exception):

  def __init__ (self, message):
    self.message = message

  def __str__ (self):
    return self.message


class AuthenticationError (ExpError):
  pass

class UnexpectedError (ExpError):

  def __init__ (self, *args, **kwargs):
    logger.debug('An unexpected error occured:')
    logger.debug(traceback.format_exc())
    super(UnexpectedError, self).__init__(*args, **kwargs)

# Cannot execute desired action.
class RuntimeError(ExpError):

  def __init__ (self, message):
    logger.debug('A runtime error has occured: %s' % message)

  def __str__ (self):
    return self.message


class ApiError(ExpError):

  def __init__(self, code=None, message=None, status_code=None, payload=None):
    self.message = message or 'An unknown error has occurred.'
    self.code = code or 'unknown.error'
    self.status_code = status_code
    self.payload = payload

  def __str__(self):
    return '%s: %s \n %s' % (self.code, self.message, self.payload)


class NetworkError(ExpError): pass
