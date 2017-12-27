from wit import Wit 
from gnewsclient import gnewsclient
from pprint import pprint

# server_access_token_here
access_token = "BDXO7ZVHGTJ3SKZVHVEZLM4L4K7C7D4G"

client = Wit(access_token = access_token)


#message_text = "I live in Brazil"
#resp = client.message(msg=message_text)
#pprint(resp)


def wit_response(message_text):
	resp = client.message(msg=message_text)
	categories = {'news_type': None, 'location': None}
	
	entities = list(resp['entities'])
	for entity in entities:
		categories[entity] = resp['entities'][entity][0]['value']
	return categories

#pprint(wit_response('I want sport news from Brazil'))


def get_news_elements(categories):
	news_client = gnewsclient()
	news_client.query = ''
	
	if categories['news_type'] != None:
		news_client.query += categories['news_type']
		
	if categories['location'] != None:
		news_client.query += categories['location']
		
	news_items = news_client.get_news()
	
	elements = []
	
	for item in news_items:
		element = {
					'title': item['title'],
					'buttons': [{
								'type': 'web_url',
								'title': 'Read more',
								'url': item['link']
					}],
					'image_url': item['img']		
		}
		elements.append(element)
		
	return elements
		
#pprint(get_news_elements(wit_response("I want sport news from Brazil")))





"""
def wit_response(message_text):
	resp = client.message(message_text)
	categories = {'newstype':None, 'location':None}

	
	entities = list(resp['entities'])
	for entity in entities:
		categories[entity] = resp['entities'][entity][0]['value']
	
	return categories

def get_news_elements(categories):
	news_client = gnewsclient()
	news_client.query = ''

	if categories['newstype'] != None:
		news_client.query += categories['newstype'] + ' '

	if categories['location'] != None:
		news_client.query += categories['location']

	news_items = news_client.get_news()

	elements = []

	for item in news_items:
		element = {
					'title': item['title'],
					'buttons': [{
								'type': 'web_url',
								'title': "Read more",
								'url': item['link']
					}],
					'image_url': item['img']		
		}
		elements.append(element)

	return elements
"""