import sys
import getopt
import random
import math
import pandas as pd
import numpy as np
import scipy as scp
from datetime import datetime, timedelta
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

rows_per_node = 100 #initial rows per node
important_cols = 3 #number of important features
phi = 0.75 #probability phi for store in remotely else locally
update_stats = 10 #update Node statistics every up update_stats new rows
transfer_cost = 1 #transfer_cost
prob_thres = 0.38 #Gaussian probability threshold
cost_thres = 30 #Transfer cost threshold
similar_thres = 0.10 #Similarity threshold
AA = 1 #value <a> in reverse sigmod function
BB = 1 #value <b> in reverse sigmod function
num_of_cluster = 2 #Number of clusters with similar nodes

class dNode:
    def __init__(self, n, df, noc, nor):
        self.id = n
        self.noc = noc
        self.nor = nor
        self.data = df.copy()
        self.avg_ = [-1] * noc
        self.dScore = [-1] * important_cols
        self.report_time = datetime.now()
        calc_avg(self) #get the avg of imported data
        #self.similarity = [-1] * noc
        classify_df(self)


def printNode (dn):
    print ('-'*100)
    print ('ID: ', dn.id)
    print ('ROW COUNTER: ', dn.nor)
    print ('COLUMNS COUNTER: ', dn.noc)
    print ('DATAFRAME')
    #print ('-'*100)
    #print (dn.data)
    print ('AVG: ', dn.avg_)
    print ('Score: ', dn.dScore)
    print ('Report Time: ', dn.report_time)
    #print ('SIMILARITY: ', dn.similarity)

def calc_avg(dn):
    res = dn.data.mean(axis=0).round(3)
    c = len(dn.data.columns)
    for i in range (c):
        dn.avg_[i] = res[i]
    return dn

def classify_df(dn):
    # DATA CONVERTING

    # Convert the data to be able to classify
    X = dn.data.iloc[:, :dn.noc-1]
    y = dn.data.iloc[:, dn.noc-1]

    # Extract the 2 most important columns
    topD = SelectKBest(score_func=chi2, k=important_cols)
    fit = topD.fit(X, y)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(X.columns)
    featureScores = pd.concat([dfcolumns, dfscores], axis=1)
    featureScores.columns = ['Dimensions', 'Score']  # naming the dataframe columns
    temp = featureScores.nlargest(important_cols, 'Score')  # print n best features
    for i in range(important_cols):
        dn.dScore[i] = temp['Dimensions'].index[i]

def insert_new_row(dn, new_row):
    dn.data = dn.data.append(new_row)
    print 'New row inserted correctly.'
    dn.nor+=1
    if (dn.nor % update_stats == 0):
        #Need to Update Node Stats
        print 'Updating Node ', dn.id
        dn.report_time = datetime.now()
        classify_df(dn)
        calc_avg(dn)

def cluster_dns(cl_arr, dn_avg):
    # cluster the nodes with avg of the specific column
    # save the top K nodes in a list
    # for loop for each node
    # decide for save local or remote
    dn_avg
    print 'cluster'

def main(argv):
    columns = -1
    rows = -1
    num_of_nodes = -1
    try:
        opts, args = getopt.getopt(argv, "hc:r:n:", ["help=", "col=", "rw=", "nd="])
    except getopt.GetoptError:
        print 'Simulation.py -c <#columns> -r <#rows> -n <#nodes>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'Simulation.py -c <#columns> -r <#rows> -n <#nodes>'
            sys.exit()
        elif opt in ("-c", "--col"):
            columns = int(arg)
        elif opt in ("-r", "--rw"):
            rows = int(arg)
        elif opt in ("-n", "--nd"):
            num_of_nodes = int(arg)
    if ((columns < 1) or (rows < 1) or (num_of_nodes < 1)):
        print "ERROR!! Wrong Arguments."
    else:
        print 'Given number of Columns is ', columns
        print 'Given number of Row is ', rows
        print 'Given number of Nodes is ', num_of_nodes
        print "Starting Simulation Successfully..."


    # Read the given data
    #dfData = pd.read_csv('~/Documents/My DI/Metaptixiako/Dissertation/Dataset/sofia-air-quality-dataset/2017-07_bme280sof.csv', sep=',', header=0)
    dfData = pd.read_csv('~/PycharmProjects/Dissertation/data.csv', sep=',', header=0)

    ListNodes_ = []

    # Split 100 rows at each node
    for n in range(num_of_nodes):
        t_df = pd.DataFrame(dfData.iloc[(n*rows_per_node)+1:((n+1)*rows_per_node)+1,:])
        ListNodes_.append(dNode(n, t_df, columns, rows_per_node))

    # Read the rest of the DataFrame
    for i in range((num_of_nodes*rows_per_node)+1, len(dfData)):
        Similarity = [-1] * num_of_nodes
        Gauss_prob = [1] * num_of_nodes
        rewards = [0] * num_of_nodes
        dn_avg = [0] * num_of_nodes
        cl_arr = []
        cost = [transfer_cost] * num_of_nodes
        new_row = dfData.iloc[[i]]
        if (random.random() <= phi):
            #REMOTE SAVE
            print ('REMOTE SAVE')
            #Dame prepei na allaksi to for pou kato kai na kamo for pano se ena cluster me ta simantika nodes
            for node in ListNodes_:
                cost[node.id] = cost[node.id]*random.randint(1, 75)
                a = []
                #Calculate the Similarity
                for j in node.dScore:
                    a.append(node.avg_[j])
                    a.append(new_row.iloc[0,j])
                res = np.std(a, ddof=1)
                Similarity[node.id] = round(res,3)
                #Calculate Gaussian
                for g in xrange (0, len(a), 2):
                    res = 1-(Gauss_prob[node.id] * scp.stats.norm(a[g], 0.4).pdf(a[g+1]))
                    Gauss_prob[node.id] = round(res,2)
                printNode(node)
            print 'GAUSS', Gauss_prob
            print 'SIMILARITY', Similarity
            r = 0
            for node in ListNodes_:
                # Calculate the report_time passed
                now = datetime.now()
                time_passed = (now - ListNodes_[0].report_time)
                if Gauss_prob[node.id] > prob_thres:
                    r += 0.5
                if cost[node.id] > cost_thres:
                    r += 0.15
                if Similarity[node.id] < similar_thres:
                    r += 0.35
                rewards[node.id] = 1 / (1 + math.exp((AA*time_passed.total_seconds())+(BB*r)))
            print rewards
        else:
            #LOCAL SAVE
            save_in = random.randint(0, num_of_nodes-1)
            print ('LOCAL SAVE in Node', save_in)
            insert_new_row(ListNodes_[save_in], new_row)

if __name__ == "__main__":
    main(sys.argv[1:])
