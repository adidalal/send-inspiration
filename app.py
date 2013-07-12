# app.py

# import required libraries
import os
import requests
import sendgrid
from flask import Flask, render_template, request
from twilio.rest import TwilioRestClient

# import configuration variables
from myconfig import *
client = TwilioRestClient(account_sid, auth_token)
footer = "\n\n\n[Sent via tiny.cc/sendinspiration]"

# initialize Flask
app = Flask(__name__)

# return main page if no parameters passed
@app.route('/')
def main_page():
    return render_template('index.html')
	
# return text response if requested by twilio	
@app.route('/reply')
def reply():
    return render_template('reply.xml')

@app.route('/quotes')
def quote():
    # get random quote
    get_response = requests.get(url='http://api.forismatic.com/api/1.0/?method=getQuote&format=text&lang=en')
    quote = get_response.text
    # send quote via text [Twilio]
    if len(request.args['number']) > 0:
	# define phone number as the one passed from webpage
        phonenum = request.args['number']
	# send text
    	message = client.sms.messages.create(body=quote,
    	to= phonenum ,
    	from_= mynum)
    	# show user the success web page
	return render_template('finish.html')
    
    # send quote via email [SendGrid]
    else:
	# define email as the one passed from webpage
    	email = request.args['email']
	# send email
    	s = sendgrid.Sendgrid(suser, spass, secure=True)
    	body = quote + footer
	message = sendgrid.Message(semail, "Inspirational Quote", body, body)
	message.add_to(email)
	s.web.send(message)
	# show user the success web page
	return render_template('finish.html')
	
# run app
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)