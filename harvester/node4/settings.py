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
vm_ip = 'node4:115.146.86.45'
database = ''
location = ''
admin_user = 'node4'
admin_pass = 'sentiment4'

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

#Node 4 configuration: Western AU 2, Northern Territory, South AU, Queensland
#Western AU 2:
	if quadrant == '1':
		database = 'westernau2'
		location = 'WesternAU2'
		region_quadrant = '3'
		consumer_key = '9bOaeTQMWCAs9HfSqVYAvjwYs'
		consumer_secret = 'tkdsr2faY0Uwlsc82MMSMra4qQUxhuaOcHwgw64a3x06Hxn2CV'
		access_token = '3078779083-57s7grHAHrprwNdYAlGNjujxehTzUnuqmXV7U1K'
		access_secret = 'hSJwBxwp9dSZf9Jn4rSxUFWKcXm92Ykgz2BYDA5hZi2I8'
		#Bounding Box:
		locations = [114.7926,-35.2065,122.2963,-31.8488]
	elif quadrant == '2':
		database = 'westernau2'
		location = 'WesternAU2'
		region_quadrant = '4'
		consumer_key = 'd66ZXxfysj5GPYtM1lSxSw2AN'
		consumer_secret = 'IiDg8TzNXjLGS1zIqv9wLCtK9oKfPcy4Pt5HF8a7N98jUBe83s'
		access_token = '3080228634-JYl3QFd105Cu1Ax0ds3qxsZfOZCltyiVDjwHStS'
		access_secret = 'JcomcHM3UXa3gEoyBVWvUziWiUQAagFZrS3wSa3HzFpkA'
		#Bounding Box:
		locations = [122.3073,-34.2313,128.9650,-13.5437]
#Northern Territory:
	elif quadrant == '3':
		database = 'northernt'
		location = 'NorthernTerritory'
		region_quadrant = '5'
		consumer_key = '2khe7NG3AMDRW6lGvAWfbnGpV'
		consumer_secret = 'L1m561e8zyRYkU4QM9Fgen9RfChBAjpWzRbIAik2M0VSbmYSxK'
		access_token = '3080315696-mwEFTRqvBfRodIlycsFfWU7bC5tj5xgd8pljDYZ'
		access_secret = 'qV2YsmgsK227rutJbe90PiO3a9EWIfjGKAeFmFdm1Zc2u'
		#Bounding Box:
		locations = [129.0199,-19.0301,138.0012,-14.8919]
	elif quadrant == '4':
		database = 'northernt'
		location = 'NorthernTerritory'
		region_quadrant = '6'
		consumer_key = 'cPugFljtfcCe4PBbWqmZkbmMY'
		consumer_secret = '0AtZKLleaQzeFNcKSApVIA4W2lMu6o4UqIueVTi3Sa59DWatnz'
		access_token = '3080290860-B1EXRiol0UWgYF1Rc5lXk62DII1mNFlm8myT90F'
		access_secret = 'QA1wdfASAzbtiJwvBaDK9wUNDhBpcQFhzwWLwYvQQJWOV'
		#Bounding Box:
		locations = [129.0199,-23.0092,138.0012,-19.0717]
	elif quadrant == '5':
		database = 'northernt'
		location = 'NorthernTerritory'
		region_quadrant = '7'
		consumer_key = '3NKq4mnfBTDPdNdFDeV43wbMT'
		consumer_secret = 'vnld2kAAalDdvTDXGLOPCst1yYUE5jg3iDjBKBvuh1CLcumBFT'
		access_token = '3080334600-S8eIgOJnFrTbqmBKu32CYWfUaevtCzzpyMSR8qG'
		access_secret = 'pxNN5FXaqKxoMHytb1jACcHY60MwFPEsgnWdI72DJm7c1'
		#Bounding Box:
		locations = [129.0199,-26.0066,133.4749,-23.0092]
	elif quadrant == '6':
		database = 'northernt'
		location = 'NorthernTerritory'
		region_quadrant = '8'
		consumer_key = 'TXigZAAiaPz1MdBwqIZCX76gr'
		consumer_secret = 'cwB7Ndnukc6PjNNyGj59TvzMfdrn7qewo1H2Po7FDH6dApyA43'
		access_token = '3084226170-2Mz4ViEDyCIYN8GNbpSN76biIVu6D06BRrcXa1U'
		access_secret = 'D3OAUGKZIgtvMsdKNNYjS6W5Nfhp6mu0S77tSWIw1siXD'
		#Bounding Box:
		locations = [133.4749,-26.0066,137.9847,-23.0092]
