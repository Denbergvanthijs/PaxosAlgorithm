from computer import Computer


class Message():
    """The Message class."""

    def __init__(self, src, dst, messageType, value):
        """Initialises the Message class."""
        if not isinstance(src, (Computer, type(None))):
            raise TypeError("The src must be of type Computer or None if from external agent.")
        if not isinstance(dst, Computer):
            raise TypeError("The dst must be of type Computer.")
        if not isinstance(value, int):
            raise TypeError("The value must be of type integer.")

        self.src = src
        self.dst = dst
        self.messageType = Message.checkMessageType(messageType)
        self.value = value

    def setSource(self, source):
        """Sets the source of the message."""
        if not isinstance(source, (Computer, type(None))):
            raise TypeError("Src must be of type Computer or None if from external agent.")
        self.src = source

    def getSource(self):
        """Gets the source of the message."""
        return self.src

    def setDestination(self, destination):
        """Sets the destination of the message."""
        if not isinstance(destination, Computer):
            raise TypeError("Dst must be of type Computer.")
        self.destination = destination

    def getDestination(self):
        """Gets the destination of the message."""
        return self.dst

    def setMessageType(self, messageType):
        """Sets the type of the message: {PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED, REJECTED}."""
        self.messageType = Message.checkMessageType(messageType)

    def getMessageType(self):
        """Gets the type of the message: {PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED, REJECTED}."""
        return self.messageType

    @staticmethod
    def checkMessageType(messageType):
        """Checks the given messageType. Raises or returns a valid string.

        Only accepts the following strings:
        {PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED, REJECTED}
        """
        if not isinstance(messageType, str):
            raise TypeError("MessageType must be string.")

        if messageType.upper() in ("PROPOSE", "PREPARE", "PROMISE", "ACCEPT", "ACCEPTED", "REJECTED"):
            return messageType.upper()  # Cleans the string
        else:
            raise ValueError("Not a valid messageType.")
