import pandas
import string
import re
import math
from fuzzywuzzy import fuzz

data_frame = pandas.read_excel('manually_refined_set.xlsx')
data_frame = data_frame.fillna('')
data = [s.to_dict() for k, s in data_frame.iterrows()]

# extract gjaar
jaar_reg = re.compile('[0-9]{4}')

for d in data:
    d['year'] = []
    if d['Geboren']:
        try:
            year = int(d['Geboren'])
            d['year'] = year
            continue
        except:
            pass

        m = jaar_reg.match(d['Geboren'])

        if not m:
            continue

        try:
            year = int(m.group(0))
            d['year'] = year
        except:
            print('no convert')


'''
for d in data:
    print(d['year'])
'''

print(len(data))  # get a quick count of record_count

# generate new indexes.
for num in range(len(data)):
    data[num]['index'] = num  # can't do assignment in list comprehension.
    data[num]['naam_vol'] = ' '.join([data[num]['Roepnaam'], data[num]['Achternaam']])

yeared_data = [d for d in data if d['year']]

handled_indexes = []
last_index = 0
lookback = 5

def find_parent_candidates(you):
    ps = you['p1naam'], # , you['p2naam']  # roepnaam en achternaam
    global last_index

    parents = []
    for p1 in ps:
        data_subset = [d2 for d2 in yeared_data if (10 < you['year'] - d2['year'] < 70) and d2['index'] > last_index-lookback and d2['index'] < you['index']]
        sub_p = [(p1, d3['naam_vol'], fuzz.ratio(p1, d3['naam_vol']), d3) for d3 in data_subset]

        if not sub_p:
            continue

        m = max([frv for p1, d3, frv, tup in sub_p])
        if m < 100:
            # print('no likely candidate')
            continue
        candidates = [p for p in sub_p if p[2] == m]

        if len(candidates) >= 1:
            # print(len(candidates))
            candidates = [c for c in candidates if c[-1]['index'] not in handled_indexes[:-2]]
            # print(len(candidates))
            if len(candidates) == 0:
                # print('terminated at {}'.format(you['index']))
                continue

            set_maxes=[you['index'] - c[-1]['index'] for c in candidates if you['index'] - c[-1]['index'] > 0]
            # print(len(set_maxes))
            if len(set_maxes) == 0:
                continue
            m_l = max(set_maxes)  # furthest away (eldest non-processed)
            candidates = [p for p in candidates if (you['index'] - p[-1]['index']) == m_l]

            # now only one candidate lef
            if candidates[0][-1]['index'] not in handled_indexes:
                handled_indexes.append(candidates[0][-1]['index'])  # append index to index-list
            # print(handled_indexes)

            parents.append(candidates[0][-1])
            last_index = candidates[0][-1]['index']

    return parents




for kid in yeared_data[:]:
    parents = find_parent_candidates(kid)

    if parents:
        kid['p1index'] = parents[0]['index']
        if len(parents) == 2:
            kid['p2index'] = parents[1]['index']


out = pandas.DataFrame(yeared_data)
# out.to_excel('test.xlsx')

