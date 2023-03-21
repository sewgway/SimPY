import simpy
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import PillowWriter
import tqdm
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

worker_panel = 3
initial_steel  = 0
panel_capacity = 40
steel_capacity = 1000
forklift_capacity = 5

class ForkliftGarage:
    def __init__(self,env, forklift_capacity):
        self.forklifts = simpy.Resource(env,capacity=forklift_capacity)
        self.carrying_capacity = 2
        self.trans_time = 4
    def transport(self, mat, src, tgt, amount):
        material = getattr(src,mat)
        material2 = getattr(tgt, mat)
        while amount > 0:
            if amount > self.carrying_capacity:
                load = self.carrying_capacity
            else:
                load = amount
            yield material.get(load)
            yield material2.put(load)
            yield env.timeout(self.trans_time)
            amount += - load






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
                self.exported_panels += self.panels.level
                yield ImportExport_warehouse.panels.get(self.panels.level)
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
                with ForkliftGarage.forklifts.request() as request:
                    yield request
                    yield env.process(ForkliftGarage.transport('steel', ImportExport_warehouse, self, 10))
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
                with ForkliftGarage.forklifts.request() as request:
                    yield request
                    yield env.process(ForkliftGarage.transport('panels', self, ImportExport_warehouse, amount_to_be_transferred))
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
            
def monitor(env,A, B, C):
    yield env.timeout(0)
    while True:
            xlist.append(env.now)
            ylist1.append(A.steel.level)
            ylist2.append(A.panels.level)
            ylist3.append(B.steel.level)
            ylist4.append(B.panels.level)
            expopanels.append(A.exported_panels)
            forklift_ut.append(C.forklifts.count)
            item = (env.now, A.steel.level, A.panels.level, A.exported_panels, B.steel.level, B.panels.level,
              C.forklifts.count,
              len(C.forklifts.queue))
            data.append(item)
            # print('Steel %d' %A.steel.level)      
            yield env.timeout(1)

ylist1=[]
ylist2=[]
ylist3=[]
ylist4=[]
forklift_ut=[]
expopanels=[]
xlist=[]
data=[]

env=simpy.Environment()
# env=simpy.rt.RealtimeEnvironment(factor=0.01, strict=False)

ImportExport_warehouse = ImportExport_warehouse(env)
FabricationHall = FabricationHall(env)
ForkliftGarage = ForkliftGarage(env, forklift_capacity)
env.process(monitor(env, ImportExport_warehouse, FabricationHall, ForkliftGarage))

SIMTIME=1000


env.run(until=SIMTIME)
print('Finished with Simulation')
fig = plt.figure()

l, = plt.plot([], [], 'k-', label='Steel Warehouse')
m, = plt.plot([], [], 'r-', label='Panels Warehouse')
o, = plt.plot([], [], 'g-', label='Exported panels')
x, = plt.plot([], [], 'y-', label='Steel Fabrication Hall')
y, = plt.plot([], [], 'b-', label='Panels Fabrication Hall')
r, = plt.plot([], [], 'mo', label='Forklifts in use')
t, = plt.plot([], [], 'mo', label='Forklifts queue')
plt.legend(loc='upper left')
metadata=dict(title='Movie', artist='Panos')
writer = PillowWriter(fps=15, metadata=metadata)

dfdata = pd.DataFrame(data, columns=['Time', 'Steel Warehouse', 'Panels Warehouse', 'Exported panels', 'Steel Fabrication Hall', 'Panels Fabrication Hall', 'Forklifts in use', 'Forklifts queue'])

plt.xlim(0,SIMTIME)
plt.ylim(0,100)
output_path = os.path.join(dir_path, 'animation.gif')
with writer.saving(fig, output_path, 100):
    for i in range(len(data)):
        l.set_data(dfdata.loc[0:i, 'Time'], dfdata.loc[0:i,'Steel Warehouse'])
        m.set_data(dfdata.loc[0:i, 'Time'], dfdata.loc[0:i,'Panels Warehouse'])
        o.set_data(dfdata.loc[0:i, 'Time'], dfdata.loc[0:i,'Exported panels'])
        x.set_data(dfdata.loc[0:i, 'Time'], dfdata.loc[0:i,'Steel Fabrication Hall'])
        y.set_data(dfdata.loc[0:i, 'Time'], dfdata.loc[0:i,'Panels Fabrication Hall'])
        r.set_data(dfdata.loc[0:i, 'Time'], dfdata.loc[0:i,'Forklifts in use'])
        t.set_data(dfdata.loc[0:i, 'Time'], dfdata.loc[0:i,'Forklifts queue'])
      
        writer.grab_frame()     

