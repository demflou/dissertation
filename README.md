# Dissertation Repository
Distributed Task Management at the Edge of the Network

# Data Producer File Compilation
- I have created a data producer in python which create a csv file.
- python dataProducer.py -h (for help)
- python dataProducer.py -c <#columns> -r <#rows> -mn <min> -mx <max>

# Simulation Project Compilation
- I used to implement the project PyCharm CE IDE
- python Simulation.py -h (for help)
- python Simulation.py -c <#columns> -r <#rows> -n <#nodes>

# Tasks
- 

# Feature Learning
I classify the given data from [d0, dcolumns-1]. The last columns I implement it as a label with values 0 or 1.
Use Chi-square test to check how much important is each feature to y and return the k-most important features.
Then i use SelectKbest function to predict the most important dimensions of the row so i will check them later for import a new row into a node.
