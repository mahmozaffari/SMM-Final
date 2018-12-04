import csv
import os, sys
import twitter
import json
import requests
import pickle
#from requests_oauthlib import OAuth1
import nltk
from twitter import Twitter, OAuth
# from Inputs import my_credsa, my_credsb, famous_list, read_famous_list, authenticate, common_features, file_delimeter, feature_processing, recorded
from Inputs import authenticate
from credentials import *
from collections import defaultdict
import time
from collections import defaultdict
from datetime import datetime, timedelta
from email.utils import parsedate_tz


def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])

url = 'https://stream.twitter.com/1.1/statuses/filter.json'
userlookup_url = 'https://api.twitter.com/1.1/users/lookup.json'


def get_list_of_users(users_file):
	f = open(users_file, 'rb')
	users_to_follow = []
	for line in f:
		users_to_follow.append(line[1:].strip().decode('utf-8'))
	print(users_to_follow)
	f.close()
	return users_to_follow


def lookup_users(usernames,client):
	# looks up the users in 'usernames' by screen name and retrieves the id
	# Returns a dictionary of screen_name and id

	users = defaultdict(str)
	print(usernames)
	screen_name_par_val = ','.join(usernames)
	print('I am looking up '+screen_name_par_val+' ids')

	params = {'screen_name': screen_name_par_val}
	response = client.get(userlookup_url, params=params)
	payload = response.json()
	for item in payload:
		users[item['screen_name']] = item['id']

	for u in usernames:
		if not u in users:
			print('coulnt find user ' + u)

	return users


def follow_users(users_file, creds,duration):
	# Duration is in seconds
	client = authenticate(creds)

	usernames = get_list_of_users(users_file)
	users_to_follow = lookup_users(usernames, client)

	FOLLOW_DURATION = timedelta(seconds=duration)
	MAX_TIME = datetime.utcnow() + FOLLOW_DURATION
	print('stop following at : ', str(MAX_TIME),' (UTC)')
	print('stop following at : ',datetime.now() + FOLLOW_DURATION,' (local time)')

	timeout = time.time() + duration
	print('Following will be stopped at {} (UTC)'.format(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(timeout))))

	params = {'follow': [i for u,i in users_to_follow.items()]}
	print(params)

	file_num = 1


	MAX_TWEETS = 100
	response = client.get(url, stream=True, params=params)
	if response.ok:
		f = open("tweets.json", "wb")
		num_tweets = 0
		try:
			for line in response.iter_lines():

				if time.time() > timeout:
					print("Time is up ...")
					f.close()
					print('Collected {} tweets'.format((file_num-1) * MAX_TWEETS + num_tweets))

				if num_tweets == MAX_TWEETS:
					print('Collected {} tweets at {} (UTC)'.format(file_num*MAX_TWEETS, time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(time.time()))))
					num_tweets = 0
					file_num += 1
					file_name = ''.join(['tweets_', str(file_num), '.json'])
					print('** opening new file {} **'.format(file_name))
					f.close()
					f = open(file_name,'wb')

				# Twitter sends empty lines to keep the connection alive. We need to filter those.
				if line:
					# stop after reaching MAX_TIME
					f.write(line + b'\n')
					num_tweets += 1
					if num_tweets%100 == 0:
						print(".", end='', flush=True)

		except KeyboardInterrupt:
			# User pressed the 'Stop' button
			print()
			print('Data collection interrupted by user!')
		finally:
			# Cleanup -- close file and report number of tweets collected
			f.close()
			print()
			print('Collected {} tweets.'.format(MAX_TWEETS*(file_num-1) + num_tweets))
	else:
		print('Connection failed with status: {}'.format(response.status_code))


def main():
	# python3 extract.py usernames.txt 15 # means run for 2 hours

	args = sys.argv[1:]
	users_file = str(args[0])
	my_creds = credentials
	run_for_duration = int(args[1])*60*60*24	#in seconds
	print('Follow the users for '+ str(run_for_duration)+' seconds')

	follow_users(users_file,my_creds,run_for_duration)

if __name__ == '__main__':
	main()