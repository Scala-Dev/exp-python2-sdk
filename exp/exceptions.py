
from .logger import logger

class ExpError (Exception):
  def __init__(self, message):
    logger.error('')



class AuthenticationError (ExpError):
  pass

class UnexpectedError (ExpError):

  def __init__ (self, *arg, **kwargs):
    logger.debug('An unexpected error occured:')
    logger.debug(traceback.format_exc())
    super(UnexpectedError, self).__init__(*args, **kwargs)

class NotAuthenticatedError (ExpError):
	pass

# Options to exp.start were invalid or incomplete.
class OptionsError(ExpError):
  pass

# Cannot execute desired action.
class RuntimeError(ExpError):
  pass
