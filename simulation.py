from network import Network
from message import Message
from computer import Computer


class Simulation():
    """The Simulation class."""

    def __init__(self, nProposers, nAcceptors, tMax, events, network):
        """Initialises the Simulation class."""
        self.nProposers = nProposers
        self.nAcceptors = nAcceptors
        self.tMax = tMax
        self.events = events
        self.network = network

    def run(self):
        """Runs the simulation."""
        for tick in range(self.tMax):
            tickVal = str(tick).zfill(3)
            if (not self.network.numberOfMessages()) and (not self.numberOfEvents()):
                return None  # Simulation is stopped

            event = self.events.get(tick)
            # print(event)
            if event is not None:
                (F, R, pC, pV) = event
                for computer in F:
                    computer.setFailing(True)
                for computer in R:
                    computer.setFailing(False)
                if (pC is not None) and (pV is not None):
                    message = Message(None, pC, "PROPOSE", pV)
                    pC.deliverMessage(message)
                    print(f"{tickVal}: {message}")
                else:
                    message = self.network.extractMessage()
                    if message is not None:
                        print(f"{tickVal}: {message}")
                        message.dst.deliverMessage(message)

            else:
                message = self.network.extractMessage()
                if message is not None:
                    print(f"{tickVal}: {message}")
                    message.dst.deliverMessage(message)

    def numberOfEvents(self):
        """Gets the number of events for this simulation."""
        return len(self.events)


if __name__ == "__main__":
    network = Network()
    network.setProposers([Computer(i, "Proposer", network) for i in range(1, 1 + 1)])
    network.setAcceptors([Computer(i, "Acceptor", network) for i in range(1, 3 + 1)])

    E = {0: [[], [], network.proposers[0], 42]}

    s = Simulation(nProposers=1, nAcceptors=3,
                   tMax=15, events=E, network=network)
    s.run()

    # 1 3 15
    # 0 PROPOSE 1 42
    # 0 END
