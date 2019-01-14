import random
import math
import time
import operator

data = {}
solution = []
fitness = None

def readInstance(filename):
    """
   Function to read the instance file of TSP
    """
    global data
    source_directory = "" #path where the files are stored.
    file = open(source_directory + filename, 'r')#opening the file
    a = int(file.readline())#number of cities
    data = {}# dictionary to store city and its co-ordinates
    for line in file:#looping every line of the instance file
        (id, x, y) = line.split()
        data[int(id)] = (int(x), int(y))# storing city and its co-ordinates in the dictionary
    file.close()#closing the file
    return a,data# returning number of cities and data

def solution_generation(selection):
    
    if selection == "random":#if tour is equal to random
        random_sol = list(data.keys())#generate a random solution for cities
        random.shuffle(random_sol)#shuffle the random solution
        return random_sol# return the random solution
    
    elif selection == "nearest_neighbour":
        tour = list(data.keys()).copy() #creating a copy of cities list
        vCities = [] # list to store visited cities
        index = random.randint(0, len(tour)) # randomly selecting an index to select random city
        current = tour[index] # picking up a random city to start the tour
        vCities.append(current) # adding the current random city to the already visited cities list
        tour.pop(index) # removing starting city from unvisitedCities list
        
        while len(tour) > 0: # looping all the cities so that each one is visited
            distance = {} # dictionary to store distance between currect city and rest of the cities
            c = 0
            
            while c < len(tour):
                distance[tour[c]] = euclideanDistance(tour[c], current) # calculating distance between currect city and a given city
                c += 1
            
            nearest = min(distance.items(), key=operator.itemgetter(1))[0] #selecting a city with the least distance to the current city
            vCities.append(nearest) # adding the city with minimum distance city to the visited city list
            tour.pop(tour.index(nearest)) # popping out the minimum distance city from the unvisitedCities list
            current = nearest # making the minimum distance city as the current or recent city
        return vCities # returning the visited city list

def euclideanDistance(c1, c2):#function to calculate euclidean distance between two cities
    """
    Distance between two cities
    """
    d1 = data[c1]
    d2 = data[c2]
    return math.sqrt( (d1[0]-d2[0])**2 + (d1[1]-d2[1])**2 )# return the euclidean distance


def computeFitness(sol, a):# function to compute the fitness or cost
    """
    Computing the cost or fitness of the individual
    """
    fitness = euclideanDistance(sol[0], sol[len(sol)-1])# calculate the cost based on the euclidean distance between the first and the last city
    for i in range(0, a-1):# looping all the cities except the last city
        fitness += euclideanDistance(sol[i], sol[i+1])# incrementing the fitness
    return fitness

def local_search(solut, fitness,cities):
    """Function to perform 3-opt local search."""
    global solution #declaring solution as a global variable

    n = len(solut) # lenth of the solution
    a = random.randint(0, n)#a random edge is chosen from the solution
    
    for c in range(0, n):#looping in the length of solution
        
        if c==a: #if the chosen edge is equal to previously chosen edge choose a new edge
            continue
        
        e = c+1#the edge beside the second edge
        while e < n:# looping till the end of solution
            if e == c or e == a:#if the third edge matches the second or the first it is incremented by 1 
                e += 1
                continue
            
            a, c, e = sorted([a, c, e])# all three edges are sorted
            b, d, f = a+1, c+1, e+1#b,d and f edges are the adjacent edges to a,c and e
        
            sol = solut[:a+1] + solut[b:c+1]    + solut[d:e+1]    + solut[f:] # this is the identity combination
            fit = computeFitness(sol, cities)# the cost of the combination is calculated
            if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
                solution = sol# the solution is replaced by the recently calculated solution
                fitness = fit#cost is replaced by recently calculated cost
                
            sol = solut[:a+1] + solut[b:c+1]    + solut[e:d-1:-1] + solut[f:] #this is the combination for 2-opt
            fit = computeFitness(sol, cities)# the cost of the combination is calculated
            if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
                solution = sol# the solution is replaced by the recently calculated solution
                fitness = fit#cost is replaced by recently calculated cost
                
            sol = solut[:a+1] + solut[c:b-1:-1] + solut[d:e+1]    + solut[f:] #this is the combination for 2-opt
            fit = computeFitness(sol, cities)# the cost of the combination is calculated
            if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
                solution = sol# the solution is replaced by the recently calculated solution
                fitness = fit#cost is replaced by recently calculated cost
            
            sol = solut[:a+1] + solut[c:b-1:-1] + solut[e:d-1:-1] + solut[f:] #this is the combination for 3-opt
            fit = computeFitness(sol, cities)# the cost of the combination is calculated
            if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
                solution = sol# the solution is replaced by the recently calculated solution
                fitness = fit#cost is replaced by recently calculated cost
            
            sol = solut[:a+1] + solut[d:e+1]    + solut[b:c+1]    + solut[f:] #this is the combination for 3-opt
            fit = computeFitness(sol, cities)# the cost of the combination is calculated
            if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
                solution = sol# the solution is replaced by the recently calculated solution
                fitness = fit#cost is replaced by recently calculated cost
                
            sol = solut[:a+1] + solut[d:e+1]    + solut[c:b-1:-1] + solut[f:] #this is the combination for 3-opt
            fit = computeFitness(sol, cities)# the cost of the combination is calculated
            if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
                solution = sol# the solution is replaced by the recently calculated solution
                fitness = fit#cost is replaced by recently calculated cost
                
            sol = solut[:a+1] + solut[e:d-1:-1] + solut[b:c+1]    + solut[f:] #this is the combination for 3-opt
            fit = computeFitness(sol, cities)# the cost of the combination is calculated
            if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
                solution = sol# the solution is replaced by the recently calculated solution
                fitness = fit#cost is replaced by recently calculated cost
                
            sol = solut[:a+1] + solut[e:d-1:-1] + solut[c:b-1:-1] + solut[f:]  #this is the combination for 2-opt
            fit = computeFitness(sol, cities)# the cost of the combination is calculated
            if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
                solution = sol# the solution is replaced by the recently calculated solution
                fitness = fit#cost is replaced by recently calculated cost
            e += 1#increment the value of the third edge
            
    return solution,fitness# return the solution and cost

