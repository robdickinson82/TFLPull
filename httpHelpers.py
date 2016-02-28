import urllib
from urllib2 import Request, urlopen, URLError, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, install_opener, build_opener, HTTPCookieProcessor
from cookielib import CookieJar


def openUrl(url, data = None, headers = None, opener = None):
	if data:
		encodedData = urllib.urlencode(data)
	else:
		encodedData = None	
		
	if headers:
		req = Request(url, encodedData, headers)
	else:
		req = Request(url, encodedData)

	try:
		if opener:
			f = opener.open(req)
		else:
			f = urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		elif hasattr(e, 'code'):
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code
	else:
		print 'Successfully got URL'	
		return f


def getCookieOpener():

	# create "opener" (OpenerDirector instance)
	opener = build_opener(HTTPCookieProcessor(CookieJar()))

	# Install the opener.
	# Now all calls to urllib2.urlopen use our opener.
	install_opener(opener)
	return opener