import random
import matplotlib.pyplot as plt
from ReadingCloudNetworks import CloudNetworks
from NetworkAnalysis import NetworkAnalysis, Attack


def RunSims():
        Networks=CloudNetworks()   
        Networks.Create_Networks_DictList()
        networks=Networks.get_networksDictList
        Attack_Model=Attack()
        VertexSim(networks,Attack_Model)        
        EdgeSim(networks,Attack_Model)



def VertexSim(networks,model):
    results = [] 
    pers=model.get_per
    Analysis= NetworkAnalysis("Nodes")

    # alliterating through all the networks 
    for network in networks:
        G = network['graph'].copy()
        result = [] #to store the properties of a networking while removing nodes 
        
        for i in range(len(pers)):
            V = list(G.nodes)
            random.shuffle(V)
            batche = model.return_batch(V,pers[i])
            G.remove_nodes_from(batche)
            umConnected_components,largest_componentSize ,ASP, diam,ACC, avg_degree,avg_Cluster= Analysis.properties(G)
            result.append([umConnected_components,round(largest_componentSize/len(G),2) ,ASP, diam,ACC, avg_degree,avg_Cluster,pers[i],network['name']])

        results.append(result)


    Analysis.set_Results=results
    Analysis.ResultsTable("V_RA")
    for type in Analysis.Plot_types:
        Analysis.plot(type,"random attack")
        plt.savefig(f"C:\\Users\\fayoy\\OneDrive\\Desktop\\networkx\\RandomAttacks\\V_{type}.png",bbox_inches ="tight") 
    return results


def EdgeSim(networks,model):

    results = [] 
    pers=model.get_per
    Analysis= NetworkAnalysis("Links")
    # alliterating through all the networks 
    for network in networks:
        G = network['graph'].copy()
        result = [] #to store the properties of a networking while removing edges 

        for i in range(len(pers)):
            E = list(G.edges)
            random.shuffle(E)
            batche = model.return_batch(E,pers[i])
            G.remove_edges_from(batche)
            umConnected_components,largest_componentSize ,ASP, diam,ACC, avg_degree,avg_Cluster= Analysis.properties(G)
            result.append([umConnected_components ,round(largest_componentSize/len(G),2) ,ASP, diam,ACC, avg_degree,avg_Cluster,pers[i],network['name']])
            
        results.append(result)

    Analysis.set_Results=results
    Analysis.ResultsTable("E_RA")
    for type in Analysis.Plot_types:
        Analysis.plot(type,"random attack")
        plt.savefig(f"C:\\Users\\fayoy\\OneDrive\\Desktop\\networkx\\RandomAttacks\\E_{type}.png",bbox_inches ="tight") 
    return results


RunSims()