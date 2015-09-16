import time
import threading
from lib import socket


credentials = {}

def init(host='', uuid='', secret=None):
    # Save credentials
    # Generate credentials
    # Start socket connection
    credentials['uuid'] = uuid
    credentials['secret'] = secret
    credentials['host'] = host



def mainEventLoop():
  #socket.setSomething('HI bob!')
  print 'A'
  time.sleep(4)
  mainEventLoop()



socket.start()  
  
mainEventLoop()






    

    


    


    



    
