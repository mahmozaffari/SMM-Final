# clone edited
import csv
import os, sys
import twitter
import json
import requests
import pickle
#from requests_oauthlib import OAuth1
import nltk
from twitter import Twitter, OAuth
from Inputs import my_credsa, my_credsb, famous_list, read_famous_list, authenticate, common_features, file_delimeter, feature_processing, recorded
from load_tweets import parse_file
from collections import defaultdict
import urllib.parse
import time
import datetime
from collections import defaultdict
from twython import Twython, TwythonError
from remove_entities import clean_text

# --------------------------

url = 'https://api.twitter.com/1.1/search/tweets.json'

# --------------------------

def main():

	# python3 extract2.py partiesb.txt output/Dems_stats.txt
	# python3 extract2.py partiesa.txt output/Reps_stats.txt


	uuniques = defaultdict(int)
	user_file = open('users.txt')
	users,cu,uu, uuniques = parse_file(user_file,uuniques,'users')
	user_dict = defaultdict(int)
	for u in range(0,len(users)-1):
        	uid = users[u].features['user<id']
	        if len(uid)>0:
        	        user_dict[uid[0]] = u


	CONSUMER_KEY = my_credsb['CONSUMER_KEY']
	CONSUMER_SECRET = my_credsb['CONSUMER_SECRET']
	OAUTH_TOKEN = my_credsb['TOKEN_KEY']
	OAUTH_TOKEN_SECRET = my_credsb['TOKEN_SECRET']

	twitter_twy = Twython(CONSUMER_KEY, CONSUMER_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	li = sequences[y]
	tweets = twitter_twy.lookup_status(id = li)
	#tweets = twitter_twy.lookup_status(id_str = '551763146877452288')


	'''level = 2
	args = sys.argv[1:]
	ids = read_dataset()
	my_creds = my_credsa
	run_party(ids[0:2],my_creds,level)'''


if __name__ == '__main__':
	main()



