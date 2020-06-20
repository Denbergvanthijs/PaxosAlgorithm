from computer import Computer
from message import Message
from network import Network


class Simulation():
    """The Simulation class."""

    def __init__(self, nProposers: int, nAcceptors: int, tMax: int, events: dict, network: Network):
        """Initialises the Simulation class."""
        self.nProposers = nProposers
        self.nAcceptors = nAcceptors
        self.tMax = tMax
        self.events = events
        self.network = network

    def run(self):
        """Runs the simulation."""
        for tick in range(self.tMax):
            if (not self.network.numberOfMessages()) and (not len(self.events)):
                break  # Break, not return or else code under the for-loop wil be skipped

            tickVal = str(tick).zfill(3)  # String representation of current ticknumber
            event = self.events.pop(tick, None)  # Removes current event, if event exists in dict

            if event is not None:
                F, R, pC, pV = event

                for computer in F:
                    computer.failed = True
                for computer in R:
                    computer.failed = False

                if F:  # Seperated from the for-loop to print all failed computers in a single line
                    print(f"{tickVal}: ** {' '.join([c.getName() for c in F])} kapot **")
                if R:  # Seperated from the for-loop to print all recovered computers in a single line
                    print(f"{tickVal}: ** {' '.join([c.getName() for c in R])} gerepareerd **")

                if (pC is not None) and (pV is not None):  # If external propose, with value
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

        print()  # Empty line
        for proposer in self.network.proposers:
            # TODO: Add `Pn heeft geen consensus.` if there's no concensus
            print(f"{proposer.getName()} heeft wel consensus (voorgesteld: {proposer.proposed}, geaccepteerd: {proposer.value})")


if __name__ == "__main__":
    # NOTE: Only 1 of the two examples can be on at a time
    # TODO: Write function to read the files from `./inputs` folder
    # TODO: Consider inheriting two classes from Computer: Proposer, Acceptor

    # Example 1
    # network = Network()
    # network.proposers = [Computer(i, "Proposer", network) for i in range(1, 1 + 1)]
    # network.acceptors = [Computer(i, "Acceptor", network) for i in range(1, 3 + 1)]

    # E = {0: [[], [], network.proposers[0], 42]}

    # s = Simulation(nProposers=2, nAcceptors=3, tMax=15, events=E, network=network)
    # s.run()

    # Example 2
    network = Network()
    network.proposers = [Computer(i, "Proposer", network) for i in range(1, 2 + 1)]
    network.acceptors = [Computer(i, "Acceptor", network) for i in range(1, 3 + 1)]

    E = {0: [[], [], network.proposers[0], 42],
         8: [[network.proposers[0]], [], None, None],
         11: [[], [], network.proposers[1], 37],
         26: [[], [network.proposers[0]], None, None]
         }

    s = Simulation(nProposers=2, nAcceptors=3, tMax=50, events=E, network=network)
    s.run()
