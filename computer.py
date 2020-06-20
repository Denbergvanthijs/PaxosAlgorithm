from message import Message
from network import Network


class Computer:
    """The Computer class."""

    n = 1

    def __init__(self, ID: int, cType: str, network: Network):
        """Initialises the Computer class."""
        if not cType.upper() in ("ACCEPTOR", "PROPOSER"):
            raise ValueError("Not a valid cType.")

        self.ID = ID  # The computer number
        self.cType = cType.upper()  # Cleans the string
        self.network = network

        self.failed = False  # If the current computer is broken

        self.proposed = None  # Initial proposed value from external.
        self.value = None  # Current accepted value
        self.n = 1  # Current number of transaction
        self.priorN = 0  # Prior number of transaction

        self.promises = 0  # Number of promises from Acceptors to Proposers
        self.accepted = []  # The accepted Ns

        self.rejects = 0  # Number of rejected from Accepters to Proposers
        self.rejected = False  # If the current transaction is

        self.highestN = 0  # Highest promised number
        self.highestV = 0  # Highest promised value

    def getName(self) -> str:
        """Gets the name of the current computer."""
        return f"{self.cType[0]}{self.ID}"

    def deliverMessage(self, message: Message) -> None:
        """Delivers a message to another computer, via the Network-queue."""
        # External to Proposer, Proposer returns "PREPARE" to all acceptors
        if message.messageType == "PROPOSE":
            self.proposed = message.value

            for acceptor in self.network.acceptors:
                # PREPARE message can not contain the proposed value:
                # https://en.wikipedia.org/wiki/Paxos_(computer_science)#Phase_1a:_Prepare

                returnMessage = Message(self, acceptor, "PREPARE", None, n=Computer.n)
                self.network.queueMessage(returnMessage)

            Computer.n += 1  # Increment the transaction number with one for every new PROPOSE

        # Proposer to Acceptor, Acceptor returns any of: {Nothing, "PROMISE"} to Proposer
        elif message.messageType == "PREPARE":
            if message.n > self.priorN:
                returnMessage = Message(self, message.src, "PROMISE", self.value, n=message.n)
                self.network.queueMessage(returnMessage)

        # Acceptor to Proposer, Proposer returns nothing to a single Acceptor or "PROMISE" to all Acceptors
        elif message.messageType == "PROMISE":
            self.promises += 1

            if message.value is not None:
                # self.value will have the highest value send by the proposers
                self.highestN, self.highestV = (message.n, message.value) if message.n > self.highestN else (self.highestN, self.highestV)

            # 50% accepted is not enough
            if self.promises > (len(self.network.acceptors) // 2):
                self.value = self.proposed  # If accepted, accepted value will be the proposed value

                if message.n not in self.accepted:
                    if self.highestN > self.n:  # If an acceptor has an higher propose than current proposer
                        number, value = self.highestN, self.highestV
                    else:
                        number, value = self.n, self.proposed

                    for acceptor in self.network.acceptors:
                        returnMessage = Message(self, acceptor, "ACCEPT", value, n=number)
                        self.network.queueMessage(returnMessage)

                    self.promises = 0
                    self.accepted.append(number)

        # Proposer to Acceptor, Acceptor returns any of: {"ACCEPTED", "REJECTED"} to Proposer
        elif message.messageType == "ACCEPT":
            if message.n > self.priorN:
                self.priorN = message.n
                self.value = message.value

                returnMessage = Message(self, message.src, "ACCEPTED", self.value, n=self.priorN)
                self.network.queueMessage(returnMessage)
            else:
                returnMessage = Message(self, message.src, "REJECTED", None, n=self.n)
                self.network.queueMessage(returnMessage)

        # Acceptor to Proposer, Proposer returns nothing
        elif message.messageType == "ACCEPTED":
            self.value = message.value

        # Acceptor to Proposer, Proposer returns nothing to a single Acceptor or "PREPARE" to all Acceptors
        elif message.messageType == "REJECTED":
            self.rejects += 1

            if self.rejects > (len(self.network.acceptors) // 2):
                if not self.rejected:  # If not yet rejected
                    self.rejected = True

                    for acceptor in self.network.acceptors:
                        returnMessage = Message(self, acceptor, "PREPARE", None, Computer.n)
                        self.network.queueMessage(returnMessage)
