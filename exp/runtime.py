
import time
import json
import hmac
import base64
import hashlib
import requests
import threading

from .network import network
from .authenticator import authenticator
from .exceptions import RuntimeError, OptionsError

class _Runtime (object):

  def __init__ (self):
    self._is_started = False

  def start (self, enable_events=True, host='https://api.goexp.io', **options):

    options['host'] = host
    options['enable_events'] = enable_events

    if options.get('type') is 'user' or ((options.get('username') or options.get('password') or options.get('organization')) and not options.get('type')):
      options['type'] = 'user'
      if not options.get('username'):
        raise OptionsError('Please specify the username.')
      if not options.get('password'):
        raise OptionsError('Please specify the password.')
      if not options.get('organization'):
        raise OptionsError('Please specify the organization.')
    elif options.get('type') is 'device' or ((options.get('secret') or options.get('allow_pairing')) and not options.get('type')):
      options['type'] = 'device'
      if not options.get('uuid') and not options.get('allow_pairing'):
        raise OptionsError('Please specify the device uuid.')
      if not options.get('secret') and not options.get('allow_pairing'):
        raise OptionsError('Please specify the device secret.')
    elif options.get('type') is 'consumer_app' or (options.get('api_key') and not options.get('type')):
      options['type'] = 'consumer_app'
      if not options.get('uuid'):
        raise OptionsError('Please specify the consumer app uuid.')
      if not options.get('api_key'):
        raise OptionsError('Please specify the consumer app api key.')
    else:
      raise OptionsError('Please specify authentication type.')

    if self._is_started:
      raise RuntimeError('Runtime already started.')
    self._is_started = True

    authenticator_thread = threading.Thread(target=lambda: authenticator.start(**options))
    authenticator_thread.daemon = True
    authenticator_thread.start()
    authenticator.wait()

    if enable_events:
      network_thread = threading.Thread(target=lambda: network.start(**options))
      network_thread.daemon = True
      network_thread.start()
      network.wait()


runtime = _Runtime()
