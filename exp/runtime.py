
from .logger import logger
from .network import network
from .authenticator import authenticator
from .exceptions import RuntimeError

class Runtime (object):

  def start (self, enable_network=True, host='https://api.goexp.io', **options):

    options['host'] = host
    options['enable_network'] = enable_network

    if options.get('type') is 'user' or ((options.get('username') or options.get('password') or options.get('organization')) and not options.get('type')):
      options['type'] = 'user'
      if not options.get('username'):
        raise RuntimeError('Please specify the username.')
      if not options.get('password'):
        raise RuntimeError('Please specify the password.')
      if not options.get('organization'):
        raise RuntimeError('Please specify the organization.')
    elif options.get('type') is 'device' or ((options.get('secret') or options.get('allow_pairing')) and not options.get('type')):
      options['type'] = 'device'
      if not options.get('uuid') and not options.get('allow_pairing'):
        raise RuntimeError('Please specify the device uuid.')
      if not options.get('secret') and not options.get('allow_pairing'):
        raise RuntimeError('Please specify the device secret.')
    elif options.get('type') is 'consumer_app' or (options.get('api_key') and not options.get('type')):
      options['type'] = 'consumer_app'
      if not options.get('uuid'):
        raise RuntimeError('Please specify the consumer app uuid.')
      if not options.get('api_key'):
        raise RuntimeError('Please specify the consumer app api key.')
    else:
      raise RuntimeError('Please specify authentication type.')

    authenticator.configure(**options)  # Configure the authenticator.
    network.configure(**options)  # Configure the network.
    network.start()
    authenticator.get_auth()  # Block until authentication has been received.
    logger.info('EXP SDK started successfully.')


runtime = Runtime()
