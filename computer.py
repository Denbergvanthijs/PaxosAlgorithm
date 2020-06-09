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

        self.proposed = None  # Initial proposed value from external.
        self.failed = False
        self.value = None  # Current accepted value
        self.prior = 0  # Prior number of transaction

        self.promises = 0  # Number of promises from Acceptors to Proposers
        self.accepted = False  # If the current transaction is accepted

        self.rejects = 0  # Number of rejected from Accepters to Proposers
        self.rejected = False  # If the current transaction is

    def getName(self):
        """Gets the name of the current computer."""
        return f"{self.cType[0]}{self.ID}"

    def deliverMessage(self, message):
        """Delivers a message to a computer, via the Network-queue."""
        # Extern naar PROPOSER, dit handelt een proposer af
        if message.messageType == "PROPOSE":
            self.proposed = message.value

            for acceptor in self.network.acceptors:
                # PREPARE message can not contain the value:
                # https://en.wikipedia.org/wiki/Paxos_(computer_science)#Phase_1a:_Prepare
                returnMessage = Message(self, acceptor, "PREPARE", None, Computer.n)
                self.network.queueMessage(returnMessage)

            Computer.n += 1

        # Proposer naar ACCEPTOR, dit handelt een acceptor af
        elif message.messageType == "PREPARE":
            if message.n > self.prior:
                returnMessage = Message(self, message.src, "PROMISE", self.value, self.prior)
                self.network.queueMessage(returnMessage)

        # Acceptor naar PROPOSER, dit handelt een proposer af
        elif message.messageType == "PROMISE":
            self.promises += 1

            # 50% accepted is not enough
            if self.promises > (len(self.network.acceptors) // 2):
                if message.value is not None:
                    self.value = message.value if message.value > self.value else self.value

                if not self.accepted:
                    for acceptor in self.network.acceptors:
                        returnMessage = Message(self, acceptor, "ACCEPT", self.proposed, message.n)
                        self.network.queueMessage(returnMessage)

                    self.promises = 0
                    self.accepted = True

        # Proposer naar ACCEPTOR, dit handelt een acceptor af
        elif message.messageType == "ACCEPT":
            if self.prior < message.n:
                self.prior = message.n
                self.value = message.value

                returnMessage = Message(self, message.src, "ACCEPTED", self.value, self.prior)
                self.network.queueMessage(returnMessage)
            else:
                returnMessage = Message(self, message.src, "REJECTED", None, self.prior)
                self.network.queueMessage(returnMessage)

        elif message.messageType == "ACCEPTED":
            self.value = message.value

        elif message.messageType == "REJECTED":
            self.rejects += 1

            if self.rejects > (len(self.network.acceptors) // 2):
                Computer.n += 1
                self.rejected = True

            returnMessage = Message(self, message.src, "PREPARE", None, Computer.n)
            self.network.queueMessage(returnMessage)
