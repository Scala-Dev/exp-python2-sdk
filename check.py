import exp

import time

if __name__ == '__main__':
  exp.start(
  	username='email@email.com', password='Password12321', 
  	organization='scala', host='http://localhost:9000')
  channel = exp.get_channel('test_channel')
  listener = channel.listen('test_message')
  broadcast = listener.wait(15)
  if broadcast:
    print 'Got Broadcast'
    broadcast.respond('I got your message!')
  print 'Finsihed!'
  exp.stop()