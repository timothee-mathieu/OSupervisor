from threading import Thread
from utils import osdata

#Global stop_thread
stop_thread = False

class CollectData1(Thread):

 

    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        
        global stop_thread
        while True:
            if stop_thread:
                print("done")
                break
            else:
                osdata.listUsers(self.conn)
                osdata.setUserData(False)
            if stop_thread:
                print("done") 
                break
            else:
                osdata.listFloatingIPs(self.conn)
                osdata.setFloatingIPData(False)
            if stop_thread: 
                print("done")
                break
            else:
                osdata.listPorts(self.conn)
                osdata.setPortData(False)
            if stop_thread: 
                print("done")
                break
            else:
                osdata.listRouters(self.conn)
                osdata.setRouterData(False)
            if stop_thread:
                print("done") 
                break
            else:
                osdata.listImages(self.conn)
                osdata.setImageData(False)
            if stop_thread:
                print("done") 
                break
            else:
                osdata.listSecGroupRules(self.conn)
                osdata.setSecGroupRuleData(False)
            if stop_thread:
                print("done") 
                break
            else:
                osdata.listNetworkAgents(self.conn)
                osdata.setNetworkAgentData(False)
                stop_thread = True



class CollectData2(Thread):

    

    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        
        global stop_thread
        while True:
            if stop_thread: 
                print("done")
                break
            else:
                osdata.listServers(self.conn)
                osdata.setServerData(False)
            if stop_thread:
                print("done") 
                break
            else:
                osdata.listNetworks(self.conn)
                osdata.setNetworkData(False)
            if stop_thread: 
                print("done")
                break
            else:
                osdata.listSubnets(self.conn)
                osdata.setSubnetData(False)
            if stop_thread:
                print("done") 
                break
            else:
                osdata.listProjects(self.conn)
                osdata.setProjectData(False)
            if stop_thread: 
                print("done")
                break
            else:
                osdata.listSecGroup(self.conn)
                osdata.setSecGroupData(False)
            if stop_thread: 
                print("done")
                break
            else:
                osdata.listKeyPairs(self.conn)
                osdata.setKeyPairData(False)
            if stop_thread: 
                print("done")
                break
            else:
                osdata.listStacks(self.conn)
                osdata.setStackData(False)
                stop_thread = True
            
        
        
        

