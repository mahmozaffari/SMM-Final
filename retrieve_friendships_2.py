import csv
import os, sys
import twitter
import json
import requests
import pickle
#from requests_oauthlib import OAuth1
import nltk
from twitter import Twitter, OAuth
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

os.chdir(".")
order = ['c40.txt','c20.txt']
# order = ['c1.txt']

def get_done_users(file):
    list = []
    if os.path.exists(file):
        f = codecs.open(file,'r')
        for line in f:
            if line.startswith('-user'):
                list.append(line[6:].strip())
        return list[0:-1]
    else:
        return []


for o in order:

    print('processing file {}'.format(o))
    file = os.path.join('./Data',o)
    with codecs.open(file,'r') as f:
        ids = f.read()
        id_list = list(filter(None,ids.split(',')))
        exclude_list = get_done_users(os.path.join('./Out',o))
        print('Excluding {} users'.format(len(exclude_list)))

        retrieve_list = [u for u in id_list if u not in exclude_list]

        retrieve_friends_ids(retrieve_list,os.path.join('./Out',o))


