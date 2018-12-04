import csv
import os, sys
import twitter
import json
import requests
import pickle
# from requests_oauthlib import OAuth1
import nltk
from twitter import Twitter, OAuth
from load_tweets import parse_file
from collections import defaultdict
import urllib.parse
import time
import datetime
from collections import defaultdict
from twython import Twython, TwythonError
import codecs


users_file = 'repliers_id_and_counts.txt'

i = 0

user_ids = []
key = ''

if os.path.exists(users_file):
    print('load file')
    with open(users_file) as f:
        for line in f:
            user_ids.append(json.loads(line))
            i+=1
    print('{} users loaded into user_ids'.format(len(user_ids)))

else:
    with codecs.open('users.txt', 'rb',encoding='utf8') as f:
        for line in f:
            if not key == '':
                if key == 'id':
                    assert (line.startswith('v '))
                    u_id = line[2:].strip()
                    user['id'] = u_id
                    key = ''

                elif key == 'screen':
                    assert (line.startswith('v '))
                    name = line[2:].strip()
                    user['name'] = name
                    key = ''

                elif key == 'follow_count':
                    assert (line.startswith('v'))
                    count = int(line[2:].strip())
                    user['follower_count'] = count
                    key = ''

                elif key == 'friend_count':
                    assert (line.startswith('v'))
                    count = int(line[2:].strip())
                    user['friends_count'] = count
                    key = ''
            else:
                if line.startswith('f user<id'):
                    key = 'id'
                    user = defaultdict(str)
                elif line.startswith('f user<screen_name'):
                    key = 'screen'

                elif line.startswith('f user<followers_count'):
                    key = 'follow_count'

                elif line.startswith('f user<friends_count'):
                    key = 'friend_count'
                elif line.startswith('---'):
                    user_ids.append(user)

    print('{} users added to the list.'.format(len(user_ids)))

    with open(users_file, 'w') as f:
        j = 0
        for dic in user_ids:
            json.dump(dic, f)
            f.write("\n")
            j+=1

        print('{} lines were wrote to file.'.format(j))



# Sort users based on the friends count
#
sorted_user_ids = sorted(user_ids, key = lambda x: x['friends_count'],reverse=True)

# store only unique elements
unique_ids = set()
uique_entries = []
for d in sorted_user_ids:
    if not d['id'] in unique_ids:
        unique_ids.add(d['id'])
        uique_entries.append(d)


print('{} unique users'.format(len(uique_entries)))
print('{} dupplicates found'.format(len(user_ids)-len(uique_entries)))

limit_count = 5000

# retrieve users with less than 7500 friends:
for i in range(0,len(uique_entries)):
    if uique_entries[i]['friends_count'] <=limit_count:
        index = i
        break

higher_portion = uique_entries[0:index]
lower_portion = uique_entries[index:]

print('more than 5000 friends: {}'.format(len(higher_portion)))
print('less than 5000 friends: {}'.format(len(lower_portion)))

import matplotlib.pyplot as plt
# np.histogram([dic['friends_count'] for dic in sorted_user_ids], bins=10000)
plt.hist([dic['friends_count'] for dic in lower_portion], bins=100)  # arguments are passed to np.histogram
plt.title("Histogram with 'auto' bins")
plt.show()

from query_frineds_of_users import *
retrieve_friends_ids(lower_portion)
