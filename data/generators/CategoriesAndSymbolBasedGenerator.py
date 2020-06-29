# -*- coding: utf-8 -*-
""" Base inferface for categories-Based Sequence generator
    CategoriesModel should perform better for this generator
    TODO : parameter for transitions (determinist)
    TODO : locations with multiple categories
"""
import SequenceGenerator
import random
import numpy
from numpy.random import choice

## TODO: add a parameter to tune the randomness of the transitions
class CategoriesAndSymbolBasedGenerator(SequenceGenerator.SequenceGenerator):

    def __init__(self, alphabet_size=100,categories_size=30, stop_prob=0.1, alpha=0.5):
        '''
            Parameters:
        	-----------
        	alphabet_size: int
        		Size of the underlying network use to generate the sequences
        	categories_size: int
        	    Size of the underlying network linked to the alphabet. alphabet_size > categories_size
        	stop_prob: float [0,1]
        		Probability to stop a sequence during its generation
        	alpha
        	    Parameter of the transitions randomness if alpha=1 uniform transitions
        	'''
        self.alphabet_size = alphabet_size
        self.categories_size = categories_size
        self.locations = {}
        self.categories = []
        self.transitions = {}
        self.stop_prob = stop_prob
        self.alpha = alpha
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
        alpha = [self.alpha for i in range(self.alphabet_size)]
        for j in range(self.categories_size):
            for k in range(self.alphabet_size):
                r = numpy.random.dirichlet(alpha)
                # transitions =  dict(zip(self.locations, r))
                ## speed-up by removing low probability
                thres = 1. / (4.*self.alphabet_size)
                r = [x for x in r if x > thres]
                to_loc = random.sample(self.locations.keys(),len(r))
                transitions =  dict(zip(to_loc, r / sum(r)))
                self.transitions[('C' + str(j), str(k))] = transitions

    def nextSymbol(self, context=[]):
        '''
        Pick a locations according to the given 'context'
        2 possibilies:
            - empty context: a location picked at random
            - one previous locations: a location is chosen based on the previous category
        '''
        if len(context) < 2:
            return random.choice(self.locations.keys())
        else:
            pairs = self.transitions[(context[0], context[1])]
            nextLoc = choice(pairs.keys(), 1, p=pairs.values())
            return nextLoc[0]

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
                next_s = self.nextSymbol(context)
                seq.append(str(next_s))
                if len(seq)<2:
                    context = [ self.locations[next_s]]
                else:
                    context = [self.locations[seq[-2]],seq[-1]]
                if (len(seq) > 2 and random.random() < self.stop_prob):
                    stop = True
                if len(seq) > 2. * self.alphabet_size:
                    stop = True
            sequences.append(seq)
        return sequences


# import time
# start_time = time.time()
# gen = CategoriesAndSymbolBasedGenerator(alphabet_size = 2500, categories_size=41, stop_prob = 0.1, alpha=0.2)
# print "Init time: " + str(time.time() - start_time)
# print gen.categories
# print gen.locations
# print gen.transitions
# start_time = time.time()
# sequences = gen.generate(1000)
# print "Gen time: " + str(time.time() - start_time)
# for s in sequences:
# 	print s
