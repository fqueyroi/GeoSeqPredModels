# -*- coding: utf-8 -*-
""" Base class for Symbols categories model
"""

import FixOrderModel

class CategoriesAndSymbolModel(FixOrderModel.FixOrderModel):

    def __init__(self, maxContextLength, alphabet,  categories, use_lprefix=True):
        super(CategoriesAndSymbolModel, self).__init__(maxContextLength, alphabet, use_lprefix)
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
                context = [self.categories[s] for s in cseq[:-2]]
                context.append(cseq[-2])
                self.tree.increment(cseq[-1], context)
        else:
            maxlength = self.maxContextLength
            self.tree.increment(seq[0], [])
            for i in range(2, maxlength + 1):
                cseq = seq[:i]
                context = [self.categories[s] for s in cseq[:-2]]
                context.append(cseq[-2])
                self.tree.increment(cseq[-1],  context)
            for i in range(len(seq) - maxlength):
                length = min(maxlength + 1, len(seq) - i)
                cseq = seq[i:i + length]
                context = [self.categories[s] for s in cseq[:-2]]
                context.append(cseq[-2])
                self.tree.increment(cseq[-1],  context)

    def probability(self, symbol, context):
        if len(context) == 1:
            return super(CategoriesAndSymbolModel, self).probability(symbol, context)
        else:
            cat_context = [self.categories[s] for s in context[:-1]]
            cat_context.append(context[-1])
            return super(CategoriesAndSymbolModel, self).probability(symbol, cat_context)


# seq = 'abracadabra'
# alphabet = set(seq)
#
# alphabet = ['a','b','r','c','d']
# categories = {'a': 'C1', 'b': 'C1', 'c': 'C1', 'd': 'C2', 'r': 'C2'}
#
#
# model = CategoriesAndSymbolModel(3, alphabet, categories)
# model.learn(seq)
#
# print seq
# print
#
# print "Tree : "
# print model.tree
#
# # context = ['a', 'b']
# context = ['a']
#
#
# for n in alphabet:
# 	ncontext = context[:]
# 	print n + " | " + ','.join(ncontext) + " : " + str(model.probability(n,ncontext))
