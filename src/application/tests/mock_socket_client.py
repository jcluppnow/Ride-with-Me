"""
Socket client that enables user to be defined on scope
"""
from channels.testing import WebsocketCommunicator

class AuthWebsocketCommunicator(WebsocketCommunicator):
    """
    Socket client that enables user to be defined on scope
    """
    def __init__(self, application, path, headers=None, subprotocols=None, user=None): # pylint: disable=too-many-arguments
        super(AuthWebsocketCommunicator, self).__init__(application, path, headers, subprotocols) # pylint: disable=super-with-arguments
        if user is not None:
            self.scope['user'] = user
