#Twitter API credentials

#Email default configurations:
smtp_server = 'smtp.gmail.com'
from_address = 'sentiment.notificator@gmail.com'
to_address = 'dmontufar@student.unimelb.edu.au'
from_password = 'Twittersentiment'
def_subject = 'Harvesting process status update'
smtp_port = 587

#Local CouchDB 

server = 'http://localhost:5984/'
vm_ip = 'node2:115.146.87.46'
database = ''
location = ''
admin_user = 'node2'
admin_pass = 'sentiment2'

#Initialize variables for each quadrant
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
region_quadrant = ''
#Bounding Box:
locations = []


def defineQuadrant(quadrant):

	global consumer_key
	global consumer_secret
	global access_token
	global access_secret
	#Bounding Box:
	global locations
	global location
	global database
	global region_quadrant

#Node 2 configuration: Northern Territory
#Northern Territory:
	if quadrant == '1':
		database = 'northernt'
		location = 'NorthernTerritory'
		region_quadrant = '1'
		consumer_key = 'MhAsXbp6r8W22TGkx5YOhtMOi'
		consumer_secret = 'z7CAEvAzjY02DrJlAqSSMirF46QRmDyirK2tSEUPd5Mkn6sarY'
		access_token = '3112457798-eb4ar8eoPYm7lgAXUiB5SzQvtK8YdYXrjOw2WHQ'
		access_secret = 'tJnkaujfhNN0ddiTKD8eRkWfjIkV3RDRu5lXXQ4SVjWfi'
		#Bounding Box:
		locations = [129.0199,-15.0182,133.4968,-12.6084]  
	elif quadrant == '2':
		database = 'northernt'
		location = 'NothernTerritory'
		region_quadrant = '2'
		consumer_key = 'oTUiA9QcbtnypAxGpCnjc9xuo'
		consumer_secret = '6E6qfYVyi8Eaq9aTmIPaY7HCgpuTEqj152pd6G0LG2nunUYAlw'
		access_token = '3112421772-NcmX2chb8XLUGSrAHtFCQZh1bBiKEY7Roio5vDV'
		access_secret = 'y9DYULTLDhBXAtr624anQHz6E0azpjAcHr3dwrrw6d5LL'
		#Bounding Box:
		locations = [129.9647,-12.6084,133.4968,-10.8864]  
	elif quadrant == '3':
		database = 'northernt'
		location = 'NorthernTerritory'
		region_quadrant = '3'
		consumer_key = 'AoU8gS1l1EmhwYP9P0Dp37C1b'
		consumer_secret = 'xTymN58jouBNNhjhZ7qGSpdFzx5DwSLFcljHI3nUeMUG0VMb8q'
		access_token = '3112514239-ZONBAZdkn6wcTW9MFDq3QT8xC4ovx8SIjLRx5PD'
		access_secret = 'joyTa2bSGYvApvkVMHJ9l8WGdyCh3UzF5lkQVJPNSBewN'
		#Bounding Box:
		locations = [133.4968,-14.7857,135.6117,-11.2745]  
	elif quadrant == '4':
		database = 'northernt'
		location = 'NorthernTerritory'
		region_quadrant = '4'
		consumer_key = 'uBOVqbtLh0r21to7JHbBZ66cF'
		consumer_secret = 'Q8CAytcmjLmbqtZYhI96ZkRoU0HAucgz1PuJ3zzTxZgBHrgPq0'
		access_token = '3112527331-IU1A0xCL04GajQcg6lWp2fRIXbMBtEDiLByFnfn'
		access_secret = 'RVkwUlAMfTLfCrKNrLaTHWAHl3aI4zFNkC4twxpqTHXWm'
		#Bounding Box:
		locations = [135.6117,-14.7857,137.1443,-10.7353]
