class Computer:
    """The Computer class."""

    def __init__(self, ID, cType, network):
        """Initialises the Computer class."""
        if not cType.upper() in ("ACCEPTOR", "PROPOSER"):
            raise ValueError("Not a valid cType.")

        self.ID = ID
        self.cType = cType.upper()  # Cleans the string
        self.network = network

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

    def deliverMessage(self, message):
        """Delivers a message to a computer, via the Network-queue."""
        
        # PROPOSER
        if message.getMessageType() == "PROPOSE":
            message.setSource(self)
            message.setMessageType("PREPARE")

            for i in self.network.acceptors:
                message.setDestination(i)
                self.network.queueMessage(message)
        
        # ACCEPTOR
        elif message.getMessageType() == "PREPARE":
            pass
            # Check of message.value groter is dan de vorig bekende value 
            # Als dat zo is, stuur promise naar de proposer

        # PROPOSER
        elif message.getMessageType() == "PROMISE":
            message.setDestination(message.getSource())
            message.setSource(self)
            message.setMessageType("ACCEPT")

            self.network.queueMessage(message)

        # ACCEPTOR    
        elif message.getMessageType() == "ACCEPT":
            pass
            # Geaccpeteerd (ACCEPTED) als message.value hoogste is
            # Weigeren (REJECTED) als dat niet zo is 
            
