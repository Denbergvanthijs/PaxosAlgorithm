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

            event = self.events.pop(tick) if tick in self.events else None  # Removes current event, if event
            if event is not None:
                (F, R, pC, pV) = event

                for computer in F:
                    computer.failed = True
                for computer in R:
                    computer.failed = False

                if F:
                    print(f"{tickVal}: ** {' '.join([c.getName() for c in F])} kapot **")
                if R:
                    print(f"{tickVal}: ** {' '.join([c.getName() for c in R])} gerepareerd **")

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
                else:
                    print(f"{tickVal}:")

        print()
        for proposer in self.network.proposers:
            print(f"{proposer.getName()} heeft wel consensus (voorgesteld: {proposer.proposed}, geaccepteerd: {proposer.value})")

    def numberOfEvents(self):
        """Gets the number of events for this simulation."""
        return len(self.events)


if __name__ == "__main__":
    network = Network()
    network.proposers = [Computer(i, "Proposer", network) for i in range(1, 2 + 1)]
    network.acceptors = [Computer(i, "Acceptor", network) for i in range(1, 3 + 1)]

    E = {0: [[], [], network.proposers[0], 42],
         8: [[network.proposers[0]], [], None, None],
         11: [[], [], network.proposers[1], 37],
         26: [[], [network.proposers[0]], None, None]
         }

    # 2 3 50
    # 0 PROPOSE 1 42
    # 8 FAIL PROPOSER 1
    # 11 PROPOSE 2 37
    # 26 RECOVER PROPOSER 1
    # 0 END

    s = Simulation(nProposers=2, nAcceptors=3, tMax=50, events=E, network=network)
    s.run()
