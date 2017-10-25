import json
import urllib
import os
import os.path
import sys
import requests
from random import randint
import numpy as np
from flask import session
from flask import render_template
from flask import request, url_for, make_response,redirect
from watson_developer_cloud import ConversationV1
from os.path import join, dirname
from flask import Flask
import csv

#import pysolr
#from watson_developer_cloud import RetrieveAndRankV1

	
conversation = ConversationV1(
    username='8f852f62-ded3-4c89-b696-f6999670f391',
    password='wMCxakn17KSZ',
    version='2017-02-03')


	
print("inside global application")

#conv_workspace_id = '72e3ba4d-5ca3-4fa4-b696-4b790d55cf5d'
# conv_workspace_id = '5c2446b9-28a3-40f9-906e-b46350f494b3'
conv_workspace_id = '5e685fd6-a971-47f1-af9b-ab409f4c5a36'

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)

@app.route("/")
def get():
	print("inside get")
	session['context'] = {}
	session.modified=True
	resp=make_response(render_template("index.html"))
	return resp

@app.route("/", methods=['GET','POST'])


def post(): 
	#print('*******starting post method****')
	data = request.form['message'].lower()
	script10 = """<html></html>"""
	context = {}
	example_list = list()
	class_name_flag=False
	flag1 = False
	flag2 = False
	intent_list = list()
	
	try:
		if 'context' in session:
			context = json.loads(session['context'])
		else:
			context = {}
	except:
		#print('value not in session')
		""""""
	

	response = conversation.message( workspace_id = conv_workspace_id, message_input={'text':data }, context = context)
	print("***********"+json.dumps(response,indent=2)+"***************")
	current_intent = None
	intent_arr = ["greetings","goodbye","courtesy","fwords","sysreg","sesdr","gacdw"]
	current_context = None
	try:
		current_intent = response['intents'][0]['intent']
		tool = current_intent.split("_")
		current_context = tool[0]
		#print(current_intent)
		if current_intent in intent_arr:
			print('No suggestions for this intent')
		else:
			print("suggestions available this intent")
			flag1 = True
			flag2 = True
	except:
		print('No intent found for current query')
	
	
	if flag1:
		list_intents1  = conversation.list_intents(workspace_id = conv_workspace_id)
		#print(json.dumps(list_intents1,indent = 2) , "length is = ", len(list_intents1['intents']))
		intent_list3= list()
		i = 0
		while ( i < len(list_intents1['intents'])):
			intent_name = list_intents1['intents'][i]['intent']
			#print(intent_name)
			domain_name = intent_name.split("_")
			#print(domain_name[0])
			if current_context == domain_name[0]:
				intent_list3.append(intent_name)
			i += 1
		#print(intent_list3)
		n = None
		if len(intent_list3) > 3:
			n = np.arange(3)
		else:
			n = np.arange(len(intent_list3))
			np.random.shuffle(n)
		#print(n)
		for x in n:
			examples = conversation.list_examples(workspace_id = conv_workspace_id,intent = intent_list3[x])
			#print(json.dumps(examples,indent = 4))
			n = len(examples['examples'])
			n = randint(0, n-1)
			example_list.append(examples['examples'][n]['text'])
	
	#print(example_list)
	suggestion1 = """<html></html>"""
	if flag2:
		if len(example_list) == 1:
			suggestion1 = """<html><hr><body>
					<strong>Corresponding queries:</strong><br>
					<ul>
					<li>{query1}</li>
					</ul>
					<body><html>""".format(query1=example_list[0])
		if len(example_list) == 2:
			suggestion1 = """<html><hr><body>
					<strong>Corresponding queries:</strong><br>
					<ul>
					<li>{query1}</li>
					<li>{query2}</li>
					</ul>
					<body><html>""".format(query1=example_list[0],query2=example_list[1])
		if len(example_list) == 3:
			suggestion1 = """<html><hr><body>
					<strong>Corresponding queries:</strong><br>
					<ul>
					<li>{query1}</li>
					<li>{query2}</li>
					<li>{query3}</li>
					</ul>
					<body><html>""".format(query1=example_list[0],query2=example_list[1],query3=example_list[2])
	if 'context' in session:
		session['context'] = json.dumps(response['context'])
	
	try:
		response = response['output']['text'][0] + suggestion1
	except:
		response = "Good that you asked us, I will get updated on that very soon and will get back to you."
	return response

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 80))
	app.run(debug=True, host='0.0.0.0', port=port)
	
	

			
			