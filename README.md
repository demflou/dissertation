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
- Split 100 rows in each Node [DONE]
- Classify the data of each Node [DONE]
- Get the most important dimensions [DONE]
- Calculate the average of each dimension for each Node [DONE]
- Calculate the similarity of each dimension for each Node using Standard Deviation (low value:close to mean, high value:spread out) [DONE]
- For every 50 new saved rows in Node Classify again, calculate the average and the similarity and update the report_time
- Get a number between 0,1 with probability and if it is greater than 0.65 save localy else save remotely
- Use a Gaussian probability function to find probability for each Node produce the specific new row Gaussian = g(di)*g(dj) (probability di and dj produce by Node Ni)
- With a reward function find the correct Node to save the row if (P(Ni) > threshold) then {reward += 10} if (cost(Ni) > threshold) then {reward+=10}
- Calculate the total reward using a reverse sigmod function 1/(1+exp(20x-20))
- total_reward = 1/(1+exp(a*(report_time)+b*(reward)))
- To avoid calculation for unnecessary Nodes we do a Cluster based on average of important dimension.

# Feature Learning
I classify the given data from [d0, dcolumns-1]. The last columns I implement it as a label with values 0 or 1.
Use Chi-square test to check how much important is each feature to y and return the k-most important features.
Then i use SelectKbest function to predict the most important dimensions of the row so i will check them later for import a new row into a node.
