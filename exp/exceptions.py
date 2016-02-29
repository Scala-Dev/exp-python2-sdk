

class ExpError (Exception):
  pass


class AuthenticationError (ExpError):
  pass

class UnexpectedError (ExpError):
  pass



# Options to exp.start were invalid or incomplete.
class OptionsError(ExpError):
  pass

# Cannot execute desired action.
class RuntimeError(ExpError):
  pass
