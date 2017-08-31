import add_partner_data as pre_work
import util
import f_connect
from fuzzywuzzy import fuzz
import time

frame = pre_work.out  # prepare master data
nicer = pre_work.yeared_data

def dump_frame_to_firebase(input_frame):
    for i, data in input_frame.iterrows():
        d = util.cleanse_dict(data.to_dict())
        d['index'] = str(i)
        #f_connect.new_entry(d, "/people")
        f_connect.set(str(i), d, "/people")

def fetch_parent_lin(starting_index):
    global nicer

    p_index = nicer[starting_index]['p1index']
    print(p_index)

firebase_columns = ['Achternaam', 'Adres en huisnummer', 'Email', 'GeboorteLand', 'Geboren', 'Land', 'Plaats', 'Postcode', 'Roepnaam', 'Telefoonnummer', 'Voornamen' , 'index','lin', 'p1', 'p2']
frame = frame.rename(index=str, columns={"Achternaam": "Achternaam", "Geboorteland": "GeboorteLand", "Geboorteplaats": "Plaats", "naam_vol": 'Voornamen', "p1index": 'p1','p2index':'p2'})
print(frame.columns.values)

# dump_frame_to_firebase(frame)

frame['lineage']=''
fetch_parent_lin(0)

'''

for index, person in frame.iterrows():
    print('running for person {} where index is of type {}'.format(index, type(index)))
    all_lines = fetch_parent_lineage([[int(index)]])
    lens = [len(line) for line in all_lines]
    longest_ones = [line for line in all_lines if len(line) == max(lens)]
    chosen = []
    placed = False
    if len(longest_ones) == 1:  # one result
        chosen = list( reversed(longest_ones[0]))
        placed = True
    else:
        for long in longest_ones:
            if fuzz.ratio("Romer", frame.loc[long[-1]]) > 70:
                chosen = list(reversed(long))
                placed = True
                break
        # no match to romer, remains ambigious, choose any
    if not placed:
        chosen = list(reversed(longest_ones[0]))
    frame.set_value(index, 'lineage', chosen)

print(frame)
'''

'''
for i, vals in frame.iterrows():
    d = dict([(str(iter), str(val)) for iter, val in enumerate(vals['lineage'])])
    print(d)
    f_connect.set('lin', d, "/people/{}".format(i))
'''