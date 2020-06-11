# -*- coding: utf-8 -*-
""" Base class for Symbols categories model
"""

import FixOrderModel

class CategoriesModel(FixOrderModel.FixOrderModel):

    def __init__(self, maxContextLength, alphabet,  categories, use_lprefix=True):
        super(CategoriesModel, self).__init__(maxContextLength, alphabet, use_lprefix)
        self.categories = categories


    def __str__(self):
        return "Categories Model(" + str(self.maxContextLength) + ")"

    def learn(self, seq):
        """ Use to the sequence 'seq' to train the model
        		Parameters:
        		-----------
        		seq: list of str
        			The sequence of symbols to use
        		"""
        ## TODO this is a mess
        if len(seq) == 0:
            ## does nothing
            return
        if len(seq) == 1:
            ## only add seq[0] to the base counter
            self.tree.increment(seq[0], [])
            return
        if len(seq) <= self.maxContextLength:
            self.tree.increment(seq[0], [])
            for i in range(2, len(seq) + 1):
                cseq = seq[:i]
                self.tree.increment(cseq[-1], map(self.getCategory, cseq[:-1]))
        else:
            maxlength = self.maxContextLength
            self.tree.increment(seq[0], [])
            for i in range(2, maxlength + 1):
                cseq = seq[:i]
                self.tree.increment(cseq[-1], map(self.getCategory, cseq[:-1]))
            for i in range(len(seq) - maxlength):
                length = min(maxlength + 1, len(seq) - i)
                cseq = seq[i:i + length]
                self.tree.increment(cseq[-1], map(self.getCategory, cseq[:-1]))

    def getCategory(self,symbol):
        for k, c in self.categories.iteritems():
            if k == symbol:
                return c

    def seqToCategories(self, seq):
        catSeq = []
        for i in seq:
                catSeq.append(self.getCategory(i))
        return catSeq

    def probability(self, symbol, context):
        return super(CategoriesModel, self).probability(symbol,  map(self.getCategory, context))



# seq = 'aatccaagaatcg'
# alphabet = ['a', 'c', 'g', 't']
# categories = {'a': 'C1', 'c': 'C1', 'g': 'C2', 't': 'C2'}
#
#
# model = CategoriesModel(3, alphabet, categories)
# model.learn(seq)
#
# print "Tree : "
# print model.tree
#
# # context = ['g', 'a']
# context = ['a', 'a']
# # context = ['a']
#
# for n in alphabet:
#     ncontext = context[:]
#     print n + " | " + ','.join(ncontext) + " : " + str(model.probability(n, ncontext))

# seq = 'abracadabra'
# alphabet = set(seq)
#
# alphabet = ['a','b','r','c','d']
# categories = {'a': 'C1', 'b': 'C1', 'c': 'C1', 'd': 'C2', 'r': 'C2'}
#
#
# model = CategoriesModel(3, alphabet, categories)
# model.learn(seq)
#
# print seq
# print
#
# print "Tree : "
# print model.tree
#
# # context = ['d', 'a']
# context = ['a']
#
#
# for n in alphabet:
# 	ncontext = context[:]
# 	print n + " | " + ','.join(ncontext) + " : " + str(model.probability(n,ncontext))
