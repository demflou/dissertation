import csv
import random
import sys
import getopt


def main(argv):
    columns = -1
    rows = -1
    minNum = -1
    maxNum = -1

    try:
        opts, args = getopt.getopt(argv, "hc:r:mn:mx:", ["help=", "col=", "rw=", "min=", "max="])
    except getopt.GetoptError:
        print 'dataProducer.py -c <#columns> -r <#rows> -mn <min> -mx <max>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'dataProducer.py -c <#columns> -r <#rows> -mn <min> -mx <max>'
            sys.exit()
        elif opt in ("-c", "--col"):
            columns = int(arg)
        elif opt in ("-r", "--rw"):
            rows = int(arg)
        elif opt in ("-mn", "--min"):
            minNum = int(arg)
        elif opt in ("-mx", "--max"):
            maxNum = int(arg)

    if ((columns < 1) or (rows < 1)):
        print 'ERROR!! Wrong given values.'
        print 'Columns and Rows must be greater than 0'
    else:
        print 'Given number of Columns is ', columns
        print 'Given number of Row is ', rows
        print 'Given min number is ', minNum
        print 'Given max number is', maxNum

    header = []
    for i in range(columns):
        header.append("d" + str(i))

    with open('data.csv', 'wb') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(header);
        for i in range(rows):
            rec = []
            for j in range(columns):
                if (j == columns-1):
                    rec.append(random.choice([0, 1]))
                else:
                    rec.append(round(random.random(), 2))
            writer.writerow(rec)
    file.close()

if __name__ == '__main__':
    main(sys.argv[1:])