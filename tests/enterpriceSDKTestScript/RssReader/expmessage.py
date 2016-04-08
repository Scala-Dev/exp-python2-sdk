import exp_sdk
import scala5
import scalalib
from scalalib import sharedvars

scalaVars = sharedvars()
scala5.ScalaPlayer.Log('Starting EXP message listen')

try:
    # authentication
    exp = exp_sdk.start(uuid=scalaVars.uuid, api_key=scalaVars.api_key, host=scalaVars.host)

    # Wait for a connection.
    while not exp.is_connected:
        scalalib.sleep(1000)

    # setup channel
    channel = exp.get_channel('scala-test-channel', consumer=True)
    listener = channel.listen('my-message', max_age=30)

    # listen to message
    while True:
        broadcast = listener.wait()
        if broadcast:
            scala5.ScalaPlayer.Log('Message received')
            scalaVars.EXPmessage = broadcast.payload
            scala5.ScalaPlayer.Log('Received message: ' + broadcast.payload)
            broadcast.respond('Message received thank you!')
        scalalib.sleep(1000)

    exp.stop()
except exp_sdk.ExpError or exp_sdk.UnexpectedError:
    scala5.ScalaPlayer.LogExternalError(1000, 'ExpError', 'Error opening channel to EXP')
except exp_sdk.RuntimeError:
    scala5.ScalaPlayer.LogExternalError(1000, 'RuntimeError', 'Please check start options of EXP SDK')
except exp_sdk.AuthenticationError:
    scala5.ScalaPlayer.LogExternalError(1000, 'AuthenticationError',
                                        'Unable to connect to EXP, please check credentials')
except exp_sdk.ApiError:
    scala5.ScalaPlayer.LogExternalError(1000, 'ApiError', exp_sdk.ApiError.message)
