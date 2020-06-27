from message import Message
from network import Network

from predictor import BikePredictor


class Computer:
    """The Computer class."""

    n = 1

    def __init__(self, ID: int, network: Network):
        """Initialises the Computer class."""
        self.ID = ID  # The computer number
        self.network = network  # The network the computers operate on

        self.failed = False  # If the current computer is broken
        self.n = 1  # Current number of transaction

    def getName(self) -> str:
        """Gets the name of the current computer."""
        return f"C{self.ID}"


class Proposer(Computer):
    """Proposer class."""

    def __init__(self, ID, network):
        """Initialises the Proposer class."""
        super(Proposer, self).__init__(ID, network)

        self.proposed = None  # Initial proposed value from external.
        self.promises = 0  # Number of promises from Acceptors to Proposers
        self.acceptedNs = []  # The accepted Ns

        self.highestN = 0  # Highest promised number
        self.highestV = 0  # Highest promised value

        self.accepts = 0  # Number of accepted from Acceptor to Proposer
        self.accepted = False  # If the current transaction is accepted

        self.rejects = 0  # Number of rejected from Accepters to Proposers
        self.rejected = False  # If the current transaction is

    def getName(self) -> str:
        """Gets the name of the current computer."""
        return f"P{self.ID}"

    def deliverMessage(self, message: Message) -> None:
        """Delivers a message to an Acceptor, via the Network-queue."""
        # Proposer returns "PREPARE" to all acceptors
        if message.messageType == "PROPOSE":
            self.proposed = message.value

            for acceptor in self.network.acceptors:
                # PREPARE message can not contain the proposed value:
                # https://en.wikipedia.org/wiki/Paxos_(computer_science)#Phase_1a:_Prepare

                returnMessage = Message(self, acceptor, "PREPARE", None, n=Computer.n)
                self.network.queueMessage(returnMessage)

            Computer.n += 1  # Increment the transaction number with one for every new PROPOSE

        # Proposer returns nothing to a single Acceptor or "PROMISE" to all Acceptors
        elif message.messageType == "PROMISE":
            self.promises += 1

            if message.value is not None:
                # self.value will have the highest value send by the proposers
                self.highestN, self.highestV = (message.n, message.value) if message.n > self.highestN else (self.highestN, self.highestV)

            # 50% accepted is not enough
            if self.promises > (len(self.network.acceptors) // 2):
                self.value = self.proposed  # If accepted, accepted value will be the proposed value

                if message.n not in self.acceptedNs:
                    if self.highestN > self.n:  # If an acceptor has an higher propose than current proposer
                        number, value = self.highestN, self.highestV
                    else:
                        number, value = self.n, self.proposed

                    for acceptor in self.network.acceptors:
                        returnMessage = Message(self, acceptor, "ACCEPT", value, n=number)
                        self.network.queueMessage(returnMessage)

                    self.promises = 0
                    self.acceptedNs.append(number)

        # Proposer returns nothing
        elif message.messageType == "ACCEPTED":
            self.value = message.value
            self.accepts += 1

            if self.accepts > (len(self.network.acceptors) // 2):
                if not self.accepted:  # If not yet accepted
                    self.accepted = True

                    for learner in self.network.learners:
                        returnMessage = Message(self, learner, "SUCCES", self.value, self.n)
                        self.network.queueMessage(returnMessage)

        # Proposer returns nothing to a single Acceptor or "PREPARE" to all Acceptors
        elif message.messageType == "REJECTED":
            self.rejects += 1

            if self.rejects > (len(self.network.acceptors) // 2):
                if not self.rejected:  # If not yet rejected
                    self.rejected = True

                    for acceptor in self.network.acceptors:
                        returnMessage = Message(self, acceptor, "PREPARE", None, Computer.n)
                        self.network.queueMessage(returnMessage)


class Acceptor(Computer):
    """Acceptor class."""

    def __init__(self, ID, network):
        """Initialises the Acceptor  class."""
        super(Acceptor, self).__init__(ID, network)

        self.priorN = 0  # Prior number of transaction
        self.value = None  # Current accepted value

    def getName(self) -> str:
        """Gets the name of the current computer."""
        return f"A{self.ID}"

    def deliverMessage(self, message: Message) -> None:
        """Delivers a message to a Proposer, via the Network-queue."""
        # Acceptor returns any of: {Nothing, "PROMISE"} to Proposer
        if message.messageType == "PREPARE":
            if message.n > self.priorN:
                returnMessage = Message(self, message.src, "PROMISE", self.value, n=message.n)
                self.network.queueMessage(returnMessage)

        # Acceptor returns any of: {"ACCEPTED", "REJECTED"} to Proposer
        elif message.messageType == "ACCEPT":
            if message.n > self.priorN:
                self.priorN = message.n
                self.value = message.value

                returnMessage = Message(self, message.src, "ACCEPTED", self.value, n=self.priorN)
                self.network.queueMessage(returnMessage)
            else:
                returnMessage = Message(self, message.src, "REJECTED", None, n=self.n)
                self.network.queueMessage(returnMessage)


class Learner(Computer):
    """Learner class."""

    pred = BikePredictor()

    def __init__(self, ID, network):
        """Initialises the learner."""
        super(Learner, self).__init__(ID, network)
        self.predictor = Learner.pred.predictor

    def getName(self):
        """Gets the name of the current computer."""
        return f"L{self.ID}"

    def deliverMessage(self, message: Message) -> None:
        """Learner delivers a message with prediction to the message source."""

        if message.messageType == "SUCCES":
            prediction = self.predictor(message.value)

            returnMessage = Message(self, message.src, "PREDICTED", prediction, message.n)
            self.network.queueMessage(returnMessage)
