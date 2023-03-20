import salabim as sim

SEED = 42
MACHINES = 2     # amount of machines
INTERVAL = 10.0  # mean time between two jobs
DURATION = 5.0   # mean processing time of a job
JOBS = 10        # number of jobs that have to be completed


class Product(sim.Component):
    def process(self):
        yield self.request(machines)
        print(f"{self.name()} started at time {env.now()}")
        yield self.hold(DURATION)
        print(f"{self.name()} completed at time {env.now()}")


env = sim.Environment(random_seed=SEED)
machines = sim.Resource("machines", capacity=MACHINES)
sim.ComponentGenerator(Product, iat=sim.Exponential(INTERVAL), number=JOBS)
env.animate(True)
machines.claimers().animate(x=500, y=100, title="work in progress")
machines.requesters().animate(x=200, y=100, title="work waiting")
env.run(100.0)