import sys
import random
import collections
from collections import deque
from operator import itemgetter
import time
import matplotlib.pyplot  as plot

source_directory = "" #path where the instance files are stored.
instance = []#list to store all the clauses of an instance 
no_of_variables = 0 # stores the number of variables present in each clause of the instance file
no_of_clauses = 0 # stores the number of clauses present in each instance file
max_tries = 10 # the number of restarts
max_flips = 1000# the number of flips
instance_file = open(source_directory + "/uf20-021.cnf", "r")# open and read the instance file
instance_file = instance_file.readlines()# read each line of the instance file
for line in range(len(instance_file)-3):#discarding the last 3 lines of the instance file and considering all the other lines
    if not (instance_file[line].lstrip().startswith('c') or instance_file[line].lstrip().startswith('p')):
    #if a line does not start with c or p then consider the line       
        a = instance_file[line].rstrip('0\n').split()# remove the 0 in the end of every clause
        instance.append(a)#append the clauses into the list
    if (instance_file[line].startswith('p')):# if a line starts with p then total number of variables and total number of clauses are obtained through that line
        no_of_variables = instance_file[line].split()[-2]# obtaining total number of variables
        no_of_clauses = instance_file[line].split()[-1] # obtaining total number of clauses
        
def flip(random_clause,instance,solution,tabu_list):# function to return the best or a random variable from an unsatisfied clause
    
    probability = random.uniform(0,1)# randomly selecting a probability
    try_solution = solution.copy()#creating a copy of the solution 


    if(probability > 0.4):# checking if the value of probability is greater than 0.4
        best_flip = {}#a dictionary to store the flipped variables is taken
        
       
        for variable in random_clause:#taking a loop for all the three variables of an unsatisfied random clause
           
            
            (try_solution[abs(int(variable))-1]) = (try_solution[abs(int(variable))-1]) * -1#flipping the selected variable in the solution 
            
            unsatisfied = 0 # number of unsatisfied clauses is assigned as zero
            
            for clauses1 in instance:# looping all the clauses in the instance file
                
                satisfiability = []#list assigned to store satisfied clauses
                
                for i in clauses1:# looping all the variables in a clause
                   
                    if(int(i) in try_solution):# checking if any of the variable in the clause matches any of the variable in the given solution
                    #that is if the value of variabe is true for the given solution
                        satisfiability.append(True)# if yes the clause is satisfied and appended as true in the satisfiability list 
                    else:# else the clause is unsatisfied and  appended as false in the satisfiability list 
                        satisfiability.append(False)
        
                if (True not in satisfiability):# all the false values of satisfiability list is taken
                    unsatisfied += 1  #storing the value of unsatisfied clauses   
                    
            best_flip.update({variable : unsatisfied})# update the dictionary with the variable and its number of unsatisfied clauses
        
            (try_solution[abs(int(variable))-1]) = (try_solution[abs(int(variable))-1]) * -1 # flipping the variable to its original value
            
          
        best_variable = sorted(best_flip.items(), key=itemgetter(1))# sorting the dictionary based on the number of unsatisfied clauses
        
        for i in range(0,len(random_clause)):# looping the variables of unsatisfied random clause
            
            if abs(int(best_variable[i][0])) not in tabu_list:#if the variable is not present in tabu list
                return abs(int(best_variable[i][0]))#return the variable
        
        return "TL"# return TL if all three variables are present in  the tabu list
    else:
        rand_clause = random_clause.copy()#create a copy of the random unsatisfied clause
        for i in range(0,len(rand_clause)):# looping the variables of unsatisfied random clause
            randvar = random.randint(0,len(rand_clause)-1)#selecting a random index of the random clause
            if abs(int(rand_clause[randvar])) in tabu_list:#check if the random variable of the clause is present in the tabu list
                rand_clause.pop(randvar)#if it is present remove it from the clause 
            else:# else return the random variable
                return abs(int(rand_clause[randvar]))
        return "TL"# return TL if all three variables are present in  the tabu list 
        
def tabu_search(instance, max_tries,max_flips):
    for i in range(max_tries):#loop in the range of maximum restarts
       solution = []# list to store the solution
       tabu_list = deque()# store the tabu_list as queue
       
       for i in range(1,(int(no_of_variables)+1)):# looping the variables
         solution.append([-i,i][random.randrange(2)])#generating a random solution and storing it in the solution list
         
       for i in range(max_flips):#loop in the range of maximum flips
           
           unsatisfied_clause = 0# variable to store unsatisfied clauses
           unsatisfied_clauses = []#list to store unsatisfied clauses
                 
           for clauses in instance:#looping all the clauses
               satisfiability = []#list to store satisfiable clauses
                     
               for variable in clauses:#looping every variable of a single clause
                   if(int(variable) in solution):# checking if any of the variable in the clause matches any of the variable in the given solution
                #that is if the value of variabe is true for the given solution
                       satisfiability.append(True)# if yes the clause is satisfied and appended as true in the satisfiability list
                   else:
                       satisfiability.append(False)# else the clause is unsatisfied and  appended as false in the satisfiability list 
                       
               if (True not in satisfiability):# all the false values of satisfiability list is taken
                   unsatisfied_clause += 1#storing the value of unsatisfied clauses 
                   unsatisfied_clauses.append(clauses)#appending the unsatisfied clauses in the unsatisfied clauses list
                   
           if(unsatisfied_clause == 0):# if unsatisfied clauses is zero then return solution
               return solution
           else:
               randclause = random.randint(0,(len(unsatisfied_clauses)-1))# choose an index for random clause
               random_clause = unsatisfied_clauses[randclause]# random unsatisfied clause
               
               a = flip(random_clause,instance,solution,tabu_list)#getting the best variable and second best variable or random variable to flip
           
               if a == "TL":# if all the variables of a clause is present in tabu list find new random clause
                   continue
               
               else:
                
                   if(len(tabu_list) <= 4):# if length of  tabu_listis less than or equal to 4
                  
                      tabu_list.append(a)# append the recently obtained best variable in the list
                      (solution[abs(int(a))-1]) = (solution[abs(int(a))-1]) * -1# flip the best variable in the solution
                   elif(len(tabu_list) == 5):# if length of tabu_list is equal to 5
                      tabu_list.popleft()#remove the first element or the leftmost element from the list
                      tabu_list.append(a)#store the recently obtained best variable
                      (solution[abs(int(a))-1]) = (solution[abs(int(a))-1]) * -1#  flip the best variable in the solution
                  
               
    return "no solution found"# return no solution found if solution is not found


iterations_list = [] # list to store number of iterations

time_list = [] # list to store time

for i in range(1, 101): # Looping to execute 100 iterations of tabu search
    a = i/100 #to calculate the frequency of iterations
    iterations_list.append(a) # appending the frequency to the iteration list

    time_start = time.time() # calculating the start time

    solution = tabu_search(instance, max_tries, max_flips)#calling the tabu_search function to obtain the solution for the given instance file

    time_list.append(time.time()-time_start) # appending the tiken taken for the program to search for the solution

    print(solution) # printing the solution for the instance

time_list.sort() # sorting the time_list

plot.plot(time_list,iterations_list) # plotting a graph of run-time and iterations

plot.xlabel("run-time in seconds")# value of x-label

plot.ylabel("P (solve)")# value of y-label

plot.title("Tabu Search for the instance uf20-021.cnf")#title of the graph

plot.show()   
                 
                   
                   
                   
               
               
               
