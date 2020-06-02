from message import Message
from computer import Computer


class Network():
    """The Network class."""

    def __init__(self, messages):
        """Initialises the network."""
        self.messages = messages

    def queueMessage(self, message):
        """Adds a message to the queue."""
        if isinstance(message, Message):
            self.message.append(message)

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
        return len(self.messages)


if __name__ == "__main__":
    c1 = Computer(cType="ACCEPTOR")
    c2 = Computer(cType="ProPOser")

    m1 = Message(src=c1, dst=c2, messageType="Propose")
    n = Network(messages=[m1])

    print(n.extractMessage())  # Extracts the first and only message
    print(n.extractMessage())  # No messages left, returns None
