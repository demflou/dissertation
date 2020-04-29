import sys
import getopt
import pandas as pd
import numpy as np
from matplotlib import pyplot
from sklearn.datasets import make_classification, make_regression
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import chi2

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

    #convert the data to be able to classify
    dfData = pd.read_csv('data.csv', sep=',', header=0)
    print dfData.head()
    X = dfData.iloc[:,0:columns-2]
    y = dfData.iloc[:, columns-1]

    #extract the 2 most important columns
    topD = SelectKBest(score_func=chi2, k=2)
    fit = topD.fit(X, y)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(X.columns)
    featureScores = pd.concat([dfcolumns, dfscores], axis=1)
    featureScores.columns = ['Dimensions', 'Score']  # naming the dataframe columns
    x = featureScores.nlargest(2, 'Score')  # print 10 best features
    print x
    m1 = x['Dimensions'].iloc[0]
    max1 = m1[1:]
    m2 = x['Dimensions'].iloc[1]
    max2 = m2[1:]
    print max1, max2

    #    model = LinearRegression()
    #    transform(model.fit(dfData))
    #    importance = model.coef_

if __name__ == "__main__":
    main(sys.argv[1:])
