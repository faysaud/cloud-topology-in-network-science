import random
import matplotlib.pyplot as plt
import networkx as nx
from ReadingCloudNetworks import CloudNetworks
from NetworkAnalysis import NetworkAnalysis, AttackModel
# from collections import Counter 


def RunSims():
        Networks=CloudNetworks()   
        Networks.Create_Networks_DictList()
        networks=Networks.get_networksDictList
        Model=AttackModel()
        Roles=['Network','Storage','Service']

        for Role in Roles:
            RoleSim(networks,Model,Role)        

        

def RoleSim(networks,model,Role):
    results = []
    Rvirtex=[] 
    pers=model.get_per
    Analysis= NetworkAnalysis()
    Analysis.set_victim='Nodes'

    for network in networks:
        result=[]
        G = network['graph'].copy()
        attributes= nx.get_node_attributes(G,"role")
        print(attributes)
        for node,role in attributes.items():
            # role=str(role)
            if role in(Roles_V[Role]):
                Rvirtex.append(node)
                print(node,role)

        for i in range(len(pers)):
            random.shuffle(Rvirtex)
            batche = model.return_batch(Rvirtex,pers[i])
            G.remove_nodes_from(batche)
            NCC,LCCN ,ASP, diam,ACC, avg_degree,avg_Cluster= Analysis.properties(G)
            result.append([NCC ,round(LCCN/len(G),2) ,ASP, diam,ACC, avg_degree,avg_Cluster,pers[i],network['name']])
                # attributes= nx.get_node_attributes(G,"role")
                # typeCountDict=Counter([v for k, v in attributes.items()])
                # types=[k for k, v in typeCountDict.items()]
                # countList=[v for k, v in typeCountDict.items()]  
                # print(name,types,countList)

        results.append(result)

    Analysis.set_Results=results
    Analysis.ResultsTable('RoleAttack',f"{Role}_Attack")
    for type in Analysis.plotTypes:
        Analysis.plot(type,f"{Role} attack")
        print(type)
        plt.savefig(f"C:\\Users\\fayoy\\OneDrive\\Desktop\\networkx\\RoleAttack\\{Role}_{type}.png",bbox_inches ="tight") 
    return results


# Global var
Roles_V={'Network':"top_of_rack_switch, aggregation_switch, core_switch,security_gateway, edge_ingress, load_balancer,api_gateway, ingress_gateway",
            "Storage":"storage_node, database, storage, cache",
            "Service":"hypervisor_host, web-service, app_service, microservice"}

RunSims()