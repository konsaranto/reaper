### Overview

Reaper is a python3 script which makes http post requests to gather valid credentials from site login forms.

**Reaper was created for educational purposes. Stay away from illegal activities.**

The script assumes that you have python3 installed under /usr/bin/python3. It also needs the sys,requests,re,time,os,threading,
queue,bs4 modules and the lxml parser installed.

## Usage

```
reaper.py   [-u username | -U username_file][-p password | -P password_file][-url url | -URL url_file]
            [-f save_file][-t number_of_tries:time_to_wait][-c url_after_failed_attempt]
            [-th number_of_threads][-s][-up file_with_credentials][parameters]
```

## Flags

-h display the help section  
-u set the username  
-U set the file containing the usernames (one username at each line)  
-p set the password  
-P set the file containing the passwords (one password at each line)
-up set the file containing the credentials (Syntax username:password) (one combination at each line)  
-url set the url and the port (e.g. http://127.0.0.1:160/login.php or http://scanme.nmap.org)  
  don't omit /login.php or whatever it is, if it exists, and don't omit http:// or https://  
-URL set the file containing the urls you want to attack (one url at each line)  
-f set the file to save the valid credentials found (required)  
-t set the number x of tries before waiting for y seconds (Syntax x:y) (optional)  
-c set the full (http://) url that loads when you make a failed attempt (optional)  
-th set the number of threads (optional)  
-s use a second method of validating credentials (optional)  

## Comments

Set the parameters to be passed along with the http requests. Do it like this:
username=USERNAME/password=PASSWORD/csrf_token=TOKEN/... , where username, password, csrf_token etc. are the names of the
parameters to be passed with the request. The order of the parameters passed doesn't matter. Put capitalized USERNAME
and PASSWORD at the appropriate places so the script knows where to replace with the ones from the files. Obviously, find
the parameters' names either by looking at the source code or with Burp Suite or whatever, but do not url encode any of the
characters, as Reaper is gonna do it when it makes the requests.

Also, if the site is using csrf tokens (a parameter with a value that changes at each post request), take notice:
-If the site has the value for the token embedded in the HTML code (look at the source code) place the word TOKEN at the
 appropriate place.
-If the site gets the value for the token from a script (look at the source code) place the word SCRIPT at the appropriate place.
-If there is no csrf token don't even include the parameter at all.
-If there are more than one csrf tokens put the appropriate value (TOKEN | SCRIPT) for each one.
To spot a csrf token make some post requests and notice if any of the parameters' value changes.

Notice that a lot of sites actually have protection against this type of attack, by blocking the ip address of the attacker for
some time, rendering it unable to perform requests. You can use the -t flag to set the number x of tries before the thread waits
for the y amount of time to continue. This works properly only if there is one thread working on a url.

You can set the number of parallel threads with the -th flag. The way this works is say you have 3 urls to check and 4 threads.
The first and second thread are gonna work on the first and second url respectively and the third and fourh thread are gonna
work at the third url together. If you specify the -t flag it's gonna work properly for the first and second url but not for
the third one. The same logic applies to any number of urls.

You can also limit the amount of username/password combinations you try, considering that most routers use a small collection
of credentials by default. You can properly do this with the -up flag, so it doesn't try every password with every username.

Some sites change the url they serve when you make a failed login attempt. If that's the case you must use the -c flag and set
this url. That's cause the script uses the url as an indicator of a successful or failed login attempt. That means that, if the
url they serve after a failed login attempt changes, the script is gonna think that the changed url translates to a successful
attempt and give wrong results. When you specify this changed url with the -c flag the script will know that this url means
failure.

The -s flag tells the scipt to use a second way of validating credentials. It doesn't work when the parameters you pass at the
command line are not exactly the same as the ones the post request needs, because then the script is gonna think that the
parameters passed are right and give false positive result. So this is better used as a way to cross check the results of the
default method when there is only one url, so you know exactly the parameter names.

### Contact Information

Konstantinos Sarantopoulos  
konsaranto@gmail.com
