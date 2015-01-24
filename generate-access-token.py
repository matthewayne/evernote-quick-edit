from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from urlparse import urlparse, parse_qsl

EN_URL="https://www.evernote.com"

CONSUMER_KEY = raw_input("Please enter your consumer key: ")
CONSUMER_SECRET = raw_input("Please enter your consumer secret: ")

client = EvernoteClient(
				consumer_key=CONSUMER_KEY,
				consumer_secret=CONSUMER_SECRET,
				sandbox= False
				)


request_token = client.get_request_token("http://localhost")
oauth_token = request_token['oauth_token'] 
oauth_token_secret = request_token['oauth_token_secret']
authorize_url = client.get_authorize_url(request_token)

AUTH_URL = raw_input("Please go to:\n"+authorize_url+"\nand authorize the application and paste the resulting URL here: ")

query= urlparse(AUTH_URL).query
params=parse_qsl(query)
params=dict(params)

auth_token = client.get_access_token(request_token['oauth_token'], request_token['oauth_token_secret'], params['oauth_verifier'])
print"\nHere is your auth token: \n\n%s\n\n" % auth_token

