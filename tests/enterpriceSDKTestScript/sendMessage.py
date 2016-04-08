# import libraries
import exp_sdk
import time
import datetime

exp_uuid = '110c7cba-f12c-43cf-ab62-e525b8de7f68'
exp_api_key = '682e0a9d341b783c6856c4bf8f4f741c08f6251b641aaeec165e052efba7fbd164f0027f5ca3e310b38c247021919d64'
exp_host = 'http://192.168.168.38:9000'
now = datetime.datetime.now()

# authentication
exp = exp_sdk.start(uuid=exp_uuid, api_key=exp_api_key, host=exp_host)

# Wait for a connection.
while not exp.is_connected:
    time.sleep(1)

# setup channel
channel = exp.get_channel('scala-test-channel', consumer=True)
responses = channel.broadcast('my-message', 'this message is send @' + now.isoformat())

# print response
for response in responses:
    print responses

exp.stop()
