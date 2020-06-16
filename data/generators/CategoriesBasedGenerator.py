# -*- coding: utf-8 -*-
""" Base inferface for categories-Based Sequence generator
    CategoriesModel should perform better for this generator
    TODO : parameter for transitions (determinist)
    TODO : locations with multiple categories
"""
import SequenceGenerator
import random
import ast
from numpy.random import choice

## TODO: add a parameter to tune the randomness of the transitions
class CategoriesBasedGenerator(SequenceGenerator.SequenceGenerator):

    def __init__(self, alphabet_size=100,categories_size=30, stop_prob=0.1):
        '''
            Parameters:
        	-----------
        	alphabet_size: int
        		Size of the underlying network use to generate the sequences
        	categories_size: int
        	    Size of the underlying network linked to the alphabet. alphabet_size > categories_size
        	stop_prob: float [0,1]
        		Probability to stop a sequence during its generation
        	'''
        self.alphabet_size = alphabet_size
        self.categories_size = categories_size
        self.locations = {}
        self.categories = []
        self.transitions = {}
        self.stop_prob = stop_prob
        self.generateLocations()
        self.generateTransitions()

    def generateLocations(self):

        for i in range(self.alphabet_size):
            self.locations[str(i)] = None
        for l in range(self.categories_size):
            self.categories.append('C'+str(l))

        #assign 1 time each categories randomly
        random_list = random.sample(self.locations, self.categories_size)
        for j in range(self.categories_size):
            self.locations[random_list[j]] = 'C'+str(j)

        #assigns each empty location left
        empty_location = [k for k, v in self.locations.iteritems() if v is None]
        for k in empty_location:
            self.locations[str(k)] = 'C'+ str(random.randint(0,self.categories_size-1))

    def generateTransitions(self):
        for k in range(0,self.categories_size):
            proba = ""
            #create a given number of probability which the sum equals to 1
            r = [random.random() for i in range(0,  self.categories_size)]
            s = sum(r)
            r = [i / s for i in r]
            for j in range(0,self.categories_size):
                if j == 0:
                    proba += '{ \'C' + str(j) + '\': ' + str(r[j]) + ', '
                elif j != self.categories_size-1:
                    proba +='\'C'+ str(j)+'\': '+str(r[j])+', '
                else :
                    proba+= '\'C'+ str(j)+'\': '+str(r[j])+'}'
            #convert the string dictionary into a real dictionary
			##TODO: directly compute the dict instead of using the literal_eval
			dict = ast.literal_eval(proba)
            self.transitions['C' + str(k)] = dict


    def nextSymbol(self, context=[]):
        '''
        Pick a locations according to the given 'context'
        2 possibilies:
            - empty context: a location picked at random
            - one previous locations: a location is chosen based on the previous category
        '''
        if len(context) == 0:
            nextSymbol = random.randint(0, self.alphabet_size - 1)
            return self.locations.keys()[nextSymbol]
        if len(context) == 1:
            pairs = self.transitions[context[0]]
            nextCat = choice(pairs.keys(), 1, p=pairs.values())
            nextLocation = []
            for k, v in self.locations.iteritems():
                if nextCat == v:
                    nextLocation.append(k)
            index = random.randint(0, len(nextLocation)-1 )
            return nextLocation[index]

        return -1

    def generate(self, nb_seq):
        '''
            The sequences generated are of size <= 2 * self.alphabet_size
        '''
        sequences = []
        for n in range(nb_seq):
            context = []
            seq = []
            stop = False
            while not stop:
                if len(context) == 0:
                    next_s = self.nextSymbol(context)
                else:
                    next_s = self.nextSymbol(context)
                seq.append(str(next_s))

                context = [ self.locations[next_s]]
                if (len(seq) > 2 and random.random() < self.stop_prob):
                    stop = True
                if len(seq) > 2. * self.alphabet_size:
                    stop = True
            sequences.append(seq)
        return sequences



# gen = CategoriesBasedGenerator(alphabet_size = 7, categories_size=4, stop_prob = 0.1)
# print gen.categories
# print gen.locations
# print gen.transitions
#
# sequences = gen.generate(5)
# for s in sequences:
# 	print s
