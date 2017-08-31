import add_partner_data as pre_work
import util
import f_connect

frame = pre_work.out  # prepare master data
nicer = pre_work.yeared_data

def fetch_parent_lin(starting_index):

    global nicer

    lin = [starting_index]
    print(lin)

    for i in range(100):

        #for n in nicer:
        #    if 'p1inde' in n:
        #        print('we are a go')

        me_data = [n for n in nicer if n['index'] == lin[-1]][0]  # found myself and all my data
        if 'p1index' in me_data :
            lin.append(me_data['p1index'])
        else:
            return lin

    return lin




if __name__ == '__main__':

    for i in nicer:
        print(i['index'])
        d = fetch_parent_lin(i['index'])
        print(i['index'], d)
        d = dict((i, v) for i, v in enumerate(reversed(d)))
        print(i['index'], d)
        f_connect.set('lin', d, "/people/{}".format(i['index']))
