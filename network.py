class Network():
    """The Network class."""

    def __init__(self):
        """Initialises the network."""
        self.messages = []  # The queue of messages

    def setProposers(self, proposers):
        """Sets list with all the proposers."""
        self.proposers = proposers

    def setAcceptors(self, acceptors):
        """Sets list with all the acceptors"""
        self.acceptors = acceptors

    def getProposer(self, ID):
        """Sets list with all the proposers."""
        return self.proposers[ID - 1]

    def queueMessage(self, message):
        """Adds a message to the queue."""
        # if not isinstance(message, Message):
        #     raise TypeError("The message must be of type Message")
        self.messages.append(message)

    def extractMessage(self):
        """
        Returns the first available message.
        A message is only available if both its source and destination are not failing.
        """
        for index, message in enumerate(self.messages):
            if (not message.src.getFailing()) and (not message.dst.getFailing()):
                return self.messages.pop(index)

        return None  # Returns None when no message is available

    def numberOfMessages(self):
        """Gets the number of messages of the network."""
        # print(self.messages)
        return len(self.messages)