#South AU:
	elif quadrant == '7':
		database = 'southau'
		location = 'SouthAU'
		region_quadrant = '1'
		consumer_key = 'qEu0uvc3cpIBIIOkAf8IiInzc'
		consumer_secret = 'ktmix0RBHsMXqk0RLo8vo7CYdCY5izqJe1VLNIKEW0jURMO671'
		access_token = '3084266178-pESWfwN8faGc2dvrG3rvVqU3GMl72wgtVamw5A1'
		access_secret = 'F4G0HPoXcMvUn5tuZkYMvoJFouFQcBZWYbNllQqpyez0m'
		#Bounding Box:
		locations = [129.0089,-31.7436,140.9895,-25.9967]
	elif quadrant == '8':
		database = 'southau'
		location = 'SouthAU'
		region_quadrant = '2'
		consumer_key = 'f4aI6A9tyFZaucWBzrs9s5iX2'
		consumer_secret = 'K7HU47zvxg9GnMCAsXgKk8uk1XjEH6V4KLDAd7n4WURPDe719T'
		access_token = '3084311970-OU1SoS3k8kLFTWARCsebU04PGY1wPwDR4TMws0I'
		access_secret = 'pifGlMn7i9QxZSFYPlxkcJXiosK0BJjFf5HBXwX3VvDyG'
		#Bounding Box:
		locations = [131.7335,-35.1371,136.3313,-31.7436]
	elif quadrant == '9':
		database = 'southau'
		location = 'SouthAU'
		region_quadrant = '3'
		consumer_key = 'lPejcik3tt7OVsUHuCfm8Hs6D'
		consumer_secret = 'bgObRI032YLFw88OW0i671NUZY0hCEXvJfPmn3HB9rt3FChSRj'
		access_token = '3084442351-hYDj3cdkht7Inj40J3lJXPMJv0NtX40Zdk92NzG'
		access_secret = 'f39cVcheUexQm0FEf8tMwXMTaC2W81LfRvn0pK9b4dO03'
		#Bounding Box:
		locations = [136.3313,-36.1194,138.8746,-31.7529]
	elif quadrant == '10':
		database = 'southau'
		location = 'SouthAU'
		region_quadrant = '4'
		consumer_key = 'k2PzNaluEVgoV2l7ywlNdnkwp'
		consumer_secret = 'cKvXWIv0Ixb5L2qZAju7vDwpNqumhbBbc5Pb6YOkfruCha7S2g'
		access_token = '3084444528-ur0mh5APLiAsXs5LGIC8S4SFjLYQiHRp9KCFVS7'
		access_secret = 'nrBOJZipGtedXCC5fiBZAz3ArLr56zujEN7B0e8vLqZjv'
		#Bounding Box:
		locations = [138.8746,-38.1079,140.9565,-31.7529]
#Queensland
	elif quadrant == '11':
		database = 'queensland'
		location = 'Queensland'
		region_quadrant = '1'
		consumer_key = 'bBjlY498LIZemSxzr8sTou6dd'
		consumer_secret = 'Hn73xUFS1SMJvxnJf06bcHJG9HbUm5ZrkTDI0BWL4gZ4l0xZud'
		access_token = '3091637984-n7HoEl4wuuuSwz5VelnIuPFoC5ATaKSlMHRagQX'
		access_secret = 'OHajAFEA2sIV4JNKhyvIIHbjbGzPe5bwzS02kFSS3dP79'
		#Bounding Box:
		locations = [138.0177,-25.9869,141.0005,-16.1582]
	elif quadrant == '12':
		database = 'queensland'
		location = 'Queensland'
		region_quadrant = '2'
		consumer_key = 'fh6dhn5GWiBVtD2nNUmQwR77J'
		consumer_secret = 'EgTdoNln4YNHvr0Nrt4vIzgD933Nx32tydYbFfAn24wAG6QEQ6'
		access_token = '3091626528-Cvq16QO9vEudUYmKgOzJRAoTUXNL6fsEfW9FLAb'
		access_secret = 'sUjanJnnld1UcT76z9RXGjjRonBkzqBUnOCFKGrb5Vve9'
		#Bounding Box:
		locations = [141.0225,-28.9689,146.4772,-9.9975]
	elif quadrant == '13':
		database = 'queensland'
		location = 'Queensland'
		region_quadrant = '3'
		consumer_key = 'VMX4Z4vwXzSKe5rW7gpglnRnS'
		consumer_secret = 'AQDmy4xet2kI9L8Caq4VgFfd7PpTscXHlI1VCbUSukvmwrV9a2'
		access_token = '3091797908-F6WbNissShgRH0w5LcS8uA4eX92XDXfaRli9bof'
		access_secret = 'pvisYjgTjAZkHB2sdCDPqjj80dGAJ7JwfN4IhUvBJ9P0Z'
		#Bounding Box:
		locations = [146.5211,-27.4782,153.7007,-18.9857]
	elif quadrant == '14':
		database = 'queensland'
		location = 'Queensland'
		region_quadrant = '4'
		consumer_key = 'Afat0wNnVR2W8WVc69bhnkMxy'
		consumer_secret = '6K9TYur0tmUJRRpzkGPZGsOnxVgIzrx2Imats0RqC4qBJtydBU'
		access_token = '3091838461-a7bfMRWQThiLHa90JbRQ2jis18BlhKYFLTryFjp'
		access_secret = 'Grw90EyPUJ4zJH7eGpsqtjAQgPkEz6JOWRRzLFqLlvxaU'
		#Bounding Box:
		locations = [146.5211,-28.9855,153.7007,-27.4831]
