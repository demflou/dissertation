import csv
import sys
import pandas as pd
import numpy as np

def main(argv):
    dfData = pd.read_csv('~/PycharmProjects/Dissertation/real_data1500K.csv', sep=',', header=0)
    rows = dfData.shape[0]
    c0 = 0
    c1 = 1
    res = -1
    with open('newdata.csv', 'wb') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(dfData.columns)
        for i in range (0, rows):
            #print dfData.iloc[i][10]
            if (dfData.iloc[i][10] >= 50.0):
                res = 1
                c1+=1
                #print res, c1
            else:
                res = 0
                c0+=1
                #print res, c0
            dfData["new_column"] = res
            writer.writerow(dfData.iloc[i])
    file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
