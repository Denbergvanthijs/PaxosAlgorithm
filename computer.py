from message import Message


class Computer:
    """The Computer class."""

    n = 1

    def __init__(self, ID, cType, network):
        """Initialises the Computer class."""
        if not cType.upper() in ("ACCEPTOR", "PROPOSER"):
            raise ValueError("Not a valid cType.")

        self.ID = ID
        self.cType = cType.upper()  # Cleans the string
        self.network = network

        self.failed = False
        self.value = None
        self.prior = 0
        self.promises = 0
        self.accepted = False

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

    def deliverMessage(self, message):
        """Delivers a message to a computer, via the Network-queue."""
        # Extern naar PROPOSER, dit handelt een proposer af
        if message.getMessageType() == "PROPOSE":
            self.value = message.value

            for acceptor in self.network.acceptors:
                # PREPARE message can not contain the value:
                # https://en.wikipedia.org/wiki/Paxos_(computer_science)#Phase_1a:_Prepare
                returnMessage = Message(self, acceptor, "PREPARE", None, Computer.n)
                self.network.queueMessage(returnMessage)

            Computer.n += 1

        # Proposer naar ACCEPTOR, dit handelt een acceptor af
        elif message.getMessageType() == "PREPARE":
            if message.n > self.prior:
                returnMessage = Message(self, message.src, "PROMISE", None, message.n)
                self.network.queueMessage(returnMessage)

        # Acceptor naar PROPOSER, dit handelt een proposer af
        elif message.getMessageType() == "PROMISE":
            self.promises += 1

            # 50% accepted is not enough
            if self.promises > (len(self.network.acceptors) // 2):
                if not self.accepted:
                    for acceptor in self.network.acceptors:
                        returnMessage = Message(self, acceptor, "ACCEPT", self.value, message.n)
                        self.network.queueMessage(returnMessage)

                    self.promises = 0
                    self.accepted = True

        # Proposer naar ACCEPTOR, dit handelt een acceptor af
        elif message.getMessageType() == "ACCEPT":
            if self.prior < message.n:
                self.prior = message.n
                self.value = message.value

                returnMessage = Message(self, message.src, "ACCEPTED", self.value, self.n)
                self.network.queueMessage(returnMessage)

    def getName(self):
        """Gets the name of this computer."""
        return f"{self.cType[0]}{self.ID}"
