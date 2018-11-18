from collections import defaultdict
import requests
from requests_oauthlib import OAuth1

def authenticate(credentials):
    try:
        oauth = OAuth1(client_key=credentials['CONSUMER_KEY'],
                      client_secret=credentials['CONSUMER_SECRET'],
                      resource_owner_key=credentials['TOKEN_KEY'],
                      resource_owner_secret=credentials['TOKEN_SECRET'],
                      signature_type='auth_header')
        client = requests.session()
        client.auth = oauth
        return client
    except (KeyError, TypeError):
        print('Error setting auth credentials.')
        raise

users_list = [
	'@BarackObama'
    '@realDonaldTrump'
    '@HillaryClinton'
]