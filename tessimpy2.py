import simpy
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

print('hi')
worker_panel = 3
initial_steel  = 0
panel_capacity = 40
steel_capacity = 1000

class ImportExport_warehouse:
    def __init__(self, env):
        self.steel = simpy.Container(env, capacity= steel_capacity, init= initial_steel)
        self.panels = simpy.Container(env, capacity= panel_capacity, init= 0)
        self.importcontrol = env.process(self.importer(env))
        self.exportcontrol = env.process(self.exporter(env))
        self.exported_panels = 0

    def importer(self, env):
        yield env.timeout(0)
        while True:
            if self.steel.level <= 20:
                print('[Warehouse] Need to import steel. Making order')
                yield env.timeout(16)
                print('[Warehouse] Steel arrived from supplier')
                yield self.steel.put(100)
                print('[Warehouse] New steel stock is %d' %self.steel.level)
            else:
                yield env.timeout(1)

    def exporter(self, env):
        yield env.timeout(0)
        while True:
            if self.panels.level >= panel_capacity*0.7:
                print('[Warehouse] Export panels')
                yield env.timeout(4)
                yield self.panels.get(10)
                self.exported_panels += 1
                print("Exported panels so far are: %d" %self.exported_panels)
                yield env.timeout(8)
            else:
                yield env.timeout(1)


class FabricationHall:
    def __init__(self, env):
        self.steel = simpy.Container(env, capacity= 300)
        self.panels = simpy.Container(env, capacity= 5)
        self.importcontrol = env.process(self.importer(env))
        self.exportcontrol = env.process(self.exporter(env))
        self.fabricatorr = env.process(self.fabricator(env))

    def importer(self, env):
        yield env.timeout(0)
        while True:
            if self.steel.level < 30:
                print('[Fabrication] Need to import steel. Asking from warehouse')
                yield env.timeout(2)
                yield ImportExport_warehouse.steel.get(10)

                yield self.steel.put(10)
                print('[Fabrication] Steel arrived from warehouse')
                print('[Fabrication] New steel stock is %d' %self.steel.level)
            else:
                yield env.timeout(1)

    def exporter(self, env):
        yield env.timeout(0)
        while True:
            if self.panels.level >= 4:
                print('[Fabrication] Export panels to warehouse')
                amount_to_be_transferred = self.panels.level
                yield self.panels.get(amount_to_be_transferred)
                yield ImportExport_warehouse.panels.put(amount_to_be_transferred)
                yield env.timeout(2)
            else:
                yield env.timeout(1)

    def fabricator(self, env):
        print(env.now)
        
        while True:
            if self.steel.level >= 5 and self.panels.level + 1 < self.panels.capacity:
                yield self.steel.get(5)
                yield self.panels.put(1)
                yield env.timeout(2)
            else:
                yield env.timeout(1)
            
def clock(env,A, B):
    yield env.timeout(0)
    while True:
            xlist.append(env.now)
            ylist1.append(A.steel.level)
            ylist2.append(A.panels.level)
            expopanels.append(A.exported_panels)
            print('Steel %d' %A.steel.level)      
            yield env.timeout(2)

ylist1=[]
ylist2=[]
expopanels=[]
xlist=[]

# env=simpy.Environment()
env=simpy.rt.RealtimeEnvironment(factor=0.01, strict=False)

ImportExport_warehouse = ImportExport_warehouse(env)
FabricationHall = FabricationHall(env)
env.process(clock(env, ImportExport_warehouse, FabricationHall))

SIMTIME=500

env.run(until=SIMTIME)
fig = plt.figure()

l, = plt.plot([], [], 'k-', label='Steel')
m, = plt.plot([], [], 'r-', label='Panels')
o, = plt.plot([], [], 'g-', label='Exported panels')
plt.legend(loc='upper left')
metadata=dict(title='Movie', artist='Panos')
writer = PillowWriter(fps=15, metadata=metadata)



plt.xlim(0,SIMTIME)
plt.ylim(0,100)

with writer.saving(fig, 'animation.gif', 100):
    for i in range(len(xlist)):
        l.set_data(xlist[0:i], ylist1[0:i])
        m.set_data(xlist[0:i], ylist2[0:i])
        o.set_data(xlist[0:i], expopanels[0:i])
        writer.grab_frame()     

