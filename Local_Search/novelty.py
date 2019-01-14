import sys
import random
import collections
from collections import deque
from operator import itemgetter
import matplotlib.pyplot  as plot

source_directory = "" #path where the instance files are stored.
instance = []#list to store all the clauses of an instance 
no_of_variables = 0 # stores the number of variables present in each clause of the instance file
no_of_clauses = 0 # stores the number of clauses present in each instance file
max_iterations = 100000# the number of iterations
instance_file = open(source_directory + "/uf20-021.cnf", "r") # open and read the instance file
instance_file = instance_file.readlines()# read each line of the instance file
for line in range(len(instance_file)-3):#discarding the last 3 lines of the instance file and considering all the other lines
    if not (instance_file[line].lstrip().startswith('c') or instance_file[line].lstrip().startswith('p')):
    #if a line does not start with c or p then consider the line   
        a = instance_file[line].rstrip('0\n').split()# remove the 0 in the end of every clause
        instance.append(a)# append the clauses into the list
    if (instance_file[line].startswith('p')):# if a line starts with p then total number of variables and total number of clauses are obtained through that line
        no_of_variables = instance_file[line].split()[-2]# obtaining total number of variables
        no_of_clauses = instance_file[line].split()[-1]# obtaining total number of clauses
        
def flip(random_clause,instance,solution):# function to return the best and the second best or a random variable from an unsatisfied clause
    
    probability = random.uniform(0,1)# randomly selecting a probability
    try_solution = solution.copy()#creating a copy of the solution 

    if(probability > 0.4):# checking if the value of probability is greater than 0.4
        best_flip = {}#a dictionary to store the flipped variables is taken
        
       
        for variable in random_clause: #taking a loop for all the three variables of an unsatisfied random clause
           
            
            (try_solution[abs(int(variable))-1]) = (try_solution[abs(int(variable))-1]) * -1 #flipping the selected variable in the solution 
            
            unsatisfied = 0 # number of unsatisfied clauses is assigned as zero.
            
            for clauses1 in instance:# looping all the clauses in the instance file
                
                satisfiability = []#list assigned to store satisfied clauses
                
                for i in clauses1:# looping all the variables in a clause
                   
                    if(int(i) in try_solution):# checking if any of the variable in the clause matches any of the variable in the given solution
                     #that is if the value of variabe is true for the given solution
                        satisfiability.append(True)# if yes the clause is satisfied and appended as true in the satisfiability list 
                    else:# else the clause is unsatisfied and  appended as false in the satisfiability list 
                        satisfiability.append(False)
        
                if (True not in satisfiability):# all the false values of satisfiability list is taken
                    unsatisfied += 1 #storing the value of unsatisfied clauses 
                    
            best_flip.update({variable : unsatisfied})# update the dictionary with the variable and its number of unsatisfied clauses
        
            (try_solution[abs(int(variable))-1]) = (try_solution[abs(int(variable))-1]) * -1 # flipping the variable to its original value
            
          
        best_variable = sorted(best_flip.items(), key=itemgetter(1))# sorting the dictionary based on the number of unsatisfied clauses
        
        return best_variable[0][0],best_variable[1][0]#return the best and second best variable
    else:
        return [random_clause[random.randint(0,2)]]#return a random variable from unsatisfied clause
        
def novelty(instance, max_iterations):# perform novelty search
    
   solution = []# list to store the solution
   flipped_val = {}# dictionary to store flipped values
   
   for i in range(1,(int(no_of_variables)+1)):# looping the variables
     solution.append([-i,i][random.randrange(2)])#generating a random solution and storing it in the solution list
     
   for i in range(max_iterations):#loop in the range of maximum iterations
       
       unsatisfied_clause = 0 # variable to store unsatisfied clauses
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
           
           a = flip(random_clause,instance,solution)#getting the best variable and second best variable or random variable to flip
           
       if(len(a) == 1):# if a random variable is obtained flip it
          
         
           (solution[abs(int(a[0]))-1]) = (solution[abs(int(a[0]))-1]) * -1
       else:# else if best and second best variable is obtained
           if str(random_clause) in flipped_val:#if the random clause is present in the dictionary
               if abs(int(a[0])) == flipped_val[str(random_clause)]:#if the recently flipped variable of the given clause is the best variable
                   prob = random.uniform(0,1)#generate a random probability
                   if (prob <= 0.3):# if the random probability is less than equal to 0.03
                      (solution[abs(int(a[1]))-1]) = (solution[abs(int(a[1]))-1]) * -1# flip the second best variable in solution
                      flipped_val[str(random_clause)] = (abs(int(a[1])))# store the second best variable in the dictionary
                   else:
                      (solution[abs(int(a[0]))-1]) = (solution[abs(int(a[0]))-1]) * -1# flip the best variable in solution
                      flipped_val[str(random_clause)] = (abs(int(a[0])))# store the best variable in the dictionary
               else:#if the recently flipped variable of the given clause is not the best variable flip it and store it in the dictionary
                    (solution[abs(int(a[0]))-1]) = (solution[abs(int(a[0]))-1]) * -1
                    flipped_val[str(random_clause)] = (abs(int(a[0])))
               
           else:#if the random clause is not present in the dictionary flip thebest variable flip it and store it in the dictionary
               (solution[abs(int(a[0]))-1]) = (solution[abs(int(a[0]))-1]) * -1
               flipped_val[str(random_clause)] = (abs(int(a[0])))
               
   return "no solution found"# return no solution found if solution is not found
                
 
iterations_list = [] # list to store number of iterations

time_list = [] # list to store time

for i in range(1, 101): # Looping to execute 100 iterations of tabu search
    a = i/100 #to calculate the frequency of iterations
    iterations_list.append(a) # appending the frequency to the iteration list

    time_start = time.time() # calculating the start time

    solution = novelty(instance, max_iterations)#calling the novelty function to obtain the solution for the given instance file

    time_list.append(time.time()-time_start) # appending the tiken taken for the program to search for the solution

    print(solution) # printing the solution for the instance

time_list.sort() # sorting the time_list

plot.plot(time_list,iterations_list) # plotting a graph of run-time and iterations

plot.xlabel("run-time in seconds")# value of x-label

plot.ylabel("P (solve)")# value of y-label

plot.title("Novelty+ for the instance uf20-021.cnf")#title of the graph

plot.show()                  
                   
                   
                   
               
               
               
