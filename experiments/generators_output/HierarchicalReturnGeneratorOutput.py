
import sys, os
import itertools
import collections
sys.path.append(''.join([os.path.dirname(__file__), '/..']))
import DataModUtils
import SeqStats
import csv

sys.path.append(''.join([os.path.dirname(__file__), '/../..', '/models/']))
import PPMCModel
import FixOrderModel
import ThereAndBackModel
import HONModel
import EvalFunctions

sys.path.append(''.join([os.path.dirname(__file__), '/../..', '/data/generators/']))
import HierarchicalReturnGenerator

#train each models and return the results
def learning(func_table, base, context_lengths, training, testing):
    '''
    Parameters:
    -----------
    func_table:
        table with the models
    base:
        dictionary with all test informations by model

    :return: completed dictionary
    '''
    result = []
    for k, v in func_table.iteritems():
        ##Get informations and train each model
        func, args, name = func_table[k]

        for context in context_lengths:
            model = func(context, *args)
            for seq in training:
                model.learn(seq)
            if name == "HON":
                model.prune()

            func1 = EvalFunctions.averageProbNextSymbol(model, testing)
            func2 = EvalFunctions.averageProbAllSymbols(model, testing)

            # print str(model)
            # print "	probs averageProbNextSymbol: " + str(round(func1 * 100., 2))
            # print "	probs averageProbAllSymbols: " + str(round(func2 * 100., 2))

            result_func = base.copy()
            result_func.update({'model': name, 'context': context,
                'size' : model.size(), 'score_1': str(round(func1 * 100., 2)),
                'score_2': str(round(func2 * 100., 2))})
            result.append(result_func)
    return result



### PARAMETERS
### (Should list all variables for the experiments)
context_lengths = [1,2]
a_size = [100,800,2000]         #Alphabet size
k_values = [3]                  #Average number of new connexion in the network
stop_prob = 0.1                     #Probability to stop a sequence
prob_return_node = [0.01,0.1,0.3]             #Ratio of return node in the network
testing_ratio = 0.1                 #Sequence separation ratio
repeat = 20


result = []

values = list(itertools.product(a_size, k_values, prob_return_node))

for i in values:
    for j in range(repeat):
        base = collections.OrderedDict()
        base['model'] = None
        base['alphabet_size'] = i[0]
        base['connect'] = i[1]
        base['stop_prob'] = stop_prob
        base['prob_return_node'] = i[2]
        base['context'] = None
        base['size']    = None
        base['score_1'] = None
        base['score_2'] = None

        ## Generate datasets
        gen = HierarchicalReturnGenerator.HierarchicalReturnGenerator(alphabet_size=i[0],
            k=i[1], stop_prob=stop_prob, prob_return_node=i[2])
        locations = gen.network

        sequences = gen.generate(1000)
        sequences = DataModUtils.removeRepetitions(sequences)

        # print "Nb Seqs : " + str(len(sequences))

        ### Get the unique list of symbols found in sequences
        alphabet = SeqStats.symbols(sequences)
        # print "Nb Symbols : " + str(len(alphabet))
        base['nb_symbols'] = len(alphabet)
        ### Create Training/Testing subsets
        training, testing = [], []
        training, testing = DataModUtils.sampleSequences(sequences, testing_ratio)

        func_table = {
            1: (PPMCModel.PPMCModel, [alphabet], "PPMC"),
            2: (ThereAndBackModel.ThereAndBackModel, [alphabet], "There And Back"),
            3: (HONModel.HONModel, [alphabet], "HON"),
            4: (FixOrderModel.FixOrderModel, [alphabet], "Fix Order"),
        }
        result.append(learning(func_table, base, context_lengths, training, testing))

##Write result in a file
path_seq_file = sys.path[0] + '/RES_Return_Generator.csv'
with open(path_seq_file, 'w') as seq_file:
    csv_writer = csv.DictWriter(seq_file, base.keys())
    csv_writer.writeheader()
    for i in result:
        for j in i:
            csv_writer.writerow(j)