def perturbation(solut,fitness,cities):
    for i in range(5):#looping in the range of 5
        n = len(solut)# length of solution
        a, b = random.sample(range(n+1), 2)# randomly picking two edges

    
        global solution

        sol = solut[:a+1] + solut[b:a:-1]  + solut[b+1:] # this is the combination for identity
        fit = computeFitness(sol, cities)# the cost of the combination is calculated
        if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
            solution = sol# the solution is replaced by the recently calculated solution
            fitness = fit#cost is replaced by recently calculated cost
            
        sol = solut[:a+1] + solut[a+1:b+1]    + solut[b+1:]  #this is the combination for 2-opt
        fit = computeFitness(sol, cities)# the cost of the combination is calculated
        if (fit< fitness):#if the cost of the solution is less than the previously calculated cost
            solution = sol# the solution is replaced by the recently calculated solution
            fitness = fit#cost is replaced by recently calculated cost
    
    return solution, fitness# return the solution and cost

def acceptance_criterion(loc_sol,loc_fit,loc_sol1,loc_fit1):
    probability = random.randint(0,20)#generating a random probability
    prob = probability/20#calculating the probability
    
    if(prob == 0.05):# if the probability is equal to 0.05
    
        return loc_sol1,loc_fit1# return the cost and solution obtained through local search after perturbation
 
    else:
     
        if(loc_fit < loc_fit1):# if the cost of local search before perturbation is less than local search after perturbation
            solution = loc_sol# replace the solution and the cost
            fitness = loc_fit
            return solution, fitness# return the cost and solution obtained through local search before perturbation
            
        else:# else replace the solution and cost of local search after perturbation
            solution = loc_sol1
            fitness = loc_fit1
            return solution, fitness# return the cost and solution obtained through local search after perturbation

if __name__ == "__main__":#main function

    files = ["inst-0.tsp",'inst-13.tsp']# all the instance files 
    heuristic = ["random","nearest_neighbour"]# list containg the heuristic approach names
    
    for file in files:
        cities,data =  readInstance(file)#obtaining the cities and data dictionary
       
        for i in range(0, 2):
            solution = solution_generation(heuristic[i])# obtaining the solution through heuristic method selected
            
            for iteration in range(0, 5):# looping for 5 iterations
                print("Heuristic : ",heuristic[i],"instance : ", file, "iteration : ", iteration)
                fitness = computeFitness(solution, cities)#obtaining the cost through computeFitness function
                print("Original Cost : ",fitness)#print the original cost
                loc_sol,loc_fit = local_search(solution, fitness, cities)#solution and cost are obtained before perturbation for local search
                t_end = time.time() + 60 * 5#the end time is selected as 5 minutes
                
                while time.time() < t_end:#the loop is run for 5 minutes
                   per_sol,per_fit = perturbation(loc_sol,loc_fit,cities)#solution and cost are obtained for perturbation function
                   loc_sol1,loc_fit1 = local_search(per_sol,per_fit,cities)#solution and cost are obtained after perturbation for local search
                   loc_sol,loc_fit = acceptance_criterion(loc_sol,loc_fit,loc_sol1,loc_fit1)#solution and cost are obtained for acceptance criterion

                print("Updated Cost", loc_fit)# to print the updated cost