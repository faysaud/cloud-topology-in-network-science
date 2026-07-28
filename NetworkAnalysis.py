import random
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import warnings
import re

class NetworkAnalysis:
    def __init__(self,victim):

        self._Results=0
        self.Plot_types=["LCC","diam","ASP","ACC","ADeg","cluster"]
        self.victim=victim

    def properties(self,G):
    #return properties of graph G
        Csizes=[]
        Connected_components = list(nx.connected_components(G))
        numConnected_components= len(Connected_components)
        if numConnected_components > 0: # only compute the properties if exist 1 or more connected components
            subG = G.subgraph(max(Connected_components, key=len))   
            if len(subG.nodes())>1: #only compute connected component properties, if existi a connected component that has at least 2 nodes 

                degrees_Dict =G.degree()
                degrees_list= [v for k, v in degrees_Dict]
                avg_degree= round(sum(degrees_list)/G.number_of_nodes(),1) 
                ACC = nx.average_clustering(G)
                
                # for ASP and diameter wil we will consider the gaint component and 
                ASP = nx.average_shortest_path_length(subG)
                diam = nx.diameter(subG)
                # get clusters sizes 
                for Connected_component in Connected_components:
                    C=G.subgraph(Connected_component)
                    if len(Connected_component) > 1 and not(nx.utils.graphs_equal(C,subG)):
                        Csizes.append(len(Connected_component)) 
                if len(Csizes) ==0:
                    avg_Cluster=0
                else:avg_Cluster=sum(Csizes)/len(Csizes)

                return [numConnected_components,len(subG) ,round(ASP,2), round(diam,2),round(ACC,2), round(avg_degree,2),round(avg_Cluster,2)]
            
            else:
                # Handle the case when there are no LCC
                return None, None,None,None, None,None,None
            
        else:
            # Handle the case when there are no connected components
            return None, None, None,None, None,None,None



    @property
    def Results(self): 
        print("getter method called") 
        return self._Results 

    @Results.setter
    def set_Results(self,results):
        self._Results=results
        print("setter method called") 
    @property
    def plotTypes(self): 
        print("getter method called") 
        return self.Plot_types 

    def plot(self,type,title):  
     
        # here specife the type/metric to be ploted by the function   
        if type =="NCC": TData=0 ; metric='NCC'
        elif type =="LCC": TData=1; metric='$|N_{LCC}| / |N|$ '
        elif type =="ASP": TData=2; metric='ASP'
        elif type =="diam": TData=3; metric='Diameter '
        elif type =="ACC": TData=4; metric='ACC '
        elif type =="ADeg": TData=5; metric='⟨K⟩'
        elif type =="cluster": TData=6; metric='⟨s⟩'


        else:
            warnings.warn("Warning...uncorrect type /n type parameter only takes NCC,LCC or diam /n value this function only plot: NCC,LCC and diameter, ") ; TData=0;metric='none'

        fig = plt.figure(dpi=400)
        ax = fig.subplots()
        markers = ['o', '*', 's',] # Add your desired markers here
        marker_idx=-1
        colors =["#FF5100", "#FF0000FF","#AD0A01","#E41C1CB8","#b0bf1a","#4be765","#4aa500","#3B6829","#42e8f3","#81a8e3","#50bbf0","#003bdd"] # four raneg of colors for the three the 3 type of cloud networks 

        plt.xticks(fontsize = 14)
        plt.yticks( fontsize = 14)

        for d in range(len(self._Results)):
            data = self._Results[d]
            x = [(item[7])*100 for item in data]
            y = [item[TData] for item in data]
            name= data[4][8]
            print(name)
            # adjest the marker shape and size based on the network 
            if d%4==0: marker_idx+=1 # change the marker after ploting 4 networks (for each topology)
            numericalVal= re.findall(r'\d+',name);  NSize=int(numericalVal[0]) #change marker size base on the netwrok size 
            if(1<NSize<200):marksSize=3#100  
            elif(100<NSize<700):marksSize=4 #500
            elif(700<NSize<2000):marksSize=6 #1000
            elif(2000<NSize<7000):marksSize=7 #5000
            else: marksSize=9
            ax.plot(x, y, marker=markers[marker_idx], linewidth=0.5, markersize=marksSize,color=colors[d],label=name)

        ax.set_xlabel(f'{self.victim} Removed (%)',fontsize=18)
        ax.set_ylabel(f'{metric}',fontsize=18)
        ax.set_title(f'{title}')
        plt.legend(bbox_to_anchor=(0.5, 1.35), loc='upper center',ncol=3)



    def ResultsTable(self,Fname):

        Table = pd.DataFrame()
        name,per,NCC,LCC=[],[],[],[]
        diam,ASP,ACC=[],[],[]
        avg_K,Avg_ClusterS=[],[]

        for result in  self.Results:
            for batches in result:
                name.append(batches[8])
                per.append(f"{((batches[7])*100)} %")
                NCC.append(batches[0])
                LCC.append(batches[1])
                ASP.append(batches[2])
                diam.append(batches[3])
                ACC.append(batches[4])
                avg_K.append(batches[5])
                Avg_ClusterS.append(batches[6])

        Table["Networks"]=name;
        Table[f"% {self.victim} removed"]= per
        Table["NCC"]= NCC
        Table["LCC/N"]=LCC
        Table["ASP(LCC)"] = ASP
        Table["Diameter(LCC)"]=diam
        Table["ACC"] =ACC
        Table["Avg Degress"] = avg_K 
        Table['Avg Cluster size']=Avg_ClusterS
        Table.to_csv(f'C:\\Users\\fayoy\\OneDrive\Desktop\\networkx\\RandomAttacks\\{Fname}.csv')



class Attack:

    def __init__(self):
        self.per=[0.0,0.01,0.05,0.1,0.15,0.2,0.3]
    
    # Function return a "per" percentage of the network starting from the beging of the list   
    def return_batch(self,lst,per):
        batch_size = round(len(lst)*per)
        # return a slice of the list 
        batch=lst[0:batch_size]
        return batch 

    @property
    def get_per(self):
        print("percentages of network removal")
        return self.per
