import httplib, urllib
import json
from Modifiers import *

# load your API key and Arduino IP address into the json file 'setings.js'
# and specify the absolute path if running from Cron
f = open('/root/dev/jsonDuino/logging_clients/settings.js', 'r')
jsonObj = json.loads(f.read())
apikey = jsonObj['thingspeak_apikey']
arduino_ip = jsonObj['arduino_ip']
arduino = httplib.HTTPConnection(arduino_ip)


try:
	arduino.request("GET","/json")
	response = arduino.getresponse()
	print "Arduino response:" , response.status, response.reason
	jsonObj = json.loads(response.read())
	a0 = jsonObj['a0']
	print "a0:", modify(a0)

	params = urllib.urlencode({'field1': modify(a0),'key':apikey})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com:80")
	conn.request("POST", "/update", params, headers)
	ts_response = conn.getresponse()
	print "Thingspeak Response:", ts_response.status, ts_response.reason
	conn.close
except:
	print "connection failed!"

