from Inputs import authenticate
from credentials import *
from collections import defaultdict
import time
from collections import defaultdict
from datetime import datetime, timedelta
from email.utils import parsedate_tz
import glob
import codecs
from query_friends_of_users_2 import *
import csv

Main_users = {1:'Trump' ,2:'Obama',3:'VP',4:'Hillary Clinton',5:'Bill Clinton',6:'Doug Jones',7:'Michelle Obama'}

def check_by_user_lookup(u,r_f_list,client):

    url = 'https://api.twitter.com/1.1/users/lookup.json'
    param = {'user_id': u}
    response = client.get(url, params=param)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            data = data[0]
            count = data['friends_count']
            if count == len(r_f_list):
                return 'MATCH'

    elif response.status_code == 404:
        return 'NOT FOUND'
    else:
        return 'FAILED'

def produce_gephi_spreadshits(dic,target_nodes,u_to_p_dic):
#     Write nodes spreadshit
    global Main_users
    with open('MainNodes.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter = ',')
        writer.writerow(['Id','Label','Class'])
        for i,u in Main_users.items():
            writer.writerow([i,u,i])

    with open('Nodes.csv', 'w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Id','Label','Class'])

        for c,nodes in target_nodes.items():
            for n in nodes:
                writer.writerow([n,n,int(c[1:])])

    all_nodes = []
    for x,y in target_nodes.items():
        all_nodes.extend(y)
    all_nodes = list(set(all_nodes))


    with open('edges.csv', 'w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Source','Target','Type','Weight'])

        for c,d in dic.items():
            for u,f in d.items():
                for f_i in f:
                    if f_i in all_nodes:
                        writer.writerow([u,f_i,'Undirected',1])

    print('edges done')
    print('starting main edges')
    with open('MainEdges.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter = ',')
        writer.writerow(['Source','Target','Type','Weight'])

        for u,count_dic in u_to_p_dic.items():
            for i, count in count_dic.items():
                writer.writerow([u,i,'Undirected',count])


def main():
    print("here")

    target_users = {}       # list of the unique user, which we are interested in looking for the relationships between
    out_files = ['c1000.txt','c100.txt','c80.txt','c60.txt']#,'c80.txt','c60.txt','c40.txt']

    for f in out_files:
        f_path = os.path.join('./Data/',f)
        with codecs.open(f_path,'r') as fr:
            ids = fr.read()
            ids = list(filter(None, ids.split(',')))
            target_users[f[0:-4]]=list(set(ids))

    print('There is {} individual users in network.'.format(sum([len(u) for v, u in target_users.items()])))

    all_target_users = [ uu for v, u in target_users.items() for uu in u]

    dict_all = {}

    for f in out_files:
        dict_friends = defaultdict(list)

        f_path = os.path.join('./Out/',f)
        with codecs.open(f_path,'r') as fr:
            flag = False    # set true if line starts with -user ... (user id)
            for line in fr:
                if line.startswith('-user'):
                    if flag == True:
                        assert(line[6:].strip() == u_id)
                        continue
                    u_id = line[6:].strip()
                    flag = True
                elif line.startswith('----'):
                    flag = False
                    u_id = ''
                    friends_id_list = []
                else:
                    friends_id_list = line.strip().split(',')
                    dict_friends[u_id] = friends_id_list
                    flag = False
                    u_id = ''
                    friends_id_list = []

        dict_all[f[0:-4]] = dict_friends

    global Main_users
    user_to_politican_edges = {}
    file_path = os.path.join('./Data','user2politician.txt')
    line_i = 0
    with codecs.open(file_path,'r') as f:
        for line in f:
            if line_i==0:
                line_i += 1
                continue

            l = line.strip().split(',')
            u_id = l[0]
            if u_id in all_target_users:

                entry_dic = {}
                for i in range(1,len(l)):
                    if not int(float(l[i])) == 0:
                        entry_dic[i]=int(float(l[i]))

                user_to_politican_edges[u_id] = entry_dic


    print(len(user_to_politican_edges))

    produce_gephi_spreadshits(dict_all,target_users,user_to_politican_edges)

if __name__ == '__main__':
    main()