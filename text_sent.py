from flask import Flask, request, redirect
import textblob, os
from textblob import TextBlob
from twilio.rest import Client

# Setup web application to receive incoming texts via webhooks
app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])

def analyze_text():

	# Setup twilio client to receive and send text from the right numbers
	trial_num =  os.environ.get('TWILIO_NUM')
	my_num = os.environ.get('MY_NUM')

	account_sid = os.environ.get('ACCOUNT_SID')
	tw_auth_token = os.environ.get('TW_AUTH_TOKEN')
	client = Client(account_sid, tw_auth_token)

	# Save incoming text body and analyze its sentimental polarity
	in_message = request.form['Body']

	analysis = TextBlob(in_message)
	polarity = analysis.sentiment.polarity
	
	if polarity > 0:
		out_message = 'positive sentiment'
	elif polarity < 0:
		out_message = 'negaitve sentiment'
	else:
		out_message = 'neutral sentiment'

	# Send text back of the polarity
	message = client.messages \
					.create(
						 body= out_message,
						 from_= trial_num,
						 to= my_num
					 )
	return str(in_message)

if __name__ == "__main__":
    app.run(debug=True)