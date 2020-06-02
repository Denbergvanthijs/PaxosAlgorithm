from network import Network


class Simulation():
    """The Simulation class."""

    def __init__(self, nProposers, nAcceptors, tMax, events):
        """Initialises the Simulation class."""
        self.nProposers = nProposers
        self.nAcceptors = nAcceptors
        self.tMax = tMax
        self.events = events

        self.network = Network()

    def run(self):
        """Runs the simulation."""
        for tick in range(self.tMax):
            if (not self.network.numberOfMessages()) and (not self.numberOfEvents()):
                return None  # Simulation is stopped

            print(str(tick).zfill(3))

    def numberOfEvents(self):
        """Gets the number of events for this simulation."""
        return len(self.events)


if __name__ == "__main__":
    s = Simulation(nProposers=10, nAcceptors=10, tMax=40, events=[])
    s.run()
