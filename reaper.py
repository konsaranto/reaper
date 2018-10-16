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

import sys,queue,threading,arguments,functions

#---pass the parameters to and get the variables we need from functions.py---
save, url, parameters_list, number_of_tries, time_to_sleep, page, second_way, threadList = arguments.arguments(*sys.argv)

#---define the variables and start the threads---
Q = queue.Queue()
urlQ = queue.Queue()

#fill the Q
for i in parameters_list:
	Q.put(i)
print("\nNumber of credential combinations:", Q.qsize())

#fill the urlQ
for i in url:
	urlQ.put(i)
print("Number of urls:", urlQ.qsize())

#start the threads
print ("Starting threads...")
functions.main(Q, save, urlQ, parameters_list, number_of_tries, time_to_sleep, page, second_way, threadList)
