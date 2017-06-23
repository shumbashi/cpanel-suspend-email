#!/usr/bin/python

import sys
import subprocess
import urllib
import json

def main():
	if len(sys.argv) < 2:
		print "Argument missing: Supply an Email address"
		exit(1)

	email = sys.argv[1]

	try:
		domain = email.split('@')[1]
	except Exception:
		print 'Unable to parse email address'
		exit(1)

	command = "grep -R %s /var/cpanel/users | gawk -F':' '{print $1}' | head -n 1 | xargs grep USER | gawk -F'=' '{print $2}'" % domain
	email_owner,error  = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

	api_call = "uapi --user=%s --output=json Email suspend_login email=%s" % (email_owner.strip('\n'), urllib.quote_plus(email))
	result,error  = subprocess.Popen(api_call, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	try:
		result = json.loads(result)
		status = result['result']['status']
		if status == 1:
			exit(0)
		else:
			exit(1)
	except Exception as e:
		exit(1)

if __name__ == '__main__':
	main()
