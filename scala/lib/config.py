_vars = {}

def set(**kwargs):
  for key, value in kwargs.iteritems():
    _vars[key] = value

def get(name):
  return _vars.get(name, None)
  
    
