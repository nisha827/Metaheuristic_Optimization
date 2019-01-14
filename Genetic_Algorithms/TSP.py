import random
from Individual import *
import sys
import time

class BasicTSP:
    def __init__(self, _fName, _popSize, _mutationRate, _maxIterations):
        """
        Parameters and general variables
        """

        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = _popSize
        self.genSize        = None
        self.mutationRate   = _mutationRate
        self.maxIterations  = _maxIterations
        self.iteration      = 0
        self.fName          = _fName
        self.data           = {}

        self.readInstance()
        self.initPopulation()


    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (id, x, y) = line.split()
            self.data[int(id)] = (int(x), int(y))
        file.close()

    def initPopulation(self):
        """
        Creating random individuals in the population
        """
        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data)
            individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        print ("Best initial sol: ",self.best.getFitness())

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
            print ("iteration: ",self.iteration, "best: ",self.best.getFitness())

    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.popSize-1) ]
        indB = self.matingPool[ random.randint(0, self.popSize-1) ]
        return [indA, indB]
    
    def twoBestIndividuals(self):
        twoBestInd = []
        fitnessList = []
        for i in range(0, self.popSize -1):
            fitnessList.append(self.matingPool[i].getFitness())

        fitnessList.sort()

        for i in range(0,2):
            for j in range(0, self.popSize -1):
                if self.matingPool[j].getFitness() == fitnessList[i] and len(twoBestInd)<2:
                    twoBestInd.append(self.matingPool[j])
        #print(twoBestInd)
        return twoBestInd

    def rouletteWheel(self):
        """
        Your Roulette Wheel Selection Implementation
        """
        
        parents = []
        rand = random.random()
        probSum = 0
        subProbSum = 0
        
        for i in range(0, self.popSize-1):
            probSum = probSum + self.matingPool[i].getFitness()
        
        for j in range(0, self.popSize-1):
            a = self.matingPool[j].getFitness()/probSum
            subProbSum = subProbSum + a
            if rand < subProbSum:
                while len(parents) < 2:
                    parents.append(self.population[j])
        
        return parents

    def uniformCrossover(self, indA, indB):
        """
        Your Uniform Crossover Implementation
        """
        c=[]
        index = []
        value = []
        child = indA.genes.copy()

        for i in range(len(indA.genes)):
            c.append(random.randint(0,1))
            
        for  i in range(len(child)):
            if c[i] == 1:
                child[i] = None
                index.append(i)
            
        for j in range(len(indB.genes)):
            if indB.genes[j] not in child:
                value.append(indB.genes[j])
            
        for i,j in zip(index, value):
            child[i] = j
        
        return(child)

    def cycleCrossover(self, indA, indB):
        """
        Your Cycle Crossover Implementation
        """
        #c=[None,None,None,None,None,None,None]
        #index = []
        #value = []
        child = indA.genes.copy()
        l = 0
        child[0] = indA.genes[0]
        for i in range(len(indA.genes)):
            if indB.genes[i] not in child:
                j=i
                while j<len(indB.genes):
                    if indB.genes[j] not in child and l%2 == 0:
                        ind = indA.genes.index(indB.genes[j])
                        child[ind] = indA.genes[ind]
                        j=ind
                        print(j)
                #index[i].append(j)
                    elif indB.genes[j] not in child and l%2 != 0:
                        ind = indA.genes.index(indB.genes[j])
                        child[j] = indB.genes[j]
                        j=ind
                    elif indB.genes[j] in child:
                        break
                l = l + 1
            if indA.genes in child:
                break
        return child
    
    def reciprocalExchangeMutation(self, ind):
        """
        Your Reciprocal Exchange Mutation implementation
        """
        if random.random() > self.mutationRate:
            return
        A = random.randint(0, self.genSize-1)
        B = random.randint(0, self.genSize-1)

     # exchanging the values at random indexes obtained at A and B above
        temp = ind.genes[A]
        ind.genes[A] = ind.genes[B]
        ind.genes[B] = temp

        ind.computeFitness()
        self.updateBest(ind)

    def scrambleMutation(self, ind):
        """
        Your Scramble Mutation implementation
        """
        if random.random() > self.mutationRate:
            return
        a = random.randint(0, self.genSize-1)
        b = random.randint(0, self.genSize-1)

        while(a>=b):
            a = random.randint(0, self.genSize-1)
            b = random.randint(0, self.genSize-1)
        
        v = []
        [v.append(ind.genes[i]) for i in range(a,b)] #step 1
    
        random.shuffle(v)  #step 2
    
        for j in range(a,b):
            ind.genes.remove(ind.genes[j])  #step 3
            ind.genes.insert(j,v[j-a]) #step 4    #j-a since the part to be shuffled begins from this index of list
        
        ind.computeFitness()
        self.updateBest(ind)

    def crossover(self, indA, indB):
        """
        Executes a 1 order crossover and returns a new individual
        """
        child = []
        tmp = {}

        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        for i in range(0, self.genSize):
            if i >= min(indexA, indexB) and i <= max(indexA, indexB):
                tmp[indA.genes[i]] = False
            else:
                tmp[indA.genes[i]] = True
        aux = []
        for i in range(0, self.genSize):
            if not tmp[indB.genes[i]]:
                child.append(indB.genes[i])
            else:
                aux.append(indB.genes[i])
        child += aux
        return child

    def mutation(self, ind):
        """
        Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

        ind.computeFitness()
        self.updateBest(ind)

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation
        """
        self.matingPool = []
        for ind_i in self.population:
            self.matingPool.append( ind_i.copy() )

    def newGeneration(self, configuration):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """
        for i in range(0, len(self.population)):
            """
            Depending of your experiment you need to use the most suitable algorithms for:
            1. Select two candidates
            2. Apply Crossover
            3. Apply Mutation
            """
            if configuration == 1:
                [ind1, ind2] = self.randomSelection()
                child = self.uniformCrossover(ind1, ind2)
                self.population[i].setGene(child)
                self.reciprocalExchangeMutation(self.population[i])
                
            if configuration == 2:
                [ind1, ind2] = self.randomSelection()
                child = self.cycleCrossover(ind1, ind2)
                self.population[i].setGene(child)
                self.scrambleMutation(self.population[i])
                
            if configuration == 3:
                [ind1, ind2] = self.rouletteWheel()
                child = self.uniformCrossover(ind1, ind2)
                self.population[i].setGene(child)
                self.reciprocalExchangeMutation(self.population[i])
                
            if configuration == 4:
                [ind1, ind2] = self.rouletteWheel()
                child = self.cycleCrossover(ind1, ind2)
                self.population[i].setGene(child)
                self.reciprocalExchangeMutation(self.population[i])
                
            if configuration == 5:
                [ind1, ind2] = self.rouletteWheel()
                child = self.cycleCrossover(ind1, ind2)
                self.population[i].setGene(child)
                self.scrambleMutation(self.population[i])
                
            if configuration == 6:
                [ind1, ind2] = self.twoBestIndividuals()
                child = self.uniformCrossover(ind1, ind2)
                self.population[i].setGene(child)
                self.scrambleMutation(self.population[i])
                
    def GAStep(self, config):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        self.updateMatingPool()
        self.newGeneration(config)

    def search(self, config):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep(config)
            self.iteration += 1

        print ("Total iterations: ",self.iteration)
        print ("Best Solution: ", self.best.getFitness())

if len(sys.argv) == 1:
    files = ["inst-0.tsp","inst-13.tsp","inst-16.tsp"]
    for problem_file in files:
        for configuration in (1,7):
            for test in range(1,4):
                ga = BasicTSP(problem_file, 100, 0.1, 300)
                startTime = time.time()
                ga.search(configuration)
                endTime = (time.time()-startTime)/60
                print("problem_file:",problem_file,"Configuration:",configuration,"test:",test,"Time taken:",endTime)
                del ga
    sys.exit(0)