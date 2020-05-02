import sys
import getopt
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

row_per_node = 100
important_rows = 2

class dNode:
    def __init__(self, n, df, noc, nor):
        self.id = n
        self.data = df.copy()
        self.cntr = nor
        self.avg_ = [-1] * noc
        calc_avg(self) #get the avg of imported data
        #self.similarity = [-1] * non

def printNode (dn):
    print ('ID: ', dn.id)
    #print ('COUNTER: ', dn.cntr)
    #print ('DATAFRAME')
    #print ('-'*100)
    #print (dn.data)
    print ('AVG: ', dn.avg_)
    #print ('SIMILARITY: ', dn.similarity)

def calc_avg(dn):
    res = dn.data.mean(axis=0).round(3)
    c = len(dn.data.columns)
    for i in range (c):
        dn.avg_[i] = res[i]
    return dn

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
    Similarity = [-1] * num_of_nodes

    # Split 100 rows at each node
    for n in range(num_of_nodes):
        t_df = pd.DataFrame(dfData.iloc[(n*row_per_node)+1:((n+1)*row_per_node)+1,:])
        ListNodes_.append(dNode(n, t_df, columns, row_per_node))

    # Print all Nodes
    for obj in ListNodes_:
        printNode(obj)


    # DATA CONVERTING

    # Convert the data to be able to classify
    X = dfData.iloc[:, 0:columns-2]
    y = dfData.iloc[:, columns-1]

    # Extract the 2 most important columns
    topD = SelectKBest(score_func=chi2, k=important_rows)
    fit = topD.fit(X, y)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(X.columns)
    featureScores = pd.concat([dfcolumns, dfscores], axis=1)
    featureScores.columns = ['Dimensions', 'Score']  # naming the dataframe columns
    x = featureScores.nlargest(important_rows, 'Score')  # print 10 best features
    print x
    m1 = x['Dimensions'].iloc[0]
    max1 = m1[1:]
    m2 = x['Dimensions'].iloc[1]
    max2 = m2[1:]
    print max1, max2


if __name__ == "__main__":
    main(sys.argv[1:])
