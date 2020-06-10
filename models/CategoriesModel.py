# -*- coding: utf-8 -*-
""" Base class for Symbols categories model
"""

import FixOrderModel

#TODO change to PredModel
class CategoriesModel(FixOrderModel.FixOrderModel):

    def __init__(self, maxContextLength, alphabet,  categories, seq, use_lprefix=True):
        super(CategoriesModel, self).__init__(maxContextLength, alphabet, use_lprefix)
        self.categories = categories
        self.seq = seq

    def __str__(self):
        return "Categories Model(" + str(self.maxContextLength) + ")"

    def learn(self, seq):
        super(CategoriesModel, self).learn(seq)

    def getCategory(self,symbol):
        for k, c in categories.iteritems():
            if symbol in c:
                return k

    def seqToCategoriesAndSymbols(self, seq, symbol):
        catSeq = []
        for i in seq:
            if i != symbol:
                catSeq.append(self.getCategory(i))
            else:
                catSeq.append(i)
        return catSeq

    def seqToCategories(self, seq):
        catSeq = []
        for i in seq:
                catSeq.append(self.getCategory(i))
        return catSeq

    def probability(self, symbol, context):
            #Model with categories and the given symbol
            catModel = CategoriesModel(3, categories.keys(), categories, seq)
            catSeq = self.seqToCategoriesAndSymbols(seq, symbol)
            catModel.learn(catSeq)

            #Model with only categories to count N(C(s))
            totModel = CategoriesModel(3, categories.keys(), categories, seq)
            totSeq = self.seqToCategories(seq)
            totModel.learn(totSeq)

            catContext = []
            for i in context:
                catContext.append(self.getCategory(i))

            context_node_cat = totModel.tree.longestPrefix(catContext)
            tot_count_n = context_node_cat.totalCount() + 0.
            context_node = catModel.tree.getNode(catContext)

            context_b = ''.join(context)
            #additional research of pattern, context of len = 1
            if len(context) == 1:
                if symbol == context_b:
                    res = catModel.tree.longestPrefix(context)
                    return (context_node[symbol] + res[symbol]) / tot_count_n
                elif self.getCategory(symbol) is self.getCategory(context[0]):
                    context_cpt = symbol
                    res = catModel.tree.longestPrefix(context_cpt)
                    return (context_node[symbol] + res[symbol]) / tot_count_n
            # context of len > 1
            else:
                if symbol in context:
                    nvContext = []
                    for i in context:
                        if i != symbol:
                            nvContext.append(self.getCategory(i))
                        else:
                            nvContext.append(i)
                    node = catModel.tree.longestPrefix(nvContext)
                    if context_node is not None and node[symbol] > context_node[symbol]:
                        return (node[symbol] +  context_node[symbol]) / tot_count_n
                    elif context_node is None and node[symbol] > context_node[symbol]:
                        return (node[symbol]) / tot_count_n
                #test solution
                # elif self.getCategory(symbol) in catContext:
                #     print "ici"
                #     nvContext = []
                #     print context
                #     for i in context:
                #         if self.getCategory(i) == self.getCategory(symbol):
                #             nvContext.append(symbol)
                #         else:
                #             nvContext.append(self.getCategory(i))
                #     print nvContext
                #     res_test = catModel.tree.longestPrefix(nvContext)
                #     return (res_test[symbol] + context_node[symbol]) / tot_count_n
            if  context_node is None:
                return 0
            else:
                return context_node[symbol] / tot_count_n



seq = 'aatccaagaatcg'
alphabet = ['a', 'c', 'g', 't']
categories = {'C1': ['a', 'c'], 'C2': ['g', 't']}

model = CategoriesModel(3, alphabet, categories, seq)
model.learn(seq)

print "Tree : "
print model.tree

context = ['g', 'a']    #bug
# context = ['a', 'a']   #bug should find 2/5 not 1/5 on a | a,a
# context = ['a']

for n in alphabet:
    ncontext = context[:]
    print n + " | " + ','.join(ncontext) + " : " + str(model.probability(n, ncontext))

# seq = 'abracadabra'
# alphabet = set(seq)
#
# alphabet = ['a','b','r','c','d']
# categories = {'C1': ['a','b', 'c'], 'C2': ['d', 'r']}
#
#
# model = CategoriesModel(3, alphabet, categories, seq)
# model.learn(seq)
#
# print seq
# print
#
# print "Tree : "
# print model.tree
#
# context = ['d', 'a']
# # context = ['r','a']
# # context = ['a']
#
#
# for n in alphabet:
# 	ncontext = context[:]
# 	print n + " | " + ','.join(ncontext) + " : " + str(model.probability(n,ncontext))
