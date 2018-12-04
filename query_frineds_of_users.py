from credentials import *
import time
from twython import TwythonRateLimitError, Twython,TwythonAuthError
from collections import defaultdict
import codecs
import requests
from requests_oauthlib import OAuth1

def retrieve_friends_ids(users, file_name):

    # CONSUMER_KEY1 = my_creds['CONSUMER_KEY']
    # CONSUMER_SECRET1 = my_creds['CONSUMER_SECRET']
    # OAUTH_TOKEN1 = my_creds['TOKEN_KEY']
    # OAUTH_TOKEN_SECRET1 = my_creds['TOKEN_SECRET']

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
    # creds['creds1'] = {'CONSUMER_KEY': CONSUMER_KEY1, 'CONSUMER_SECRET': CONSUMER_SECRET1, 'TOKEN_KEY': OAUTH_TOKEN1, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET1}
    creds['creds1'] = {'CONSUMER_KEY': CONSUMER_KEY2, 'CONSUMER_SECRET': CONSUMER_SECRET2, 'TOKEN_KEY': OAUTH_TOKEN2, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET2}
    creds['creds2'] = {'CONSUMER_KEY': CONSUMER_KEY3, 'CONSUMER_SECRET': CONSUMER_SECRET3, 'TOKEN_KEY': OAUTH_TOKEN3, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET3}
    creds['creds3'] = {'CONSUMER_KEY': CONSUMER_KEY4, 'CONSUMER_SECRET': CONSUMER_SECRET4, 'TOKEN_KEY': OAUTH_TOKEN4, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET4}
    creds['creds4'] = {'CONSUMER_KEY': CONSUMER_KEY5, 'CONSUMER_SECRET': CONSUMER_SECRET5, 'TOKEN_KEY': OAUTH_TOKEN5, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET5}
    creds['creds5'] = {'CONSUMER_KEY': CONSUMER_KEY6, 'CONSUMER_SECRET': CONSUMER_SECRET6, 'TOKEN_KEY': OAUTH_TOKEN6, 'TOKEN_SECRET': OAUTH_TOKEN_SECRET6}

    cred_inuse = 'creds1'

    last_use_time = [{'name': 'creds1', 'time': 0}, {'name': 'creds2', 'time': 0}, {'name': 'creds3', 'time': 0}, {'name': 'creds4', 'time': 0}, {'name': 'creds5', 'time': 0}]

    print(creds[cred_inuse])

    twitter_twy = Twython(creds[cred_inuse]['CONSUMER_KEY'], creds[cred_inuse]['CONSUMER_SECRET'], creds[cred_inuse]['TOKEN_KEY'],  creds[cred_inuse]['TOKEN_SECRET'])
    # twitter_twy = Twython(CONSUMER_KEY2, CONSUMER_SECRET2, OAUTH_TOKEN2, OAUTH_TOKEN_SECRET2)



    count_rate_exceed = 0
    with codecs.open(file_name,'w') as out_file:
        for u in users:
            ids = []
            next_cursor = -1
            # print("Retrieving friends of {}".format(u))
            out_file.write(' '.join(['-user',u,'\n']))
            while (next_cursor):
                try:
                    returned = twitter_twy.get_friends_ids(user_id=u, count=5000, cursor=next_cursor,
                                                           stringify_ids=True)
                    print('.',end='')

                    for result in returned['ids']:
                        ids.append(result)
                    next_cursor = returned["next_cursor"]

                    count_rate_exceed = 0

                except TwythonRateLimitError:
                    count_rate_exceed += 1
                    print('Too many requests')

                    # if count_rate_exceed > 3:
                    #     time.sleep(200)

                    # else:
                    last_use_time = sorted(last_use_time, key=lambda x: x['time'])
                    time_diff = time.time() - last_use_time[0]['time']
                    if time_diff < 900 and time_diff > 0:
                        print('sleeping for {} seconds'.format(900 - time_diff))
                        time.sleep(900 - time_diff)

                    last_use_time[0]['time'] = time.time()
                    cred_inuse = last_use_time[0]['name']

                    print('New credential: {}'.format(cred_inuse))
                    twitter_twy = Twython(creds[cred_inuse]['CONSUMER_KEY'], creds[cred_inuse]['CONSUMER_SECRET'],
                                          creds[cred_inuse]['TOKEN_KEY'], creds[cred_inuse]['TOKEN_SECRET'])
                except TwythonAuthError:
                    print("Couldn't authenticate {}".format(cred_inuse))
                    cred_inuse = cred_inuse[0:-1]+str(int(cred_inuse[-1])%5+1)
                    print('trying {}'.format(cred_inuse))
                    twitter_twy = Twython(creds[cred_inuse]['CONSUMER_KEY'], creds[cred_inuse]['CONSUMER_SECRET'],
                                          creds[cred_inuse]['TOKEN_KEY'], creds[cred_inuse]['TOKEN_SECRET'])


            print('\n')
            print("friends of {}.***count:{}".format(u,len(ids)))
            out_file.write(','.join(ids))
            out_file.write('\n')
            out_file.write('-------------------------\n')


    print("Process finished.")