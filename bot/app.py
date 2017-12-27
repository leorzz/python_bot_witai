
# https://www.youtube.com/watch?v=kKD-4jlvsM8&list=PLyb_C2HpOQSC4M3lzzrql7DSppTeAxh-x&index=2
# https://github.com/nikhilkumarsingh/facebook-messenger-bot
# https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
# https://github.com/davidchua/pymessenger

import os, sys
from flask import Flask, request
from utils import wit_response, get_news_elements
from pymessenger.bot import Bot
from pprint import pprint

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAWCSmSrM7QBAIruQDZCWn3ZALPSrtN8nTr5uZCUKiSZBOubcRwfjrE2lFeNZCmDbWZAavVwLc7P5J39ZAsjQIGiNJuX1WnpIPY6ir2Y5PPtvzzUROcVzfJyNKkBlN4ZCntZCZBQ2MOihKbbS5MHes84qFI8AhFi02k5lEVXlbZA9G0wKkvZBZBLlpEmI"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "11223344":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200



@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	#log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:
				
				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']
				
				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'
					
					response = None
					entity, value = wit_response(messaging_text)
					
					if entity == 'news_type':
						response = "Ok. I will send you {} news".format(str(value))
					elif entity == 'location':
						response = 'Ok. So, you live in {0}. I will send you top headlines from {0}'.format(str(value))
						
					if response == None:
						response = "Sorry, I didn't undestand!"
					
					
					bot.send_text_message(sender_id, response)
					

	return 'ok', 200
	



def log(message):
	print("===== Log =====")
	print(message)
	sys.stdout.flush()



if __name__ == "__main__":
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
