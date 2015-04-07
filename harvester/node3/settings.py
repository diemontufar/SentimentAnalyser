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
vm_ip = 'node3:115.146.86.97'
database = ''
location = ''
admin_user = 'node3'
admin_pass = 'sentiment3'

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

#Node 3 configuration: Victoria, Tasmania, NSW, Western AU 1
#Victoria:
	if quadrant == '1':
		database = 'victoria'
		location = 'Victoria'
		region_quadrant = '1'
		consumer_key = '9bOaeTQMWCAs9HfSqVYAvjwYs'
		consumer_secret = 'tkdsr2faY0Uwlsc82MMSMra4qQUxhuaOcHwgw64a3x06Hxn2CV'
		access_token = '3078779083-57s7grHAHrprwNdYAlGNjujxehTzUnuqmXV7U1K'
		access_secret = 'hSJwBxwp9dSZf9Jn4rSxUFWKcXm92Ykgz2BYDA5hZi2I8'
		#Bounding Box:
		locations = [140.9675,-38.5435,142.7199,-33.9720]  
	elif quadrant == '2':
		database = 'victoria'
		location = 'Victoria'
		region_quadrant = '2'
		consumer_key = 'd66ZXxfysj5GPYtM1lSxSw2AN'
		consumer_secret = 'IiDg8TzNXjLGS1zIqv9wLCtK9oKfPcy4Pt5HF8a7N98jUBe83s'
		access_token = '3080228634-JYl3QFd105Cu1Ax0ds3qxsZfOZCltyiVDjwHStS'
		access_secret = 'JcomcHM3UXa3gEoyBVWvUziWiUQAagFZrS3wSa3HzFpkA'
		#Bounding Box:
		locations = [142.7308,-38.8989,145.0544,-35.4262]  
	elif quadrant == '3':
		database = 'victoria'
		location = 'Victoria'
		region_quadrant = '3'
		consumer_key = '2khe7NG3AMDRW6lGvAWfbnGpV'
		consumer_secret = 'L1m561e8zyRYkU4QM9Fgen9RfChBAjpWzRbIAik2M0VSbmYSxK'
		access_token = '3080315696-mwEFTRqvBfRodIlycsFfWU7bC5tj5xgd8pljDYZ'
		access_secret = 'qV2YsmgsK227rutJbe90PiO3a9EWIfjGKAeFmFdm1Zc2u'
		#Bounding Box:
		locations = [145.0544,-39.1549,148.2020,-35.7746]  
	elif quadrant == '4':
		database = 'victoria'
		location = 'Victoria'
		region_quadrant = '4'
		consumer_key = 'cPugFljtfcCe4PBbWqmZkbmMY'
		consumer_secret = '0AtZKLleaQzeFNcKSApVIA4W2lMu6o4UqIueVTi3Sa59DWatnz'
		access_token = '3080290860-B1EXRiol0UWgYF1Rc5lXk62DII1mNFlm8myT90F'
		access_secret = 'QA1wdfASAzbtiJwvBaDK9wUNDhBpcQFhzwWLwYvQQJWOV'
		#Bounding Box:
		locations = [148.2430,-37.8308,150.0093,-36.7842]
#Tasmania:
	elif quadrant == '5':
		database = 'tasmania'
		location = 'Tasmania'
		region_quadrant = '5'
		consumer_key = '3NKq4mnfBTDPdNdFDeV43wbMT'
		consumer_secret = 'vnld2kAAalDdvTDXGLOPCst1yYUE5jg3iDjBKBvuh1CLcumBFT'
		access_token = '3080334600-S8eIgOJnFrTbqmBKu32CYWfUaevtCzzpyMSR8qG'
		access_secret = 'pxNN5FXaqKxoMHytb1jACcHY60MwFPEsgnWdI72DJm7c1'
		#Bounding Box:
		locations = [145.1423,-43.6036,146.2684,-42.1228]
	elif quadrant == '6':
		database = 'tasmania'
		location = 'Tasmania'
		region_quadrant = '6'
		consumer_key = 'TXigZAAiaPz1MdBwqIZCX76gr'
		consumer_secret = 'cwB7Ndnukc6PjNNyGj59TvzMfdrn7qewo1H2Po7FDH6dApyA43'
		access_token = '3084226170-2Mz4ViEDyCIYN8GNbpSN76biIVu6D06BRrcXa1U'
		access_secret = 'D3OAUGKZIgtvMsdKNNYjS6W5Nfhp6mu0S77tSWIw1siXD'
		#Bounding Box:
		locations = [146.2684,-43.6712,146.8892,-42.1228] 
	elif quadrant == '7':
		database = 'tasmania'
		location = 'Tasmania'
		region_quadrant = '7'
		consumer_key = 'qEu0uvc3cpIBIIOkAf8IiInzc'
		consumer_secret = 'ktmix0RBHsMXqk0RLo8vo7CYdCY5izqJe1VLNIKEW0jURMO671'
		access_token = '3084266178-pESWfwN8faGc2dvrG3rvVqU3GMl72wgtVamw5A1'
		access_secret = 'F4G0HPoXcMvUn5tuZkYMvoJFouFQcBZWYbNllQqpyez0m'
		#Bounding Box:
		locations = [146.8892,-43.6712,147.4879,-42.1228]
	elif quadrant == '8':
		database = 'tasmania'
		location = 'Tasmania'
		region_quadrant = '8'
		consumer_key = 'f4aI6A9tyFZaucWBzrs9s5iX2'
		consumer_secret = 'K7HU47zvxg9GnMCAsXgKk8uk1XjEH6V4KLDAd7n4WURPDe719T'
		access_token = '3084311970-OU1SoS3k8kLFTWARCsebU04PGY1wPwDR4TMws0I'
		access_secret = 'pifGlMn7i9QxZSFYPlxkcJXiosK0BJjFf5HBXwX3VvDyG'
		#Bounding Box:
		locations = [147.4879,-43.2965,148.3833,-42.1228]
