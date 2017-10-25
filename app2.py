import json
import urllib
import os
import os.path
import sys
import requests
import numpy as np
from flask import session
from flask import render_template
from flask import request, url_for, make_response,redirect
from watson_developer_cloud import ConversationV1
from os.path import join, dirname
from flask import Flask
import csv
from random import shuffle

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
	suggestion1 = """<html></html>"""
	context = {}
	example_list = list()
	class_name_flag=False
	flag1 = False
	
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
			csv_path = "static/doc/"+current_context+".csv"
			ifile = open(csv_path,'r',encoding="UTF8")
			reader = csv.reader(ifile,delimiter = ',')
			data = list(reader)
			shuffle(data)
			no_of_rows = len(data)
			#print("no.of rows available are ",no_of_rows)
			temp_intent = list()
			for row in data:
				if current_intent == row[1]:
					""""""
					#print("same intent so excluded it")
				else:
					if row[1] in temp_intent:
						continue
					temp_intent.append(row[1])
					example_list.append(row[0])	
	except:
		print('No intent found for current query')
	

	if flag1:
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

		if len(example_list) == 4:
			suggestion1 = """<html><hr><body>
					<strong>Corresponding queries:</strong><br>
					<ul>
					<li>{query1}</li>
					<li>{query2}</li>
					<li>{query3}</li>
					<li>{query4}</li>
					</ul>
					<body><html>""".format(query1=example_list[0],query2=example_list[1],query3=example_list[2],query4=example_list[3])

		if len(example_list) == 5:
			suggestion1 = """<html><hr><body>
					<strong>Corresponding queries:</strong><br>
					<ul>
					<li>{query1}</li>
					<li>{query2}</li>
					<li>{query3}</li>
					<li>{query4}</li>
					<li>{query5}</li>
					</ul>
					<body><html>""".format(query1=example_list[0],query2=example_list[1],query3=example_list[2],query4=example_list[3],query5=example_list[4])			

		if len(example_list) == 6:
			suggestion1 = """<html><hr><body>
					<strong>Corresponding queries:</strong><br>
					<ul>
					<li>{query1}</li>
					<li>{query2}</li>
					<li>{query3}</li>
					<li>{query4}</li>
					<li>{query5}</li>
					<li>{query6}</li>
					</ul>
					<body><html>""".format(query1=example_list[0],query2=example_list[1],query3=example_list[2],query4=example_list[3],query5=example_list[4],query6=example_list[5])
	if 'context' in session:
		session['context'] = json.dumps(response['context'])
	
	
	try:
		response = response['output']['text'][0] + suggestion1 +script
	except:
		response = "Good that you asked us, I will get updated on that very soon and will get back to you."
	return response

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
	
	

			
			