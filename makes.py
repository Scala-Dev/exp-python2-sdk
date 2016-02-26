import exp

exp.runtime.start(username="email@email.com", password="Password12321", organization="scala", host="https://api-develop.exp.scala.com", port=443)
"""
# experiences = scala.api.get_experiences()
# experience = experiences[1];
# document = experience.document
# dayplan = document["dayPlans"][0]
# dayplan["blocks"] = [];
# for i in range(86400 / 60):
#     dayplan["blocks"].append({
#         "appKey": "default",
#         "startTime": i * 60 * 1000,
#         "endTime": i * 60 * 1000 + 10 * 1000
#     })
#     dayplan["blocks"].append({
#         "appKey": "default",
#         "startTime": i * 60 * 1000 + 20 * 1000,
#         "endTime": i * 60 * 1000 + 30 * 1000
#     })
# print dayplan["blocks"][34]    
# experience.save()


experiences = exp.api.find_experiences()
print experiences

exp.api.create_data(key="fluffy", group="cats", value={ "awesome": 3})

data = exp.api.get_data('fluffy', 'cats')
data.value = { "test": "cat" }
data.save()

contents = exp.api.get_content('root')
children =  contents.get_children()
for child in children:
    try:
        print child.get_url()
    except Exception as e:
        print e

exp.runtime.stop()

"""
import time

def cb(tmp):
    print "I got a message!!!!!!"
    print "I _________________________________________"

print "Started!"
print "Sending!"
exp.channels.organization.listen(name="hello", callback=cb)
time.sleep(2)
exp.channels.organization.broadcast(name="hello")
print "hi"
time.sleep(3)
print "Stopping EXP runtime..."
exp.runtime.stop()
print "Stopped!"

