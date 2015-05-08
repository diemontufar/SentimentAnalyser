

# ENABLE_EPHEMERAL = False
# EPHEMERAL_DIRECTORY = '/mnt/'

# ENABLE_VOLUME = False
# VOLUME_DIRECTORY = '/mnt/volumename'

master = {'vm_host': ['ubuntu@115.146.86.249'],
			'vm_host_name': 'master',
			'vm_host_id': '0',
			'vm_user': 'ubuntu',
			'vm_credential_node': '/Users/diogonal/isentiment-master.pem',
			'couchdb_admin': 'master',
			'couchdb_pass': 'sentiment',
			'couchdb_URL': 'http://127.0.0.1:5984/',
			'coucdb_databases': ['australia'],
			'es_cluster_name': 'es-sentiment-cluster',
			'es_node_name': 'sentiment-master'}

node1 = {'vm_host': ['ubuntu@115.146.87.52'],
			'vm_host_name': 'node1',
			'vm_host_id': '1',
			'vm_user': 'ubuntu',
			'vm_credential_node': '/Users/diogonal/isentiment-slave.pem',
			'couchdb_admin': 'node',
			'couchdb_pass': 'sentiment',
			'couchdb_URL': 'http://127.0.0.1:5984/',
			'coucdb_databases': ['victoria','nsw','tasmania','westernau1'],
			'es_cluster_name': 'es-sentiment-cluster',
			'es_node_name': 'sentiment-shard1'}

node2 = {'vm_host': ['ubuntu@115.146.87.46'],
			'vm_host_name': 'node2',
			'vm_host_id': '2',
			'vm_user': 'ubuntu',
			'vm_credential_node': '/Users/diogonal/isentiment-slave.pem',
			'couchdb_admin': 'node',
			'couchdb_pass': 'sentiment',
			'couchdb_URL': 'http://127.0.0.1:5984/',
			'coucdb_databases': ['westernau2','southau','northernt','queensland'],
			'es_cluster_name': 'es-sentiment-cluster',
			'es_node_name': 'sentiment-shard2'}

node3 = {'vm_host': ['ubuntu@115.146.86.97'],
			'vm_host_name': 'node3',
			'vm_host_id': '3',
			'vm_user': 'ubuntu',
			'vm_credential_node': '/Users/diogonal/test1.pem',
			'couchdb_admin': 'node',
			'couchdb_pass': 'sentiment',
			'couchdb_URL': 'http://127.0.0.1:5984/',
			'coucdb_databases': ['victoria','nsw','tasmania','westernau1'],
			'es_cluster_name': 'es-sentiment-cluster',
			'es_node_name': 'sentiment-shard3'}

node4 = {'vm_host': ['ubuntu@115.146.86.45'],
			'vm_host_name': 'node4',
			'vm_host_id': '4',
			'vm_user': 'ubuntu',
			'vm_credential_node': '/Users/diogonal/test1.pem',
			'couchdb_admin': 'node',
			'couchdb_pass': 'sentiment',
			'couchdb_URL': 'http://127.0.0.1:5984/',
			'coucdb_databases': ['westernau2','southau','northernt','queensland'],
			'es_cluster_name': 'es-sentiment-cluster',
			'es_node_name': 'sentiment-shard4'}