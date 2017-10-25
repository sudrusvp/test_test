import json
import urllib
import os
import os.path
import sys
import requests
import datetime
import timeit
import numpy as np
from flask import session
from flask import render_template
from flask import request, url_for, make_response,redirect
from watson_developer_cloud import ConversationV1
from os.path import join, dirname
from flask import Flask
from watson_developer_cloud import NaturalLanguageClassifierV1
#import pysolr
#from watson_developer_cloud import RetrieveAndRankV1

	
conversation = ConversationV1(
    username='8f852f62-ded3-4c89-b696-f6999670f391',
    password='wMCxakn17KSZ',
    version='2017-02-03')

natural_language_classifier = NaturalLanguageClassifierV1(
	username='fa6bffcd-ebac-4ece-8b20-9baf4c23f78d',
	password='8OmO1tBVONCP')

	
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
	start_time = timeit.default_timer()
	#print('*******starting post method****')
	data = request.form['message'].lower()
	script10 = """<html></html>"""
	context = {}
	example_list = [None] * 3
	class_name = [None] * 3
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
	
	#try:
	#	current_context=response['context']['current_context']
	#except:
	#	print('current_context not there')
	try:
		if response['intents'][0]['intent']:
			name = response['intents'][0]['intent']
			tool = name.split("_")
			current_context = tool[0]
			if current_context == 'goodbye' or current_context == 'courtesy' or current_context == 'greetings' or current_context=='intro' or current_context=='fwords' or current_context == 'sysreg' or current_context == 'sesdr' or current_context == 'gacdw' or current_context == 'cirats' or current_context== 'uid' :
				print('smalltalk')
			else:
				if current_context=='ecm':
					classifier = natural_language_classifier.classify('ad937ax205-nlc-835',data)
					
				elif current_context=='urt':
					classifier = natural_language_classifier.classify('ad940ex207-nlc-821',data)
					
				elif current_context=='uid':
					classifier = natural_language_classifier.classify('bfad19x228-nlc-3579',data)
					
				elif current_context=='pce':
					classifier = natural_language_classifier.classify('bfad19x228-nlc-3579',data)
					
				elif current_context=='cirats':
					classifier = natural_language_classifier.classify('bbb1c7x227-nlc-5144',data)
						
				elif current_context=='cwp':
					classifier = natural_language_classifier.classify('bbab2cx226-nlc-5117',data)
					
				elif current_context=='epolicy':
					classifier = natural_language_classifier.classify('ad940ex207-nlc-807',data)
					
				elif current_context=='gem':
					classifier = natural_language_classifier.classify('bbb1c7x227-nlc-5077',data)
				#print(json.dumps(classifier, indent=2))
				i = 0
				j = 0
				#class_name = [None] * 3
				while (j < 3):
					try:
						class_name[j] = classifier['classes'][i]['class_name']
						if classifier['classes'][i]['confidence'] == 1:
							arr = conversation.list_examples(workspace_id = conv_workspace_id,intent = str(class_name[i]))['examples']
							#print(len(arr))
							class_name_flag=True
							if len(arr) == 1:
								i = i + 1
								continue
							else:
								flag1 = True
					except:
						print('classname not exist')
					if class_name[j] == 'goodbye' or class_name[j] == 'emotions' or class_name[j] == 'courtesy' or class_name[j] == 'greetings' or class_name[j] == 'intro':
						i = i + 1
						continue
					j = j + 1
					i = i + 1
				
	except:
		print('intent not exist')
	
	try:
		if class_name_flag:
			example_list = [None] * 3
			i = 0
			#print (class_name[0])
			#print (class_name[1])
			#print (class_name[2])
			while (i < 3):
				examples = conversation.list_examples(workspace_id = conv_workspace_id,intent = str(class_name[i]),page_limit=None, include_count=None, sort=None, cursor=None)
				#print (class_name[0])
				arr = np.arange(len(examples['examples']))
				np.random.shuffle(arr)
				example_list[i] = examples['examples'][arr[0]]['text']
				if flag1:
					if data in example_list[i]:
						print("1")
						example_list[i] = examples['examples'][arr[1]]['text']
						print('2')
				example_list[i] = example_list[i].capitalize()
				# example_list[arr[0]] = examples['examples'][0]['text']
				# print(example_list[i])
				i = i +1

		else:
			print('classnameflag false')
	except:
		print("error in examples")
	
	try:
		if class_name_flag:
			if example_list[1] == None:
				script10 = """<html><hr><body>
					<strong>Corresponding queries:</strong><br>
					<ul>
					<li>{query1}</li>
					</ul>
					<body><html>""".format(query1=example_list[0])
			
			elif example_list[2] == None:
				script10 = """<html><hr><body>
					<strong>Corresponding queries:</strong><br>
					<ul>
					<li>{query1}</li>
					<li>{query2}</li>
					</ul>
					<body><html>""".format(query1=example_list[0],query2=example_list[1])
			else:
				script10 = """<html><hr><body>
							<strong>Corresponding queries:</strong><br>
							<ul>
							<li>{query1}</li>
							<li>{query2}</li>
							<li>{query3}</li>
							</ul>
							<body><html>""".format(query1=example_list[0],query2=example_list[1],query3=example_list[2])
		else:
			print("classname flag false2")
	except:
		print("in except")

	
	if 'context' in session:
		session['context'] = json.dumps(response['context'])
	#	print(session['context'])
	
	#json_data = {}
	#script3 = """<html></html>"""
	#url=""

	""""try:
		if str(response['context']['action']) == 'cust_details_action':
			try:
				cust_detail = str(response['context']['param'])
				print("Query asked with customer ID. Customer details="+cust_detail)
				url = 'http://ehnsarmecmpre01.extnet.ibm.com/api.php?query=%s'%cust_detail
				return_val = requests.get(url,verify = False, proxies = {
							'http': '',
							'https': ''
					})
				json_data = return_val.json()
				print(json_data)
			except:
				print('connection issue!!!')
	except:
		print("cust_details_action not found!")
	"""	
	
#		script2 = """<html>
#			<p style='visibility:hidden;' id='context' name='context'>{code}</p>
#			</html>""".format(code=str(json.dumps(response['context'])))
	#script4 = """<html></html>"""
	#try:
	#	if response['intents'] and response['intents'][0]['confidence']:
	#		confidence = str(round(response['intents'][0]['confidence'] * 100))
	#		script4 = str("<HTML><BODY><hr style='height: 7px;border: 0;box-shadow: 0 10px 10px -10px white inset;width:270px;margin-left:0px'></body></html>I'm "  + confidence + "% certain about this answer!")
	#except:
	#	""""""
		#print("confidence not exist")
	

	try:
		response = response['output']['text'][0] + script10
	except:
		response = "Good that you asked us, I will get updated on that very soon and will get back to you."
	#print("******leaving post method*********")
	#elapsed = timeit.default_timer() - start_time
	#print("time elapsed",elapsed)
	return response

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
	
	

			
			