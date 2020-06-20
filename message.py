class Message():
    """The Message class."""

    def __init__(self, src, dst, messageType: str, value: int, n: int = None):
        """Initialises the Message class."""
        self.src = src
        self.dst = dst
        self.messageType = Message.checkMessageType(messageType)
        self.value = value

        if n is not None:
            self.n = n

    @staticmethod
    def checkMessageType(messageType: str) -> str:
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

    def __str__(self):
        """String representation of Message."""
        if self.src is None:  # If PROPOSE from external
            return f"\t-> {self.dst.getName()}  {self.messageType} v={self.value}"

        if self.messageType == "PROMISE":
            prior = f"n={self.src.priorN}, v={self.value}" if self.src.priorN != 0 else None
            return f"{self.src.getName()} -> {self.dst.getName()}  {self.messageType} n={self.n} (Prior: {prior})"

        if self.messageType in ("ACCEPT", "ACCEPTED"):
            return f"{self.src.getName()} -> {self.dst.getName()}  {self.messageType} n={self.n} v={self.value}"

        return f"{self.src.getName()} -> {self.dst.getName()}  {self.messageType} n={self.n}"
