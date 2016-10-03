import requests

htmlfile = None
try:
    htmlfile.raise_for_status()
except requests.RequestException as e:
    print "exception"
    print e
