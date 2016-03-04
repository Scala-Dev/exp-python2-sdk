
from .logger import logger
import traceback

class ExpError (Exception):
  pass


class AuthenticationError (ExpError):
  pass

class UnexpectedError (ExpError):

  def __init__ (self, *arg, **kwargs):
    logger.debug('An unexpected error occured:')
    logger.debug(traceback.format_exc())
    super(UnexpectedError, self).__init__(*args, **kwargs)

# Cannot execute desired action.
class RuntimeError(ExpError):
  pass

class ApiError(ExpError):

  def __init__(self, payload):
    logger.debug('An api error has occured.')
    logger.debug(traceback.format_exc())
    self.message = payload.get('message')
    self.code = payload.get('code')

  def __str__(self):
    return '%s: %s' % (self.code, self.message)

