
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
def learning(func_table, base, context_lengths, training, testing, repeat):
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
    for i in range(repeat):
        for k, v in func_table.iteritems():
            result_func = base.copy()
            ##Get informations and train each model
            func, args, name = func_table[k]

            model = func(context_lengths, *args)
            for seq in training:
                model.learn(seq)

            func1 = EvalFunctions.averageProbNextSymbol(model, testing)
            func2 = EvalFunctions.averageProbAllSymbols(model, testing)

            print str(model)
            print "	probs averageProbNextSymbol: " + str(round(func1 * 100., 2))
            print "	probs averageProbAllSymbols: " + str(round(func2 * 100., 2))

            result_func.update({'model': name, 'k': context_lengths, 'score_1': str(round(func1 * 100., 2)), 'score_2': str(round(func2 * 100., 2))})
            result.append(result_func)
    return result



### PARAMETERS
### (Should list all variables for the experiments)
context_lengths = [1,2,3]
a_size = [100, 1000, 10000]         #Alphabet size
k_values = [3,5,7]                  #Average number of new connexion in the network
stop_prob = 0.1                     #Probability to stop a sequence
prob_return_node = 0.1              #Ratio of return node in the network
testing_ratio = 0.1                 #Sequence separation ratio
repeat = 20


result = []

values = list(itertools.product(context_lengths, a_size, k_values))

for i in values:
    base = collections.OrderedDict()
    base['model'] = None
    base['alphabet_size'] = i[1]
    base['stop_prob'] = stop_prob
    base['prob_return_node'] = prob_return_node
    base['k'] = None
    base['score_1'] = None
    base['score_2'] = None

    ## Generate datasets
    gen = HierarchicalReturnGenerator.HierarchicalReturnGenerator(alphabet_size=i[1], k=i[2], stop_prob=stop_prob, prob_return_node=prob_return_node)
    locations = gen.network

    sequences = gen.generate(400)
    sequences = DataModUtils.removeRepetitions(sequences)

    print "Nb Seqs : " + str(len(sequences))

    ### Get the unique list of symbols found in sequences
    alphabet = SeqStats.symbols(sequences)
    print "Nb Symbols : " + str(len(alphabet))

    ### Create Training/Testing subsets
    training, test_contexts, testing = [], [], []
    training, testing = DataModUtils.sampleSequences(sequences, testing_ratio)
    test_contexts = training

    func_table = {
        1: (PPMCModel.PPMCModel, [alphabet], "PPMC"),
        2: (ThereAndBackModel.ThereAndBackModel, [alphabet], "There And Back"),
        3: (HONModel.HONModel, [alphabet], "HON"),
        4: (FixOrderModel.FixOrderModel, [alphabet], "Fix Order"),
    }
    result.append(learning(func_table, base, i[0], training, testing, repeat))

##Write result in a file
path_seq_file = sys.path[0] + '/RES_Return_Generator.csv'
with open(path_seq_file, 'w') as seq_file:
    csv_writer = csv.DictWriter(seq_file, base.keys())
    csv_writer.writeheader()
    for i in result:
        for j in i:
            csv_writer.writerow(j)




