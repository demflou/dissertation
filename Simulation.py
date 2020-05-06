import sys
import getopt
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

rows_per_node = 100 #initial rows per node
important_cols = 3 #num of important features
phi = 0.75 #probability phi for store in remotely else locally
update_stats = 50 #update Node statistics every up update_stats new rows

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
    print ('ID: ', dn.id)
    print ('ROW COUNTER: ', dn.nor)
    print ('COLUMNS COUNTER: ', dn.noc)
    print ('DATAFRAME')
    print ('-'*100)
    print (dn.data)
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
    printNode(dn)
    dn.data = dn.data.append(new_row)
    print 'New row inserted correctly.'
    dn.nor+=1
    if (dn.nor % update_stats == 0):
        #Need to Update Node Stats
        print 'Updating Node ', dn.id
        dn.report_time = datetime.now()
        classify_df(dn)
        calc_avg(dn)
        printNode(dn)

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
    dfData = pd.read_csv('data.csv', sep=',', header=0)

    ListNodes_ = []

    # Split 100 rows at each node
    for n in range(num_of_nodes):
        t_df = pd.DataFrame(dfData.iloc[(n*rows_per_node)+1:((n+1)*rows_per_node)+1,:])
        ListNodes_.append(dNode(n, t_df, columns, rows_per_node))

    # Read the rest of the DataFrame
    for i in range((num_of_nodes*rows_per_node)+1, len(dfData)):
        Similarity = [-1] * num_of_nodes
        new_row = dfData.iloc[[i]]
        if (random.random() <= phi):
            #REMOTE SAVE
            print ('REMOTE SAVE')
            
        else:
            #LOCAL SAVE
            save_in = random.randint(0, num_of_nodes-1)
            print ('LOCAL SAVE in Node', save_in)
            insert_new_row(ListNodes_[save_in], new_row)

        #Calculate the Similarity
        for node in ListNodes_:
            a = []
            for i in node.dScore:
                a.append(node.avg_[i])
                a.append(new_row.iloc[0,i])
            res = np.std(a, ddof=1)
            Similarity[node.id] = round(res,3)

    #Calculate the report_time passed
    '''
        if(ListNodes_[0].report_time > ListNodes_[1].report_time):
        print 'Node 0 is greater'
        print 'NODE 0: ', ListNodes_[0].report_time
        now = datetime.now()
        print 'NOW: ', now
        print (now - ListNodes_[0].report_time)
        time_passed = (now - ListNodes_[0].report_time)
        if (time_passed > timedelta(microseconds=80000)):
            print "TOO LATE"
    '''
if __name__ == "__main__":
    main(sys.argv[1:])
