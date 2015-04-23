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
vm_ip = 'node1:localhost'
database = ''
location = ''
admin_user = 'diogonal'
admin_pass = 'dgl0588'

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

#Node 1 configuration: Test
#Test:
	if quadrant == '1':
		database = 'test'
		location = 'TEST'
		region_quadrant = '1'
		consumer_key = '86AeqigDcQNqySn1DQm5GZ5Jv'
		consumer_secret = 'KxjrbvZiQyBcvJtNDWyKPAnTr6kyIAWZMdpEBuftWKdzUg0JK9'
		access_token = '3161848488-ffvqUxam48G60zqPTklYTWwWY1N5sNMW2LlDUdd'
		access_secret = 'irs9HUlGEg35FrxJVc0cgCTzWlwkVjxwips58GxKR7kgq'
		#Bounding Box:
		locations = [145.0544,-39.1549,148.2020,-35.7746] 
