import operator
import pickle
import pyfpgrowth
import json
from functools import reduce
from collections import Counter

n1 = 5
n2 = 2
n3 = 2
n4 = 4 # min suport
n5 = 3 # min suport for first five years
n6 = 4 # min suport for last six years

with open('data/dictionary.json', 'r') as f:
    dicts = json.load(f)

with open('data/data_transformed.json', 'r') as f:
    data = json.load(f)

# lines = open('data/FilteredDBLP.txt','r').read().splitlines()
# lines = lines[1:] + lines[0:1]

auth_dict = dicts[0]
conf_dict = dicts[1]
year_dict = dicts[2]

for i in range(len(data)):
    data[i].append(i)

# co_auths = []
# mat = [[[] for x in range(len(year_dict))] for y in range(len(conf_dict))]
# tmp = []
# i = 0
# j = 0
# c = 1

# for line in lines:
#     if line[0] == '#':
#         if i < 8:
#             tmp.sort()
#             mat[i][j] = mat[i][j] + tmp
#             co_auths.append(tmp)
#             tmp = []
#         continue
    
#     words = line.split('\t')
    
#     if words[0] == 'author':
#         if words[1] not in auth_dict:
#             auth_dict[words[1]] = c
#             c += 1
#         tmp.append(auth_dict[words[1]])
    
#     elif words[0] == 'year':
#         j = year_dict[words[1]]
#     elif words[0] == 'Conference':
#         w = words[1].split('@')[1] if '@' in words[1] else words[1] 
#         i = conf_dict[w] if w in conf_dict else 8

auth_dict_re = {}
conf_dict_re = {}

for k, v in auth_dict.items():
    auth_dict_re[v] = k

for k, v in conf_dict.items():
    conf_dict_re[v] = k

# print(c)

auths_by_year = [[{} for x in range(len(year_dict))] for y in range(len(conf_dict))]

for v in data:
    for a in v[0]:
        if a not in auths_by_year[v[1]][v[2]]:
            auths_by_year[v[1]][v[2]][a] = 1
        else:
            auths_by_year[v[1]][v[2]][a] += 1

auths = list(map(lambda x: reduce(lambda y,z: dict(Counter(y)+Counter(z)), x ), auths_by_year))

sorted_auths_by_year = list(map(lambda y: list(map(lambda x: sorted(x.items(), key=operator.itemgetter(1), reverse=True), y)), auths_by_year))

sorted_auths = list(map(lambda x: sorted(x.items(), key=operator.itemgetter(1), reverse=True), auths))


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

non_active = list(map(lambda x: list(filter(lambda y: y not in active_auths, x)), filter_auths))

def gen_out(x):
    out_dict = {}
    for i in range(len(x)):
        out_dict[conf_dict_re[i]] = list(map(lambda y: auth_dict_re[y[0]], x[i]))
        print(conf_dict_re[i], len(out_dict[conf_dict_re[i]]))
        
    return out_dict

print("all: ",)
out_suport = gen_out(filter_auths)
print("active: ",)
out_active = gen_out(active_auths)
print("non-active: ",)
out_non_active = gen_out(non_active)

#----group-----
def get_groups(x, n):
    co_auths = [y[0] for y in x]
    patterns = pyfpgrowth.find_frequent_patterns(co_auths, n)
    co_patterns = dict(filter(lambda x: len(x[0]) > 2, patterns.items()))
    co_patterns = sorted(co_patterns.items(), key = lambda x: len(x[0]), reverse=True)

    # remove duplicate
    pats = []
    def is_duplicate(a):
        for v in pats:
            if set(a) < v:
                return False
        pats.append(set(a))
        return True

    co_patterns = list(filter(lambda y: is_duplicate(y[0]), co_patterns))
    print(len(co_patterns))
    co_patterns = list(map(lambda y: list(y[0]), co_patterns))

    def get_details(a):
        tmp = []
        for v in x:
            if set(a) < set(v[0]):
                tmp.append(v[1:])
        return [a,tmp]

    co_patterns = list(map(lambda y: get_details(y), co_patterns))           
    return co_patterns

data_pre = list(filter(lambda x: x[2] < 5, data))
data_post = list(filter(lambda x: x[2] >= 5, data))

print("11 years groups number:",)
co_auths = get_groups(data, n4)
print("first five years groups number:",)
co_auths_pre = get_groups(data_pre, n5)
print("last six years groups number:",)
co_auths_post = get_groups(data_post, n6)

co_out = list(map(lambda x: list(map(lambda y: auth_dict_re[y], x[0])), co_auths))

# -----output------
with open('output/suport.json', 'w') as f:
    json.dump(out_suport, f)

with open('output/active.json', 'w') as f:
    json.dump(out_active, f)

with open('output/non_active.json', 'w') as f:
    json.dump(out_non_active, f)

with open('output/co_auths.json', 'w') as f:
    json.dump(co_auths, f)

with open('output/co_auths_pre.json', 'w') as f:
    json.dump(co_auths_pre, f)

with open('output/co_auths_post.json', 'w') as f:
    json.dump(co_auths_post, f)

with open('output/groups.json', 'w') as f:
    json.dump(co_out, f)

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

