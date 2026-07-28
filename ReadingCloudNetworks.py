import networkx as nx
import os
import xlrd

#  this class creat netowrks graphs from xls nodes and links files, node files have a second colume specifing the role of the node
# this role is a added to as attribute to the nodes  

class CloudNetworks:
    def __init__(self):
        self.networkNames=[]
        self.topologies_names = ["FT", "L", "MS"] 
        self.networksDictList=[]


    def get_Files(self,topology_path):
        network_dircs= os.listdir(topology_path) #for all the directories within a network 
        Edges_files,Nodes_files =[],[]

        for network_dirc in network_dircs:
            all_files=os.listdir(f'{topology_path}/{network_dirc}')
            for file in all_files:
                if file == 'edges.xls':
                    Edges_files.append(f'{topology_path}/{network_dirc}/{file}')
                elif file == 'nodes.xls':
                    Nodes_files.append(f'{topology_path}/{network_dirc}/{file}')
            
        return Nodes_files,Edges_files
   

    def Creaet_graphsWithAtt(self,Efiles,Vfiles,topology_name):
        Networks=[]
    
        for i in range(len(Vfiles)):
            Edges= []
            nodes=[]
            G = nx.Graph()
            Nbook = xlrd.open_workbook(Vfiles[i])
            Nsheet = Nbook.sheet_by_index(0)

            Ebook = xlrd.open_workbook(Efiles[i])
            Esheet = Ebook.sheet_by_index(0)

            # adding nodes with their TYPE 
            for row in range(1,Nsheet.nrows):
                data = Nsheet.row_slice(row)
                node = int(data[0].value)
                role = data[1].value
                nodes.append((node,{'role':role}))

            for row in range(1,Esheet.nrows):
                data = Esheet.row_slice(row)
                node1 = int(data[0].value)
                node2 = int(data[1].value)
                Edges.append((node1,node2))

            G.add_edges_from(Edges)
            G.add_nodes_from(nodes)

            graph_name = topology_name+'-'+str(G.number_of_nodes())
            self.networkNames.append(graph_name)
            Networks.append([graph_name,G])
        return Networks  


    def Cloud_networks(self,gen_path):
        absPath= os.path.dirname(os.path.abspath(__file__))
        gen_path=os.path.join(absPath,gen_path)
        networks_dircs= os.listdir(gen_path)
        N_path=[]
        Networks=[]
        for N in networks_dircs:
            N_path.append(f'{gen_path}/{N}')

        for i in range(len(self.topologies_names)):
            Nfiles,Efiles = self.get_Files(N_path[i])
            Networks.append(self.Creaet_graphsWithAtt(Efiles,Nfiles,self.topologies_names[i]))
        return Networks
        

    def Create_Networks_DictList (self,sample=False):
        if sample== 'small':
            gen_path='./cloud_networksC' #folder only contiane a subset of the datasets 
            Networks= self.Cloud_networks(gen_path)
        elif sample== 'mid':
            gen_path='./cloud_networksD' #folder only contiane a subset of the datasets (bigger subset then small)
            Networks= self.Cloud_networks(gen_path)
        else:  
            gen_path='./cloud_networksB' #folder all datasets  
            Networks= self.Cloud_networks(gen_path)
        
        for Networks_cats in Networks:
            for i in range(len(Networks_cats)):
                networkDIct = {}
                networkDIct['name'] = Networks_cats[i][0]
                networkDIct['graph'] =Networks_cats[i][1]
                self.networksDictList.append(networkDIct)
                
    @property
    def get_networksDictList(self):
        print("returning a list of directories of [{Name:network name, graph: graph location},{...}")
        return self.networksDictList