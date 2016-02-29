import exp

import time

if __name__ == '__main__':
  exp.start(
  	username='email@email.com', password='Password12321', 
  	organization='scala', host='http://localhost:9000')
  exp.get_channel('hi!').listen('hello')
  print 'HELLO!'
  time.sleep(5)
  exp.stop()