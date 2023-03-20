import salabim as sim


worker_panel = 3
initial_steel  = 0
panel_capacity = 40
steel_capacity = 1000



class ImportExport_warehouse(sim.Component):
    def setup(self, steel, panels):
        self.steel = steel
        self.panels = panels
        self.exported_panels = 0

    

    

ImportExport_warehouse = 
# class ImportExport_warehouse:
#     def __init__(self, env):
#         self.steel = simpy.Container(env, capacity= steel_capacity, init= initial_steel)
#         self.panels = simpy.Container(env, capacity= panel_capacity, init= 0)
#         self.importcontrol = env.process(self.importer(env))
#         self.exportcontrol = env.process(self.exporter(env))
#         self.exported_panels = 0

#     def importer(self, env):
#         yield env.timeout(0)
#         while True:
#             if self.steel.level <= 20:
#                 print('[Warehouse] Need to import steel. Making order')
#                 yield env.timeout(16)
#                 print('[Warehouse] Steel arrived from supplier')
#                 yield self.steel.put(100)
#                 print('[Warehouse] New steel stock is %d' %self.steel.level)
#             else:
#                 yield env.timeout(1)

#     def exporter(self, env):
#         yield env.timeout(0)
#         while True:
#             if self.panels.level >= panel_capacity*0.7:
#                 print('[Warehouse] Export panels')
#                 yield env.timeout(4)
#                 yield self.panels.get(10)
#                 self.exported_panels += 1
#                 yield env.timeout(8)
#             else:
#                 yield env.timeout(1)


# class FabricationHall:
#     def __init__(self, env):
#         self.steel = simpy.Container(env, capacity= 20)
#         self.panels = simpy.Container(env, capacity= 5)
#         self.importcontrol = env.process(self.importer(env))
#         self.exportcontrol = env.process(self.exporter(env))
#         self.fabricatorr = env.process(self.fabricator(env))

#     def importer(self, env):
#         yield env.timeout(0)
#         while True:
#             if self.steel.level < 20:
#                 print('[Fabrication] Need to import steel. Asking from warehouse')
#                 yield env.timeout(2)
#                 yield ImportExport_warehouse.steel.get(10)

#                 yield self.steel.put(10)
#                 print('[Fabrication] Steel arrived from warehouse')
#                 print('[Fabrication] New steel stock is %d' %self.steel.level)
#             else:
#                 yield env.timeout(1)

#     def exporter(self, env):
#         yield env.timeout(0)
#         while True:
#             if self.panels.level >= 4:
#                 print('[Fabrication] Export panels to warehouse')
#                 yield env.timeout(0)
#                 yield self.panels.get(self.panels.level)
#                 yield ImportExport_warehouse.panels.put(self.panels.level)
#                 yield env.timeout(2)
#             else:
#                 yield env.timeout(1)

#     def fabricator(self, env):
#         print(env.now)
#         yield env.timeout(0)
#         while True:
#             if self.steel.level >= 5 and self.panels.level + 1 < self.panels.capacity:
#                 yield self.steel.get(5)
#                 yield self.panels.put(1)
#                 yield env.timeout(2)
#             else:
#                 yield env.timeout(1)
            


# # env=simpy.Environment()
# env=simpy.rt.RealtimeEnvironment(factor=0.1, strict=False)

# ImportExport_warehouse = ImportExport_warehouse(env)
# FabricationHall = FabricationHall(env)



# env.run(until=600)

# class Shipyard:
#     def __init__(self, env):
#         self.steel = simpy.Container(env, capacity= steel_capacity, init= initial_steel)
#         self.panels = simpy.Container(env, capacity= panel_capacity, init= 0)
       
# worker = simpy.Resource(capacity=10, name='Worker', )

# class Welding_machine(object):
#     def __init__(self, env, name, worker):
#         self.name =name
#         self.env = env
#         self.panels_made = 0
        
    
    
#     def working(self,):
#         while True:
#             yield simpy.request,self,worker
#             print('Available workers present start work at %d' %env.now)
#             yield Welding_machine.workers.get(2)
            
            

        

# def welder(env, Shipyard):
#     while True:
#         yield Shipyard.steel.get(5)
#         panel_welding_time = 10
#         yield env.timeout(panel_welding_time)
#         yield Shipyard.panels.put(1)
#         print('Made a panel at time %d' %env.now)


# env=simpy.Environment()
# Shipyard = Shipyard(env)

# def welder_gen(env, Shipyard):
#     for i in range(worker_panel):
#         env.process(welder(env, Shipyard))
#         yield env.timeout(0)

# welder_gen = env.process(welder(env, Shipyard))



# env.run(until = 500)
# print(f'Ready panels %d' % Shipyard.panels.level)