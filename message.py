from computer import Computer


class Message():
    """The Message class."""

    def __init__(self, src, dst, messageType):
        """Initialises the Message class."""
        if isinstance(src, Computer):
            self.src = src
        if isinstance(dst, Computer):
            self.dst = dst
        if isinstance(messageType, str):
            self.messageType = messageType.upper()   # Cleans the string

    def setSource(self, source):
        """Sets the source of the message."""
        if isinstance(source, Computer):
            self.src = source

    def getSource(self):
        """Gets the source of the message."""
        return self.src

    def setDestination(self, destination):
        """Sets the destination of the message."""
        if isinstance(destination, Computer):
            self.destination = destination

    def getDestination(self):
        """Gets the destination of the message."""
        return self.dst

    def setMessageType(self, messageType):
        """Sets the type of the message: {PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED, REJECTED}."""
        self.messageType = messageType.upper()

    def getMessageType(self):
        """Gets the type of the message: {PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED, REJECTED}."""
        return self.messageType


if __name__ == "__main__":
    m1 = Message(src="A1", dst="A2", messageType="Propose")
    m2 = Message(src="P1", dst="P3", messageType="PromISE")
    print(m1.getMessageType(), m2.getMessageType())
