import operator
import pickle
import pyfpgrowth
from functools import reduce
from collections import Counter

lines = open('data/FilteredDBLP.txt','r').read().splitlines()
lines = lines[1:] + lines[0:1]

auth_dict = {}
conf_dict = {'IJCAI': 0, 'AAAI': 1, 'COLT': 2, 'CVPR': 3, 'NIPS': 4, 'KR': 5, 'SIGIR': 6, 'KDD': 7}
year_dict = {'2007': 0, '2008': 1, '2009': 2, '2010': 3, '2011': 4, '2012': 5, '2013': 6, '2014': 7, '2015': 8, '2016': 9, '2017': 10}

co_auths = []
mat = [[[] for x in range(len(year_dict))] for y in range(len(conf_dict))]
tmp = []
i = 0
j = 0
c = 1

for line in lines:
    if line[0] == '#':
        if i < 8:
            tmp.sort()
            mat[i][j] = mat[i][j] + tmp
            co_auths.append(tmp)
            tmp = []
        continue
    
    words = line.split('\t')
    
    if words[0] == 'author':
        if words[1] not in auth_dict:
            auth_dict[words[1]] = c
            c += 1
        tmp.append(auth_dict[words[1]])
    
    elif words[0] == 'year':
        j = year_dict[words[1]]
    elif words[0] == 'Conference':
        w = words[1].split('@')[1] if '@' in words[1] else words[1] 
        i = conf_dict[w] if w in conf_dict else 8

auth_dict_re = {}

for k, v in auth_dict.items():
    auth_dict_re[v] = k

print(c)

auths_by_year = [[{} for x in range(len(year_dict))] for y in range(len(conf_dict))]

for i in range(len(mat)):
    for j in range(len(mat[i])):
        for v in mat[i][j]:
            if v not in auths_by_year[i][j]:
                auths_by_year[i][j][v] = 1
            else:
                auths_by_year[i][j][v] += 1

auths = list(map(lambda x: reduce(lambda y,z: dict(Counter(y)+Counter(z)), x ), auths_by_year))

sorted_auths_by_year = list(map(lambda y: list(map(lambda x: sorted(x.items(), key=operator.itemgetter(1), reverse=True), y)), auths_by_year))

sorted_auths = list(map(lambda x: sorted(x.items(), key=operator.itemgetter(1), reverse=True), auths))

n1 = 10
n2 = 2
n3 = 5
n4 = 4

filter_auths = list(map(lambda x: list(filter(lambda y: y[1] > n1, x)), sorted_auths))

active_auths = []

for i in range(len(filter_auths)):
    tmp = []
    for v in filter_auths[i]:
        sum = 0
        for j in range(n2):
            k = len(year_dict) - j - 1
            sum += (auths_by_year[i][k][v[0]] if v[0] in auths_by_year[i][k] else 0)
        if sum > n3:
            tmp.append(v)
    active_auths.append(tmp)

patterns = pyfpgrowth.find_frequent_patterns(co_auths, n4)

co_patterns = dict(filter(lambda x: len(x[0]) > 1, patterns.items()))

co_patterns = sorted(co_patterns.items(), key = lambda x: len(x[0]), reverse=True)

# remove duplicate
pats = []

def is_duplicate(x):
    for v in pats:
        if set(x) < v:
            return False
    pats.append(set(x))
    return True

print(len(co_patterns))
co_patterns = list(filter(lambda x: is_duplicate(x[0]), co_patterns))


print(len(co_patterns))

# rules = pyfpgrowth.generate_association_rules(patterns, 0.7)

# print(rules)

# for i in range(len(conf)):
#     for v in conf[i]:
#         if v not in auths[i]:
#             auths[i][v] = 1
#         else:
#             auths[i][v] += 1



# print(len(sorted_auths))

# for i in range(len(sorted_auths_by_year[0])):
#     print(sorted_auths_by_year[0][i][:20])
#     print("#")

# for v in filter_auths:
#     print(v)
#     print("#")

# for v in active_auths:
#     print(v)
#     print("#")

# for i in range(len(active_auths)):
#     print(filter_auths[i])
#     print(active_auths[i])
#     print("#")

