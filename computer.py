from message import Message


class Computer:
    """The Computer class."""

    def __init__(self, cType):
        """Initialises the Computer class."""
        if cType.upper() in ("ACCEPTOR", "PROPOSER"):
            self.cType = cType.upper()  # Cleans the string
        self.failed = False

    def setComputerType(self, cType):
        """Sets the type of this computer: {Proposer, Acceptor}."""
        self.cType = cType

    def getComputerType(self):
        """Gets the type of this computer: {Proposer, Acceptor}."""
        return self.cType

    def setFailing(self, status):
        """Sets the failed status of the computer."""
        if isinstance(status, bool):
            self.failed = status

    def getFailing(self):
        """Get the failed status of this computer: {True, False}."""
        return self.failed

    def deliverMessage(self, destinationComputer, message, network):
        """Delivers a message to a computer, via the Network-queue."""
        m = Message(src=self, dst=destinationComputer, messageType=message.messageType)
        network.queueMessage(m)


if __name__ == "__main__":
    c1 = Computer(cType="ACCEPTOR")
    c2 = Computer(cType="ProPOser")

    print(c1.getType(), c2.getType())

    c1.setFailing(True)
    print(c1.getFailing(), c2.getFailing())
