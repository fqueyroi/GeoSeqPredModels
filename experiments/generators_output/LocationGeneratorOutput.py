
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
import GeoFixOrderModel
import HONModel
import EvalFunctions

sys.path.append(''.join([os.path.dirname(__file__), '/../..', '/data/generators/']))
import LocationBasedGenerator


#train each models and return the results
def learning(func_table, base, min_k, max_k, len_test, training, testing):
    result = []
    for k, v in func_table.iteritems():
        result_func= dict.fromkeys(['model','k', 'score_1', 'score_2'])
        result_func.update(base)
        func, args, name = func_table[k]

        for i in range(min_k, max_k + 1):
            model = func(i, *args)
            for seq in training:
                model.learn(seq)

        func1 = EvalFunctions.averageProbNextSymbol(model, testing)
        func2 = EvalFunctions.averageProbAllSymbols(model, testing)

        print str(model)
        print "	probs averageProbNextSymbol: " + str(round(func1 * 100., 2))
        print "	probs averageProbAllSymbols: " + str(round(func2 * 100., 2))

        result_func.update({'model': name, 'k': len_test, 'score_1': str(round(func1 * 100., 2)), 'score_2': str(round(func2 * 100., 2))})
        result.append(result_func)
    return result


### PARAMETERS
### (Should list all variables for the experiments)
min_k = 1  ## minimum context length
max_k = [1,2,3]  ## maximum context length
len_test = 2
a_size = [100,1000]
gamma = [10**(-i) for i in range(4)]
stop_prob = 0.1
result = []

values =  list(itertools.product(max_k, a_size, gamma))

for i in values:
    base = {
        "alphabet_size": i[1],
        "stop_prob": stop_prob,
        "gamma": i[2]
    }
    ordered_dict = collections.OrderedDict()
    ordered_dict['model'] = None
    ordered_dict['alphabet_size'] = None
    ordered_dict['stop_prob'] = None
    ordered_dict['gamma'] = None
    ordered_dict['k'] = None
    ordered_dict['score_1'] = None
    ordered_dict['score_2'] = None

    ## Generate datasets
    dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.EUCLIDIAN]
    gen = LocationBasedGenerator.LocationBasedGenerator(alphabet_size=i[1], stop_prob=stop_prob, gamma=i[2])
    locations = gen.locations

    sequences = gen.generate(400)
    sequences = DataModUtils.removeRepetitions(sequences)

    print "Nb Seqs : " + str(len(sequences))

    ### Get the unique list of symbols found in sequences
    alphabet = SeqStats.symbols(sequences)
    print "Nb Symbols : " + str(len(alphabet))

    ### Create Training/Testing subsets
    training, test_contexts, testing = [], [], []
    training, testing = DataModUtils.cutEndOfSequences(sequences, len_test)
    test_contexts = training

    max_d = GeoFixOrderModel.getMaxDistance(locations, dist_fun)
    sum_d = GeoFixOrderModel.sumDensities(alphabet, locations, i[2], max_d, dist_fun)

    func_table = {
        1: (PPMCModel.PPMCModel, [alphabet], "PPMC"),
        2: (ThereAndBackModel.ThereAndBackModel, [alphabet], "There And Back"),
        3: (HONModel.HONModel, [alphabet], "HON"),
        4: (FixOrderModel.FixOrderModel, [alphabet], "Fix Order"),
    }

    result.append(learning(func_table, base,min_k, i[0], len_test, training, testing))

    for j in range(len(gamma)):
        func_table_geo = {
            1: (GeoFixOrderModel.GeoFixOrderModel, [alphabet, locations, gamma[j], dist_fun, max_d, sum_d, False],
                "GeoFix Order"),
            2: (GeoFixOrderModel.GeoFixOrderModel, [alphabet, locations, gamma[j], dist_fun, max_d, sum_d, True],
                "GeoFix Order Zero")
        }
        result.append(learning(func_table_geo, base, min_k, i[0], len_test, training, testing))

#write result in a file
path_seq_file = sys.path[0] + '/RES_Location_Generator.csv'
with open(path_seq_file, 'w') as seq_file:
    csv_writer = csv.DictWriter(seq_file, ordered_dict.keys())
    csv_writer.writeheader()
    for i in result:
        for j in i:
            csv_writer.writerow(j)




