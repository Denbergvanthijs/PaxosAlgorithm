from computer import Acceptor, Learner, Proposer
from message import Message
from network import Network


class Simulation():
    """The Simulation class."""

    def __init__(self, filename):
        """Initialises the Simulation class."""
        self.filename = filename

        self.nProposers = 0
        self.nAcceptors = 0
        self.tMax = 0
        self.events = {}
        self.network = Network()

    def setup(self) -> None:
        """Setup of the simulation."""

        with open(f"./inputs/{self.filename}.txt", "r") as fileWithData:
            simulationValues = fileWithData.readline().split()

            self.nProposers = int(simulationValues[0])
            self.nAcceptors = int(simulationValues[1])

            if len(simulationValues) == 3:
                self.nLearners = None
                self.tMax = int(simulationValues[2])
            else:
                self.nLearners = int(simulationValues[2])
                self.tMax = int(simulationValues[3])

            eventDetails = fileWithData.readlines()

        self.network.proposers = [Proposer(i, self.network) for i in range(1, self.nProposers + 1)]
        self.network.acceptors = [Acceptor(i, self.network) for i in range(1, self.nAcceptors + 1)]
        if self.nLearners is not None:
            self.network.learners = [Learner(i, self.network) for i in range(1, self.nLearners + 1)]

        for i, line in enumerate(eventDetails, start=0):
            data = line.split()

            if len(data) == 2:
                break

            event = [[], [], None, None]
            if data[1].upper() == "PROPOSE":
                ID, value = int(data[2]) - 1, int(data[3])
                event[2] = self.network.proposers[ID]
                event[3] = value

            elif data[1].upper() == "FAIL":
                cType, ID = data[2], int(data[3]) - 1
                if cType.upper() == "PROPOSER":
                    event[0].append(self.network.proposers[ID])
                elif cType.upper() == "ACCEPTOR":
                    event[0].append(self.network.acceptors[ID])

            elif data[1].upper() == "RECOVER":
                cType, ID = data[2], int(data[3]) - 1
                if cType.upper() == "PROPOSER":
                    event[1].append(self.network.proposers[ID])
                elif cType.upper() == "ACCEPTOR":
                    event[1].append(self.network.acceptors[ID])

            self.events[int(data[0])] = event

    def run(self) -> None:
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
    # NOTE: Only one of the examples can be on at a time

    # Example 1
    # s = Simulation(filename="example1")

    # s.setup()
    # Efake = {0: [[], [], s.network.proposers[0], 42]}

    # Example 2
    # s = Simulation(filename="example2")
    # s.setup()

    # Efake = {0: [[], [], s.network.proposers[0], 42],
    #          8: [[s.network.proposers[0]], [], None, None],
    #          11: [[], [], s.network.proposers[1], 37],
    #          26: [[], [s.network.proposers[0]], None, None]}

    # bikedata 1
    s = Simulation(filename="bikedata1")
    s.setup()

    Efake = {0: [[], [], s.network.proposers[0], 8],
             10: [[], [], s.network.proposers[0], 61],
             20: [[], [], s.network.proposers[0], 90],
             30: [[], [], s.network.proposers[0], 64],
             40: [[], [], s.network.proposers[0], 17],
             50: [[], [], s.network.proposers[0], 8],
             60: [[], [], s.network.proposers[0], 78],
             70: [[], [], s.network.proposers[0], 62]}

    assert s.events == Efake
    s.run()
