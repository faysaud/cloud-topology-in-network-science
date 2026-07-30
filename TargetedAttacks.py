import random
import matplotlib.pyplot as plt
import networkx as nx
from ReadingCloudNetworks import CloudNetworks
from NetworkAnalysis import NetworkAnalysis, AttackModel



def RunSims():
        Networks=CloudNetworks()   
        Networks.Create_Networks_DictList()
        networks=Networks.get_networksDictList
        Model=AttackModel()
        centralities=['Degree','Betweenness',"VoteRank"]


        for centr in centralities:
            VertexSim(networks,Model,centr)
            if centr !='VoteRank':       
                EdgeSim(networks,Model,centr)



        
def VertexSim(networks,model,centr):
    results = [] 
    Analysis= NetworkAnalysis()
    Analysis.set_victim='Nodes'

    for network in networks:
        G = network['graph'].copy()
        i=0
        result =RecursivCentrAttack(network,G,i,centr,[],model,Analysis)     
        results.append(result)

    Analysis.set_Results=results
    Analysis.ResultsTable("TargetedAttacks",f"V_{centr}")
    for type in Analysis.Plot_types:
        Analysis.plot(type,f"{centr} attack")
        plt.savefig(f"C:\\Users\\fayoy\\OneDrive\\Desktop\\networkx\\TargetedAttacks\\V_{centr}_{type}.png",bbox_inches ="tight") 
    return results


def EdgeSim(networks,model,centr):

    results = [] 
    Analysis= NetworkAnalysis()
    Analysis.set_victim='Links'

    for network in networks:
            G = network['graph'].copy()
            i=0
            result =RecursivCentrAttack(network,G,i,centr,[],model,Analysis)
            results.append(result)

    Analysis.set_Results=results
    Analysis.ResultsTable("TargetedAttacks",f"E_{centr}")
    for type in Analysis.Plot_types:
        Analysis.plot(type,f"{centr} attack")
        plt.savefig(f"C:\\Users\\fayoy\\OneDrive\\Desktop\\networkx\\TargetedAttacks\\E_{centr}_{type}.png",bbox_inches ="tight") 
    return results




def RecursivCentrAttack(network,G,i,centr,results,model,Analysis):
    pers=model.get_per

    if Analysis.victim == "Nodes":
            Ranked_lists = V_CI_orderdList(G,centr)
    else:    
            Ranked_lists = E_CI_orderdList(G,centr) 
    
    batche = model.return_batch(Ranked_lists,pers[i])

    if Analysis.victim == "Nodes":
        G.remove_nodes_from(batche) # remove Nodes...
    else:
        R = [(u,v) for u,v,_ in batche] # remove edges...
        G.remove_edges_from(R)

    umConnected_components,LCCN ,ASP, diam,ACC, avg_degree,avg_Cluster= Analysis.properties(G)
    if LCCN:
        print("network After removal of ",pers[i],"of",network['name'])
        results.append([umConnected_components ,round(LCCN/len(G),2) ,ASP, diam,ACC, avg_degree,avg_Cluster,pers[i],network['name']])

    i+=1
    if  i>=len(pers):  return results
    else: return RecursivCentrAttack(network,G,i,centr,results,model,Analysis)




def V_CI_orderdList(G,centrality):
    #return an descending list of vertex based on CI specified by the paramenter 'centrality' 
    
    if centrality=="VoteRank" :CI_sortedList=nx.voterank(G);print('ranking nodes based on VoteRank centrality' )
    else:
        if centrality=="Betweenness": CI_Dict =nx.betweenness_centrality(G);print('ranking nodes based on Betweenness centrality' )
        else: CI_Dict =nx.degree_centrality(G);print('ranking nodes based on Degree degree' )

        CI_sortedDict = {k: v for k, v in sorted(CI_Dict.items(), key=lambda item: item[1],reverse=True)}
        CI_sortedList= list(CI_sortedDict.keys())

    return CI_sortedList  



def E_CI_orderdList(G, centrality):
    #return an order descending order edge list based on CI specified
    W = []

    if centrality == 'Betweenness':
        CI_Dict = nx.edge_betweenness_centrality(G)
        # CI_sortedDict = {k: v for k, v in CI_Dict.items()}
        for u,v in G.edges():
            W.append([u, v, CI_Dict[u,v]])

        CI_orderdList=sorted(W, key=lambda x: x[2],reverse=True)   
        
    else:
        # for degree equations from 'P. Holme, B. J. Kim, C. N. Yoon, and S. K. Han, “Attack vulnerability of complex networks,” '
        CI_Dict = nx.degree(G)
        for u,v in G.edges():
            W.append([u, v, CI_Dict[u]*CI_Dict[v]])
        CI_orderdList=sorted(W, key=lambda x: x[2],reverse=True)


    return CI_orderdList



RunSims()