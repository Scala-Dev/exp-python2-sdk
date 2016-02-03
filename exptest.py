import exp
import time
print
print "Starting EXP runtime..."
exp.runtime.start(
    username="email@email.com",
    password="Password12321",
    host="https://api-develop.exp.scala.com",
    port=443,
    organization="scala")



def test (message):
    print 'HERE'
    print message


try:
  experiences = exp.api.find_experiences()
except Exception as error:
  print error
print experiences
while True:
  time.sleep(1)



"""exp.channels.organization.listen(name="hello", callback=test)
print "Started!"
print "Sending!"
time.sleep(1)
exp.channels.organization.broadcast(name="hello")
print "Stopping EXP runtime..."

exp.channels.organization.broadcast(name="hello")"""




exp.runtime.stop()
print "Stopped!"
