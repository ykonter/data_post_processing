import pandas
import string
import re
import math

data_frame = pandas.read_excel('manually_refined_set.xlsx')
data_frame = data_frame.fillna('')
data = [s.to_dict() for k, s in data_frame.iterrows()]
print(len(data))  # get a quick count of record_count

# generate new indexes.
for num in range(len(data)):
    data[num]['index'] = num  # can't do assignment in list comprehension.


# read the txt file
f = open('pilo_stamboom_data.txt')
txt_data = f.read()
print(txt_data)
txt_data = filter(lambda x: x in string.printable, txt_data)
print(txt_data)

# loop through parents and find full names::
for blob in data[3:4]:

    print(blob)
    p = [blob['p1naam'], blob['p2naam']]
    p = [p_n for p_n in p if p_n]  # filter existing # and not math.isnan(p_n)
    print(p)

    for p_naam in p:
        # for every parent
        lf = p_naam.split()[0]
        print('looking for {}'.format(lf))
        regexp = re.compile(lf)
        info_lines = [(l_num, regexp.search(l), l) for l_num, l in enumerate(txt_data.splitlines()) if regexp.search(l)]
        print('*'*20)
        for info in info_lines:
            print(info)
        print('*' * 20)

