from credentials import *
import time
from twython import TwythonRateLimitError, Twython,TwythonAuthError
from collections import defaultdict
import codecs
import requests
from requests_oauthlib import OAuth1
from Inputs import authenticate
import datetime
import json
import os
from requests import exceptions

def retrieve_friends_ids(users, file_name):


    stats = { 'creds1':{'200': 0, '401':0, '429':0},
              'creds2': {'200': 0, '401': 0, '429': 0},
              'creds3': {'200': 0, '401': 0, '429': 0},
              'creds4': {'200': 0, '401': 0, '429': 0},
              'creds5': {'200': 0, '401': 0, '429': 0},
              '404' : 0
    }


    CONSUMER_KEY2 = my_credsa['CONSUMER_KEY']
    CONSUMER_SECRET2 = my_credsa['CONSUMER_SECRET']
    OAUTH_TOKEN2 = my_credsa['TOKEN_KEY']
    OAUTH_TOKEN_SECRET2 = my_credsa['TOKEN_SECRET']

    CONSUMER_KEY3 = my_credsb['CONSUMER_KEY']
    CONSUMER_SECRET3 = my_credsb['CONSUMER_SECRET']
    OAUTH_TOKEN3 = my_credsb['TOKEN_KEY']
    OAUTH_TOKEN_SECRET3 = my_credsb['TOKEN_SECRET']

    CONSUMER_KEY4 = my_credsc['CONSUMER_KEY']
    CONSUMER_SECRET4 = my_credsc['CONSUMER_SECRET']
    OAUTH_TOKEN4 = my_credsc['TOKEN_KEY']
    OAUTH_TOKEN_SECRET4 = my_credsc['TOKEN_SECRET']

    CONSUMER_KEY5 = my_credsd['CONSUMER_KEY']
    CONSUMER_SECRET5 = my_credsd['CONSUMER_SECRET']
    OAUTH_TOKEN5 = my_credsd['TOKEN_KEY']
    OAUTH_TOKEN_SECRET5 = my_credsd['TOKEN_SECRET']

    CONSUMER_KEY6 = my_creds['CONSUMER_KEY']
    CONSUMER_SECRET6 = my_creds['CONSUMER_SECRET']
    OAUTH_TOKEN6 = my_creds['TOKEN_KEY']
    OAUTH_TOKEN_SECRET6 = my_creds['TOKEN_SECRET']


    creds = defaultdict(str)
    creds['creds1'] = {'CONSUMER_KEY': CONSUMER_KEY2, 'CONSUMER_SECRET': CONSUMER_SECRET2, 'TOKEN_KEY': OAUTH_TOKEN2, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET2}
    creds['creds2'] = {'CONSUMER_KEY': CONSUMER_KEY3, 'CONSUMER_SECRET': CONSUMER_SECRET3, 'TOKEN_KEY': OAUTH_TOKEN3, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET3}
    creds['creds3'] = {'CONSUMER_KEY': CONSUMER_KEY4, 'CONSUMER_SECRET': CONSUMER_SECRET4, 'TOKEN_KEY': OAUTH_TOKEN4, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET4}
    creds['creds4'] = {'CONSUMER_KEY': CONSUMER_KEY5, 'CONSUMER_SECRET': CONSUMER_SECRET5, 'TOKEN_KEY': OAUTH_TOKEN5, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET5}
    creds['creds5'] = {'CONSUMER_KEY': CONSUMER_KEY6, 'CONSUMER_SECRET': CONSUMER_SECRET6, 'TOKEN_KEY': OAUTH_TOKEN6, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET6}

    cred_inuse = 'creds1'

    last_use_time = [{'name': 'creds1', 'time': 0}, {'name': 'creds2', 'time': 0}, {'name': 'creds3', 'time': 0}, {'name': 'creds4', 'time': 0}, {'name': 'creds5', 'time': 0}]

    print(creds[cred_inuse])

    # twitter_twy = Twython(CONSUMER_KEY2, CONSUMER_SECRET2, OAUTH_TOKEN2, OAUTH_TOKEN_SECRET2)
    client = authenticate(creds[cred_inuse])

    dic = {}

    unsuccessful_users = []

    url_friends = 'https://api.twitter.com/1.1/friends/ids.json'

    count_consec_limit = 0

    if os.path.exists(file_name):
        mode = 'a'
    else:
        mode = 'w'

    try:
        with codecs.open(file_name,mode) as out_file:
            for u in users:
                ids = []
                next_cursor = -1
                out_file.write(' '.join(['-user',u,'\n']))
                while (next_cursor):

                    param = {'user_id': u, 'stringify_ids': True, 'cursor': next_cursor, 'count': 5000}
                    try:
                        response = client.get(url_friends, params = param)
                    except exceptions.ConnectionError:
                        print('connection error, renewing the connection')
                        client = authenticate(creds[cred_inuse])

                    if response.status_code == 200:
                        print('.',end='')
                        data = response.json()
                        ids.extend(data['ids'])
                        next_cursor = data["next_cursor"]

                        count_consec_limit = 0

                        try:
                           dic[u].extend(data['ids'])
                        except KeyError:
                           dic[u] = data['ids']

                        stats[cred_inuse]['200'] += 1

                    elif response.status_code == 401:
                        stats[cred_inuse]['401'] += 1
                        print('Unauthorized.')
                        unsuccessful_users.append(u)
                        break
                    elif response.status_code == 404:
                        print('User not found.')
                        stats['404'] += 1
                        break

                    elif response.status_code == 429:
                        stats[cred_inuse]['429'] += 1

                        count_consec_limit += 1

                        if count_consec_limit >= len(creds)+1:
                            rem = int(response.headers['x-rate-limit-remaining'])
                            print('remaining request : {}'.format(rem))
                            next_reset = datetime.datetime.fromtimestamp(int(response.headers['x-rate-limit-reset']))
                            now = datetime.datetime.now()
                            diff = (next_reset - now).total_seconds()+10
                            if diff > 0:
                                print('sleeping for {} seconds.'.format(diff))
                                time.sleep(diff)
                            else:
                                print('sleeping for {} seconds.'.format(900))
                                time.sleep(900)

                        else:
                            cred_inuse = cred_inuse[0:-1] + str(int(cred_inuse[-1]) % 5 + 1)
                            try:
                                client = authenticate(creds[cred_inuse])
                            except:
                                print('Unable to authenticate {}'.format(cred_inuse))
                                cred_inuse = cred_inuse[0:-1] + str(int(cred_inuse[-1]) % 5 + 1)
                                client = authenticate(creds[cred_inuse])


                print('\n')
                print("friends of {}.***count:{}".format(u,len(ids)))
                out_file.write(','.join(ids))
                out_file.write('\n')
                out_file.write('-------------------------\n')
    finally:
        try:
            with codecs.open('{}-unsuccesful.txt'.format(file_name[0:-4]),'w') as f:
                for u in unsuccessful_users:
                    f.write(u)
                    f.write('\n')
        except:
            print('Unseccessfull queries:')
            print(unsuccessful_users)

        try:
            with codecs.open('{}-stats.txt'.format(file_name[0:-4]),'w') as f:
                f.write(json.dumps(stats))  # use `json.loads` to do the reverse
        except:
            print(stats)

    print("Process finished.")