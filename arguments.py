'''
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

import sys,re

def arguments(*args):
    second_way = 0
    credentials = []
    page = 0
    number_of_tries = 0
    time_to_sleep = 0
    threadList = ['Thread-1']
    for i in range(0, len(args)):
        #display help
        if args[i] == "-h":
            help = """Syntax:	reaper.py	[-u username | -U username_file][-p password | -P password_file][-url url | -URL url_file]
	    	[-f save_file][-t number_of_tries:time_to_wait][-c url_after_failed_attempt][-th number_of_threads]
		[-s][-up file_with_credentials][parameters]

Flags:	-h display the help section
	-u set the username
	-U set the file containing the usernames (one username at each line)
      	-p set the password
      	-P set the file containing the passwords (one password at each line)
      	-up set the file containing the credentials (Syntax username:password) (one combination at each line)
	-url set the url and the port (e.g. http://127.0.0.1:160/login.php or http://scanme.nmap.org)
	 *don't omit /login.php or whatever it is, if it exists, and don't omit http:// or https://
      	-URL set the file containing the urls you want to attack (one url at each line)
	-f set the file to save the valid credentials found 						(required)
	-t set the number x of tries before waiting for y seconds (Syntax x:y) 				(optional)
      	-c set the full (http://) url that loads when you make a failed attempt
      	-th set the number of threads									(optional)
      	-s use a second method of validating credentials						(optional)"""
            print (help)
            sys.exit()

        #read the url
        if args[i] == "-url":
            url = args[i+1].split()

        #read and split the url file
        if args[i] == "-URL":
            urlfile = open(args[i+1], "r")
            url = urlfile.read().split("\n")
            url = url[:-1]
            for j in range(0,len(url)):
            	for k in url:
            		if k == "":
            			url.remove(k)
            urlfile.close()

        #file to save results
        if args[i] == "-f":
        	save = args[i+1]

        #read the username
        if args[i] == "-u":
        	usernames = args[i+1].split()

        #read the password
        if args[i] == "-p":
        	passwords = args[i+1].split()

        #read and split the credentials file
        if args[i] == "-up":
        	creds = open(args[i+1], "r")
        	credentials = creds.read().split("\n")
        	credentials = credentials[:-1]
        	for j in range(0,len(credentials)):
        		for k in credentials:
        			if k == "":
        				credentials.remove(k)
        	creds.close()
        	creds_file = None

        #read and split the username file
        if args[i] == "-U":
            userfile = open(args[i+1], "r")
            usernames = userfile.read().split("\n")
            usernames = usernames[:-1]
            for j in range(0,len(usernames)):
                for k in usernames:
                       if k == "":
        	                 usernames.remove(k)
            userfile.close()

        #read and split the password file
        if args[i] == "-P":
            passfile = open(args[i+1], "r")
            passwords = passfile.read().split("\n")
            passwords = passwords[:-1]
            for j in range(0,len(passwords)):
                for k in passwords:
                    if k == "":
                        passwords.remove(k)
            passfile.close()

        #get the parameters and make them a list
        if re.search("=.*?/", args[i]):
            parameters_list = []
            try:
            	creds_file
            except NameError:
            	pass
            else:
            	#if there is a credentials file
            	for j in range(0,len(credentials)):
            		#split the credentials
            		creds = credentials[j].split(":")
            		#replace USERNAME and PASSWORD with the credentials
            		parameters = args[i].replace('USERNAME', creds[0])
            		parameters = parameters.replace('PASSWORD', creds[1])
            		parameters = parameters.split()
            		#extend the param list with the parameters
            		parameters_list.extend(parameters)
            	break
            #for each combination of username and password
            for username in usernames:
            	for password in passwords:
            		#replace USERNAME and PASSWORD
            		parameters = args[i].replace('USERNAME', username)
            		parameters = parameters.replace('PASSWORD', password)
            		parameters = parameters.split()
            		#extend the param list with the parameters
            		parameters_list.extend(parameters)

        #set the sleeping variable
        if args[i] == "-t":
        	timing = args[i+1].split(":")
        	number_of_tries = timing[0]
        	time_to_sleep = timing[1]

        #if the page changes with failed attempts
        if args[i] == "-c":
            page = args[i+1]

        #if the second way of validating credentials is enabled
        if args[i] == "-s":
        	second_way = 1

        #set the number of threads
        if args[i] == "-th":
        	for j in range(1, int(args[i+1])):
        		threadList.append("Thread-%s" % (j + 1))

    return save, url, parameters_list, number_of_tries, time_to_sleep, page, second_way, threadList