#NSW
	elif quadrant == '9':
		database = 'nsw'
		location = 'NSW'
		region_quadrant = '1'
		consumer_key = 'lPejcik3tt7OVsUHuCfm8Hs6D'
		consumer_secret = 'bgObRI032YLFw88OW0i671NUZY0hCEXvJfPmn3HB9rt3FChSRj'
		access_token = '3084442351-hYDj3cdkht7Inj40J3lJXPMJv0NtX40Zdk92NzG'
		access_secret = 'f39cVcheUexQm0FEf8tMwXMTaC2W81LfRvn0pK9b4dO03'
		#Bounding Box:
		locations = [141.0335,-34.0403,148.3284,-29.0122]
	elif quadrant == '10':
		database = 'nsw'
		location = 'NSW'
		region_quadrant = '2'
		consumer_key = 'k2PzNaluEVgoV2l7ywlNdnkwp'
		consumer_secret = 'cKvXWIv0Ixb5L2qZAju7vDwpNqumhbBbc5Pb6YOkfruCha7S2g'
		access_token = '3084444528-ur0mh5APLiAsXs5LGIC8S4SFjLYQiHRp9KCFVS7'
		access_secret = 'nrBOJZipGtedXCC5fiBZAz3ArLr56zujEN7B0e8vLqZjv'
		#Bounding Box:
		locations = [144.3953,-35.7948,148.3284,-34.0403]
	elif quadrant == '11':
		database = 'nsw'
		location = 'NSW'
		region_quadrant = '3'
		consumer_key = 'bBjlY498LIZemSxzr8sTou6dd'
		consumer_secret = 'Hn73xUFS1SMJvxnJf06bcHJG9HbUm5ZrkTDI0BWL4gZ4l0xZud'
		access_token = '3091637984-n7HoEl4wuuuSwz5VelnIuPFoC5ATaKSlMHRagQX'
		access_secret = 'OHajAFEA2sIV4JNKhyvIIHbjbGzPe5bwzS02kFSS3dP79'
		#Bounding Box:
		locations = [148.3503,-36.8326,150.8937,-29.0122]
	elif quadrant == '12':
		database = 'nsw'
		location = 'NSW'
		region_quadrant = '4'
		consumer_key = 'fh6dhn5GWiBVtD2nNUmQwR77J'
		consumer_secret = 'EgTdoNln4YNHvr0Nrt4vIzgD933Nx32tydYbFfAn24wAG6QEQ6'
		access_token = '3091626528-Cvq16QO9vEudUYmKgOzJRAoTUXNL6fsEfW9FLAb'
		access_secret = 'sUjanJnnld1UcT76z9RXGjjRonBkzqBUnOCFKGrb5Vve9'
		#Bounding Box:
		locations = [150.8992,-34.5305,153.6677,-28.1051]
#Western AU 1:
	elif quadrant == '13':
		database = 'westernau1'
		location = 'WesternAU1'
		region_quadrant = '1'
		consumer_key = 'VMX4Z4vwXzSKe5rW7gpglnRnS'
		consumer_secret = 'AQDmy4xet2kI9L8Caq4VgFfd7PpTscXHlI1VCbUSukvmwrV9a2'
		access_token = '3091797908-F6WbNissShgRH0w5LcS8uA4eX92XDXfaRli9bof'
		access_secret = 'pvisYjgTjAZkHB2sdCDPqjj80dGAJ7JwfN4IhUvBJ9P0Z'
		#Bounding Box:
		locations = [112.4415,-26.8794,122.2963,-16.5564]
	elif quadrant == '14':
		database = 'westernau1'
		location = 'WesternAU1'
		region_quadrant = '2'
		consumer_key = 'Afat0wNnVR2W8WVc69bhnkMxy'
		consumer_secret = '6K9TYur0tmUJRRpzkGPZGsOnxVgIzrx2Imats0RqC4qBJtydBU'
		access_token = '3091838461-a7bfMRWQThiLHa90JbRQ2jis18BlhKYFLTryFjp'
		access_secret = 'Grw90EyPUJ4zJH7eGpsqtjAQgPkEz6JOWRRzLFqLlvxaU'
		#Bounding Box:
		locations = [113.4962,-31.8441,122.2963,-26.8892]
