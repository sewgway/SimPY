import simpy


worker_panel = 3
initial_steel  = 100
panel_capacity = 10
steel_capacity = 1000

class Shipyard:
    def __init__(self, env):
        self.steel = simpy.Container(env, capacity= steel_capacity, init= initial_steel)
        self.panels = simpy.Container(env, capacity= panel_capacity, init= 0)


class Welding_machine(object):
    def __init__(self, env, name, worker):
        self.name =name
        self.env = env
        self.panels_made = 0
        self.workers = 19
        
    
    
    def working(self,):
        while True:
            if Welding_machine.workers >= 2:
                print('Available workers present start work at %d' %env.now)
                yield Welding_machine.workers.get(2)
            
            

        

def welder(env, Shipyard):
    while True:
        yield Shipyard.steel.get(5)
        panel_welding_time = 10
        yield env.timeout(panel_welding_time)
        yield Shipyard.panels.put(1)
        print('Made a panel at time %d' %env.now)


env=simpy.Environment()
Shipyard = Shipyard(env)

def welder_gen(env, Shipyard):
    for i in range(worker_panel):
        env.process(welder(env, Shipyard))
        yield env.timeout(0)

welder_gen = env.process(welder(env, Shipyard))



env.run(until = 500)
print(f'Ready panels %d' % Shipyard.panels.level)