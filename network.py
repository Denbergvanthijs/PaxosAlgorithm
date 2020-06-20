from typing import Union

from message import Message


class Network():
    """The Network class."""

    def __init__(self):
        """Initialises the network."""
        self.messages = []  # The message queue
        self.proposers = []  # List of all proposers
        self.acceptors = []  # List of all acceptors

    def queueMessage(self, message: Message) -> None:
        """Adds a message to the queue."""
        self.messages.append(message)

    def extractMessage(self) -> Union[None, Message]:
        """Returns the first available message.

        A message is only available if both its source and destination are not failing.
        """
        for index, message in enumerate(self.messages):
            if not message.src.failed and not message.dst.failed:
                return self.messages.pop(index)

        return None  # Returns None when no message is available

    def numberOfMessages(self) -> int:
        """Gets the number of messages of the network."""
        return len(self.messages)
