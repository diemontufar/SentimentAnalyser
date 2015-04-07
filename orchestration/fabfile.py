# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application
# Command: fab deploy_node1

# Import Fabric's API module
from fabric.api import *
from fabric.api import sudo, env
from fabric.api import settings as fab_settings
from fabric.colors import green as _green, yellow as _yellow, blue as _blue, red as _red
from datetime import datetime

# from config import *
import time
import sys
import custom_settings as settings

host_name = ''
couchdb_admin = ''
couchdb_pass = ''
es_cluster_name = ''
es_shard_name = ''
node_type = 2 #A slave node as default
databases = []

start_time = time.time()

#############################SYSTEM CONFIGURATION################################

#Setup Security configurations
def setUpSecurity():
    with hide('output'):
        print(_yellow("Changing computer's name..."))
        print "New host name: " + host_name
        sudo("echo " + host_name +" > /etc/hostname")
        sudo("hostname -F /etc/hostname")
        modifyConfigFile('/etc/hosts','127.0.1.1' + "\t" + 'ubuntu.localhost','127.0.1.1'  + "\t" + host_name)
        print(_yellow("Finalizing modification process..."))
        print(_blue("Restarting System..."))
        reboot()
    print(_blue("System configured succesfully..."))
    print "WELCOME TO " + host_name + ", Let's proceed with configuration..."
    return True

#Upgrade & Update apt-get utility
def updateSystem():
    updating_success =  False
    with hide('output'):
        print(_yellow("Updating/Upgrading apt-get repository..."))
        sudo("add-apt-repository -y ppa:webupd8team/java") 
        res = sudo("apt-get update")
        if (res.succeeded):
            res = sudo("apt-get -y upgrade")
            if (res.succeeded):
                updating_success = True
                print(_blue('Respository updated/upgraded succesfully'))
            else:
                updating_success = False
                print(_red('Error upgrading repository!'))
        else:
            updating_success = False
            print(_red('Error updating repository!'))
    print(_yellow("Finalizing repository update/upgrade..."))
    return updating_success

#Install new  Softwre & utilities
def installNewSoftware():
    installation_success =  False
    with hide('output'):
        print(_yellow("Installing new Software..."))
        #Install NTP
        print("Preparing to install ntp utility...")
        res = sudo("apt-get -y install ntp")
        if (res.succeeded):
            installation_success = True
            print(_blue('ntp utility installed successfully'))
        else:
            installation_success = False
            print(_red('Error installing ntp utility!'))
        #Install couchDB
        print("Preparing to install couchdb...")
        res = sudo("apt-get -y install couchdb")
        if (res.succeeded):
            installation_success = True
            print(_blue('couchdb installed successfully'))
        else:
            installation_success = False
            print(_red('Error installing couchdb!'))
        #Install curl
        print("Preparing to install curl...")
        res = sudo("apt-get -y install curl")
        if (res.succeeded):
            installation_success = True
            print(_blue('curl installed successfully'))
        else:
            installation_success = False
            print(_red('Error installing curl!'))
        #Install unzip
        print("Preparing to install curl...")
        res = sudo("apt-get -y install unzip")
        if (res.succeeded):
            installation_success = True
            print(_blue('curl installed successfully'))
        else:
            installation_success = False
            print(_red('Error installing curl!'))
    print(_yellow("Finalizing installation process..."))
    return installation_success

#Configure Local timezone Date to Melbourne's
def configureLocalTimezone():
    with hide('output'):
        print(_yellow("Verifying Server's date and time..."))
        if not isServerDateCorrect():
            print(_yellow("Changing timezone to Melbourne..."))
            run('echo "Australia/Melbourne" | sudo tee /etc/timezone')
            sudo("dpkg-reconfigure --frontend noninteractive tzdata")
            print(_yellow("Synchronizing with UTC through NTP..."))
            modifyConfigFile('/etc/ntp.conf','server ntp','server pool.ntp.org')
            print(_yellow("Restarting ntp service..."))
            sudo("service ntp stop")
            sudo("ntpdate pool.ntp.org")
            sudo("service ntp start")
            print(_yellow("Verifying date again..."))
            current_date = run("date")
            print(_blue('Date modified successfully: ' + str(current_date)))
        print(_yellow("Finalizing Server's date verification..."))
    return True

#Verify Python version
def verifyPythonVersion():
    verification_sucess = False
    with hide('output'):
        print(_yellow("Verifying python version..."))
        version = run("python --version")
        print "Current version: " + str(version)
        res = version.split(" ")
        if ('3' in res[1]):
            print(_blue('Is the correct version, path modification will be omitted'))
        else:
            res1 = sudo("rm /usr/bin/python")
            if (res1.succeeded):
                print(_blue('Previous python symlink removed'))
                verification_sucess = True
            else:
                print(_red('Error during symlink romove process'))
                verification_sucess = False
            res2 = sudo("ln -s /usr/bin/python3.4 /usr/bin/python")
            if (res2.succeeded):
                print(_blue('Newer python symlink done'))
                print(_green('New python version: 3.4'))
                verification_sucess = True
            else:
                print(_red('Error during symlink creation'))
                verification_sucess = False
    print(_yellow("Finalizing Python version verification..."))
    return verification_sucess

#Create working directory:
def createWorkingDirectory():
    with hide('output'):
        print(_yellow("Creating working directory..."))
        sudo("mkdir SentimentAnalyser")
        sudo("chmod -R 777 SentimentAnalyser")
        with cd("SentimentAnalyser"):
            sudo("mkdir resources")
            with cd("resources"):
                sudo("mkdir servers")
                sudo("chmod -R 777 servers")
        print(_blue('Working directory created succesfully'))
        return True

#Install python modules:
def installPythonModules():
    with hide('output'):
        print(_yellow("Installing Python modules..."))
        with cd("~/SentimentAnalyser/resources"):
            print "Proceeding to Install: pip"
            res = sudo("wget https://bootstrap.pypa.io/get-pip.py")
            if res.succeeded:
                sudo("python get-pip.py")
            else:
                print(_red('Error downloading get-pip.py file!'))
                return False
            print "Proceeding to Install: tweepy"
            res = sudo("pip install tweepy")
            if res.failed:
                print(_red('Error installing tweepy!'))
                return False
            print "Proceeding to Install: couchdb-python"
            res = sudo("wget https://github.com/djc/couchdb-python/archive/master.zip")
            if res.succeeded:
                sudo("unzip master")
                with cd("couchdb-python-master"):
                    res = sudo("python setup.py install")
                    if res.failed:
                        print(_red('Error installing couchdb-python'))
                        return False
            else:
                print(_red('Error downloading couchdb-python file!'))
                return False
            sudo("rm master.zip")
            sudo("rm -R couchdb-python-master/")
            sudo("rm get-pip.py")
    print(_yellow("Finalizing Python modules installation..."))
    return True

###################################################################################

####################################COUCHDB SETUP##################################

#Setup CouchDB
def setupCoucDB():
    with hide('output'):
        print(_yellow("Starting couchdb process..."))
        res = run("curl http://127.0.0.1:5984/")
        print "CouchDB says: " + str(res)
        print(_yellow("Proceeding to open ports for couchDB..."))  
#Modify couchdb configuration to accept remote connections
#change the bind_address from 127.0.0.1 to 0.0.0.0 in /etc/couchdb/default.ini. Then restart the service and try again.
        modifyConfigFile('/etc/couchdb/default.ini','bind_address = 127','bind_address = 0.0.0.0')        
        res = sudo("restart couchdb") 
        if res.failed:
            print(_red('Error reinitializing CouchDB server'))
            return False
    print(_yellow("Finalizing couchDB initialization..."))
    return True

#Move files from local to remote
def moveFiles(from_dir,to_dir):
    with hide('output'):
        print(_yellow("Starting to copy files from local to " + host_name + "..."))
        res = put(from_dir, to_dir)
        if res.failed:
            print(_red("Error copyting files from: " + from_dir + ", to: " + to_dir))
            return False
    return True

#Configure Security in CouchDB
def configureCouchDBSecurity():
    success = False
    with hide('output'):
        print(_yellow("Configuring security in CouchDB instance at " + host_name + "..."))
        comm = 'curl -X PUT http://127.0.0.1:5984/_config/admins/' + couchdb_admin + ' -d ' + "'" + '"' + couchdb_pass + '"' + "'"
        res = run(comm)
        if res.succeeded:
            print "CouchDB says: " + res
            print(_blue("Admin user created successfully"))
            success = True
        else:
            print(_red("Error while creating user"))
            success = False
    print(_yellow("Finalizing CouchDB security configuration..."))
    return success

#Create couchDB Data Bases:
def createNodeDatabases(databases):
    success = False
    with hide('output'):
        print(_yellow("Creating databases in couchDB instance at " + host_name + "..."))
        for db in databases:
            comm = 'curl -X PUT http://' + couchdb_admin + ":" + couchdb_pass + '@127.0.0.1:5984/' + db
            res = run(comm)
            if res.succeeded:
                print "CouchDB says: " + res
                print(_blue("Database: " + db + ", created successfully"))
                success = True
            else:
                print(_red("Error while creating Database: " + db))
                success = False
    print(_yellow("Finalizing CouchDB database creation..."))
    return success

#Change couchdb database_dir to store data on ephemeral disk 
def migrateDBToStorage(new_directory):
    success = False
    with hide('output'):
        print(_yellow("Starting database migration to: " + new_directory))
        print(_yellow("This may take a few seconds, Relax!"))
        print "Copying databases..."
        res = sudo("cp -R /var/lib/couchdb/ " + new_directory)
        if res.failed:
            print(_red("Error while copying databases"))
            return False
        print "Changing owner"
        res = sudo("chown -R couchdb:couchdb " + new_directory)
        if res.failed:
            print(_red("Error while changing owner"))
            return False
        print "Changing permissions"
        res = sudo("chmod -R 777 " + new_directory)
        if res.failed:
            print(_red("Error while giving permissions"))
            return False
        print "Updating new directory con local.ini"
        res = run('curl -X PUT http://master:sentiment@127.0.0.1:5984/_config/couchdb/database_dir -d '+ '"' + new_directory + '"')
        if res.failed:
            print(_red("Error while updating local.ini"))
            return False
        print "Restarting service..."
        res = sudo("service couchdb restart")
        if res.failed:
            print(_red("Error while restarting couchdb"))
            return False
        print(_yellow("Finalizing database migration, please check Futon..."))
        return True

###################################################################################

#######################################ELASTIC SEARCH##############################

#Install Oracle Java
def installJava():
    success = False
    with hide('output'):
        print(_yellow("Installing Java (This may take a few minutes)..."))
        res = sudo("echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections")
        if res.succeeded:
            sudo("echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections")
            res = sudo("apt-get -y install oracle-java7-installer")
            if res.succeeded:
                res = sudo("apt-get -y install oracle-java7-set-default")
                if res.succeeded:
                    print(_blue("Java installed successfully..."))
                    java_version = run("java -version")
                    print "The new Java version is:"
                    print str(java_version)
                    success = True
                else:
                    print(_red('Error while setting up Java!')) 
                    success = False
            else:
                print(_red('Error while installing Java!')) 
                success = False
        else:
            print(_red('Error while setting up Oracle aggreement!'))
            success = False
    print(_yellow("Finalizing Java Installation..."))
    return success

#Install ElasticSearch
# def installTestElasticSearch():
#     success = False
#     with hide('output'):
#         print(_yellow("Starting to install ElasticSearch..."))
#         with cd("~/SentimentAnalyser/resources/servers/"):
#             res = sudo("wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.4.tar.gz")
#             if res.succeeded:
#                 sudo("tar xzf elasticsearch-1.4.4.tar.gz")
#                 with cd("elasticsearch-1.4.4"):
#                     print(_yellow("Proceeding to install es-river-couchdb..."))
#                     res = sudo("bin/plugin install elasticsearch/elasticsearch-river-couchdb/2.4.2")
#                     if res.succeeded:
#                         print(_blue("elasticsearch-river-couchdb successfully installed."))
#                         print(_yellow("Proceeding to install BigDesk plugin..."))
#                         res = sudo("bin/plugin -install lukas-vlcek/bigdesk")
#                         if res.succeeded:
#                             print(_blue("bigdesk successfully installed."))
#                             print(_yellow("Proceeding to install elasticsearch-head plugin..."))
#                             res = sudo("bin/plugin -install mobz/elasticsearch-head")
#                             if res.succeeded:
#                                 success = True
#                                 print(_blue("elasticsearch-head successfully installed."))
#                             else:
#                                 print(_red("Error installing elasticsearch-head!"))
#                                 success = False
#                         else:
#                             print(_red("Error installing bigdesk!"))
#                             success = False
#                     else:
#                         print(_red("Error installing elasticsearch-river-couchdb!"))
#                         success = False
#             res = sudo("rm -R elasticsearch-1.4.4.tar.gz")
#             if res.succeeded:
#                 print(_blue("elasticsearch-1.4.4.tar.gz successfully removed."))
#             else:
#                 print "WARINING: Error removing elasticsearch-1.4.4.tar.gz, do it manually!"
#     return success

#Install ElasticSearch
def installElasticSearch():
    with hide('output'):
        print(_yellow("Starting to install ElasticSearch..."))
        with cd("~/SentimentAnalyser/resources/"):
            res = sudo("wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.5.0.deb")
            if res.failed:
                return False
            res = sudo("dpkg -i elasticsearch-1.5.0.deb")
            if res.failed:
                return False
            res = sudo("rm elasticsearch-1.5.0.deb")
            if res.failed:
                return False
            res = sudo("/etc/init.d/elasticsearch start")
            if res.failed:
                return False
            time.sleep(15)
            test = run("curl http://localhost:9200")
            if test.succeeded:
                print "ElasticSearch says:"
                print test
            else:
                print(_red("Error curling ElasticSearch"))
                return False
            res = sudo("/etc/init.d/elasticsearch stop")
            time.sleep(5)
            if res.failed:
                return False
        print(_blue("ElasticSearch successfully installed and was stopped in order to configure it first"))
        print(_yellow("Finalizing ElasticSearch intallation..."))
        return True

#Install ES plugins
def installESplugins():
    success = False
    with hide('output'):
        print(_yellow("Starting to install ElasticSearch plugins..."))
        with cd("/usr/share/elasticsearch/bin/"):
            print(_yellow("Proceeding to install es-river-couchdb..."))
            res = sudo("./plugin -install elasticsearch/elasticsearch-river-couchdb/2.4.2")
            if res.succeeded:
                print(_blue("elasticsearch-river-couchdb successfully installed."))
                print(_yellow("Proceeding to install BigDesk plugin..."))
                res = sudo("./plugin -install lukas-vlcek/bigdesk")
                if res.succeeded:
                    print(_blue("bigdesk successfully installed."))
                    print(_yellow("Proceeding to install elasticsearch-head plugin..."))
                    res = sudo("./plugin -install mobz/elasticsearch-head")
                    if res.succeeded:
                        success = True
                        print(_blue("elasticsearch-head successfully installed."))
                    else:
                        print(_red("Error installing elasticsearch-head!"))
                        success = False
                else:
                    print(_red("Error installing bigdesk!"))
                    success = False
            else:
                print(_red("Error installing elasticsearch-river-couchdb!"))
                success = False

    print(_yellow("Finalizing ElasticSearch plugins intallation..."))
    return success

#Configuration of yml files for each node of the ElasticSearch Cluster
def configureES(node_type):
    path_to_data = "/mnt/elasticsearch/" #just in case you want to use ephemeral disk or extra volume
    enable_path_to_data = False
    sucess = False
    with hide('output'):
        if node_type=='master':
            print(_yellow("Configuring coordinator..."))
            with cd("/etc/elasticsearch/"):
                uncommentMultipleLinesNo("elasticsearch.yml",['32','40','64','65'])
                modifyConfigFile("elasticsearch.yml","cluster.name: ","cluster.name: " + es_cluster_name)
                modifyConfigFile("elasticsearch.yml","node.name: ",'node.name: "'+ es_shard_name+'"')
                if enable_path_to_data:
                    sudo("mkdir " + path_to_data)
                    sudo("chown -R elasticsearch:elasticsearch " + path_to_data)
                    sudo("chmod -R 777 " + path_to_data)
                    uncommentMultipleLinesNo("elasticsearch.yml",['149'])
                    modifyConfigFile("elasticsearch.yml","path.data: ","path.data: " + path_to_data)
                    print(_blue("Coordinator: " + es_shard_name + ", now has new path to data: " + path_to_data))
                print(_blue("Coordinator: " + es_shard_name + ", configured succesfully"))
        elif node_type=='shard':
            print(_yellow("Configuring shard..."))
            with cd("/etc/elasticsearch/"):
                uncommentMultipleLinesNo("elasticsearch.yml",['32','40','58','59'])
                modifyConfigFile("elasticsearch.yml","cluster.name: ","cluster.name: " + es_cluster_name)
                modifyConfigFile("elasticsearch.yml","node.name: ",'node.name: "'+es_shard_name+'"')
                if enable_path_to_data:
                    sudo("mkdir " + path_to_data)
                    sudo("chown -R elasticsearch:elasticsearch " + path_to_data)
                    sudo("chmod -R 777 " + path_to_data)
                    uncommentMultipleLinesNo("elasticsearch.yml",['149'])
                    modifyConfigFile("elasticsearch.yml","path.data: ","path.data: " + path_to_data)
                    print(_blue("Coordinator: " + es_shard_name + ", now has new path to data: " + path_to_data))
                print(_blue("Shard: " + es_shard_name + ", configured succesfully"))
    return True

#Start Elastic search
def startES():
    with hide('output'):
        print(_yellow("Starting ElasticSearch..."))
        res = sudo("/etc/init.d/elasticsearch start")
        if res.failed:
            print(_red("ElasticSearch is cannot start"))
            return False
        else:
            time.sleep(20)
            test = run("curl http://localhost:9200")
            print "ElasticSearch says:"
            print test
        print(_blue("ElasticSearch is now running on: http://localhost:9200"))
        return True

#Steps to pleyoy ElasticSearch Based on instance_type: 1: master, 2: shard
def deployElasticSearch(instance_type):
    res = installElasticSearch()
    if not res:
        print(_red("Something went wrong while installing ElasticSearch, please revise the process..."))
        return False
    res = installESplugins()
    if not res:
        print(_red("Something went wrong while installing ElasticSearch plugins, please revise the process..."))
        return False
    if instance_type==1:
        res = configureES('master')
        if not res:
            print(_red("Something went wrong while configuring ElasticSearch, please revise the process..."))
            return False
    else:
        res = configureES('shard')
        if not res:
            print(_red("Something went wrong while configuring ElasticSearch, please revise the process..."))
            return False
    res = startES()
    if not res:
        print(_red("Something went wrong while starting ElasticSearch, please revise the process..."))
        return False
    return True

###################################################################################

##########################################UTILS####################################

#Modify any config File
def modifyConfigFile(input_file,key,new_value):
    match = 's/^\(' + key + '\).*/' + new_value + '/'
    comm = 'sed -i.bak ' + "'" + match + "' " + input_file
    sudo(comm)

#Uncomment any config file which uses # as comment
def uncommentLine(input_file,key):
    match = '/' + key + '/ s/# *//'
    comm = 'sed -i.bak ' + "'" + match + "' " + input_file
    sudo(comm)

#Uncomment multiple lines which uses # as comment
def uncommentMultipleLines(input_file,keys):
    for key in keys:
        match = '/' + key + '/ s/# *//'
        comm = 'sed -i.bak ' + "'" + match + "' " + input_file
        sudo(comm)

#Comment a line given the number of the line
def commentLineNo(input_file,line):
    match =  str(line)+' s/^/#/'
    comm = 'sed -i.bak ' + "'" + match + "' " + input_file
    sudo(comm)

#Uncomment multiple lines given the list of line numbers
def commentMultipleLinesNo(input_file,lines):
    for line in lines:
            match =  str(line)+' s/^/#/'
            comm = 'sed -i.bak ' + "'" + match + "' " + input_file
            sudo(comm)

#Uncomment a line given the number of the line
def uncommentLineNo(input_file,line):
    match =  str(line)+' s/# *//'
    comm = 'sed -i.bak ' + "'" + match + "' " + input_file
    sudo(comm)

#Uncomment multiple lines given the list of line numbers
def uncommentMultipleLinesNo(input_file,lines):
    for line in lines:
            match =  str(line)+' s/# *//'
            comm = 'sed -i.bak ' + "'" + match + "' " + input_file
            sudo(comm)

#Get the difference in minutes between dates
def dateDiff(date1,date2):
    daysDiff = abs((date2-date1).days)
    minutesDiff = daysDiff * 24 * 60
    if minutesDiff < 5:
        return True
    return False

#Get the Server's date
def getServerDate():
    my_date = run("date")
    print 'Current Date: ' + str(my_date)
    return str(my_date)

#Verify if Server's date is configured considering localzone
def isServerDateCorrect():
    server_date = datetime.strptime(getServerDate(), '%a %b %d %I:%M:%S UTC %Y')
    if dateDiff(datetime.now(),server_date):
        return True
    return False

############################HARVESTING PROCESS###################################

#Check harvesting status
def checkHarvestingStatus():
    success = False
    with hide('output'):
        print(_yellow("Checking harvesting process on: " + env.hosts[0]))
        res = sudo("ps -Af | grep generic_harvester.py | grep -v grep || generic_harvester.py")
        if res.succeeded:
            print(_blue("QUADRANTS CURRENTLY HARVESTING:"))
            print(_blue("_____________________________________________"))
            print res
        else:
            print(_red("Something went wrong when retrieving harvesting information"))
            return False
    return True

#Stop Harvesting Process in all Quadrants
def stopHarvestingProcess():
    with hide('output'):
        with cd("~/SentimentAnalyser/harvester/"):
            print(_yellow("Stoping harvesting process on: " + env.hosts[0]))
            res = sudo("./stop_harvesting.sh")
            if res.succeeded:
                print(_blue("Harvesting process has stopped by the admin."))
                print res
            else:
                print(_red("Something went wrong when stopping harvesting process"))
                return False
    return True

#Start Hrvesting process in all Quadrants
def startHarvestingProcess():
   with hide('output'):
        with cd("~/SentimentAnalyser/harvester/"):
            print(_yellow("Starting harvesting process on: " + env.hosts[0]))
            res = sudo("./start_harvesting.sh")
            if res.succeeded:
                print(_blue("Harvesting process has started by the admin."))
            else:
                print(_red("Something went wrong when starting harvesting process"))
                return False
        return True

#Start Harvesting process on crtain Quadrant, please specify quadrant before running this method
def startHarvestingOnQuadrant():
    quadrant = 1 # <------SPECIFY!!!
    with hide('output'):
        print(_yellow("Starting harvesting process on: " + env.hosts[0] + ", Quadrant: " + quadrant))
        with cd("~/SentimentAnalyser/harvester/"):
            res = sudo("nohup python generic_harvester.py " + quadrant + " 2>1 &")
            if res.succeeded:
                print(_blue("Harvesting process has started by the admin."))
            else:
                print(_red("Something went wrong when starting harvesting process"))
                return False
    return True

###################################################################################

##################################INITIALIZATION###################################

def master():

    global host_name
    global couchdb_admin
    global couchdb_pass
    global es_cluster_name
    global es_shard_name
    global node_type
    global databases

    env.hosts = settings.master['vm_host']
    env.user   = settings.master['vm_user']
    env.key_filename = settings.master['vm_credential_node']
    host_name = settings.master['vm_host_name']
    couchdb_admin = settings.master['couchdb_admin']
    couchdb_pass = settings.master['couchdb_pass']
    es_cluster_name = settings.master['es_cluster_name']
    es_shard_name = settings.master['es_node_name']
    node_type = 1
    databases = settings.master['coucdb_databases']


def node1():

    global host_name
    global couchdb_admin
    global couchdb_pass
    global es_cluster_name
    global es_shard_name
    global node_type
    global databases

    env.hosts = settings.node1['vm_host']
    env.user   = settings.node1['vm_user']
    env.key_filename = settings.node1['vm_credential_node']
    host_name = settings.node1['vm_host_name']
    couchdb_admin = settings.node1['couchdb_admin']
    couchdb_pass = settings.node1['couchdb_pass']
    es_cluster_name = settings.node1['es_cluster_name']
    es_shard_name = settings.node1['es_node_name']
    node_type = 2
    databases = settings.node1['coucdb_databases']


def node2():

    global host_name
    global couchdb_admin
    global couchdb_pass
    global es_cluster_name
    global es_shard_name
    global node_type
    global databases

    env.hosts = settings.node2['vm_host']
    env.user   = settings.node2['vm_user']
    env.key_filename = settings.node2['vm_credential_node']
    host_name = settings.node2['vm_host_name']
    couchdb_admin = settings.node2['couchdb_admin']
    couchdb_pass = settings.node2['couchdb_pass']
    es_cluster_name = settings.node2['es_cluster_name']
    es_shard_name = settings.node2['es_node_name']
    node_type = 2
    databases = settings.node2['coucdb_databases']

def node3():

    global host_name
    global couchdb_admin
    global couchdb_pass
    global es_cluster_name
    global es_shard_name
    global node_type
    global databases

    env.hosts = settings.node3['vm_host']
    env.user   = settings.node3['vm_user']
    env.key_filename = settings.node3['vm_credential_node']
    host_name = settings.node3['vm_host_name']
    couchdb_admin = settings.node3['couchdb_admin']
    couchdb_pass = settings.node3['couchdb_pass']
    es_cluster_name = settings.node3['es_cluster_name']
    es_shard_name = settings.node3['es_node_name']
    node_type = 2
    databases = settings.node3['coucdb_databases']

def node4():

    global host_name
    global couchdb_admin
    global couchdb_pass
    global es_cluster_name
    global es_shard_name
    global node_type
    global databases

    env.hosts = settings.node4['vm_host']
    env.user   = settings.node4['vm_user']
    env.key_filename = settings.node4['vm_credential_node']
    host_name = settings.node4['vm_host_name']
    couchdb_admin = settings.node4['couchdb_admin']
    couchdb_pass = settings.node4['couchdb_pass']
    es_cluster_name = settings.node4['es_cluster_name']
    es_shard_name = settings.node4['es_node_name']
    node_type = 2
    databases = settings.node4['coucdb_databases']

###################################################################################

#####################################MAIN METHOD###################################

#Deploy Server
def deploy():
    if env.hosts =='':
        print(_red('Configuration is not defined!'))
        sys.exit()
    else:
        print(_yellow("STARTING DEPLOYMENT PROCESS IN HOST: " + env.hosts[0]))
        print(_yellow("-------------------------------------------------------------"))
        #0. Configure Security System
        # res = setUpSecurity()
        # if not res:
        #     print(_red('Something went wrong while configuring security, please revise the process...'))
        #     sys.exit()
        # #1. Update/Upgrade System
        # res = updateSystem()
        # if not res:
        #     print(_red('Something went wrong while updating/upgrading system, please revise the process...'))
        #     sys.exit()
        # #2. Install new Software
        # res = installNewSoftware()
        # if not res:
        #     print(_red('Something went wrong while installing new Software, please revise the process...'))
        #     sys.exit()
        # #3. Configure Server's Date and Time
        # res = configureLocalTimezone()
        # if not res:
        #     print(_red("Something went wrong while verifying Server's Date, please revise the process..."))
        #     sys.exit()
        # #4. Configure Python version
        # res = verifyPythonVersion()
        # if not res:
        #     print(_red("Something went wrong while verifying Python version, please revise the process..."))
        #     sys.exit()
        # #5. Create Working Directory
        # res = createWorkingDirectory()
        # if not res:
        #     print(_red("Something went wrong while creating working directory, please revise the process..."))
        #     sys.exit()
        # #6. Install Python modules
        # res = installPythonModules()
        # if not res:
        #     print(_red("Something went wrong while installing python modules, please revise the process..."))
        #     sys.exit()
        # #7. Set up CoucDB
        # res = setupCoucDB()
        # if not res:
        #     print(_red("Something went wrong while setting up couchDB, please revise the process..."))
        #     sys.exit()
        # #8. Configure CouchDB security
        # time.sleep(5) #wait until couchDB is initiated
        # res = configureCouchDBSecurity()
        # if not res:
        #     print(_red("Something went wrong while configuring couchDB security, please revise the process..."))
        #     sys.exit()
        # #Migrate databases to new storage
        # res = migrateDBToStorage("/mnt/couchdb/")
        # if not res:
        #     print(_red("Something went wrong while migrating databases, please revise the process..."))
        #     sys.exit()
        # #9. CouchDB databases creation
        # res = createNodeDatabases(databases)
        # if not res:
        #     print(_red("Something went wrong while creating databases, please revise the process..."))
        #     sys.exit()
        # #10: Copy Harvester directory to remote server:
        # res = moveFiles('~/Desktop/harvester/','~/SentimentAnalyser/')
        # with cd("~/SentimentAnalyser"):
        #     sudo("chmod -R 777 harvester")
        # if not res:
        #     print(_red("Something went wrong while copyting files, please revise the process..."))
        #     sys.exit()
        # #11: Run harvesting process
        # with cd("~/SentimentAnalyser/harvester/"):
        #     res = run("./start_harvester.sh")
        #     if not res:
        #         print(_red("Something went wrong while running harvesting process, please revise the process..."))
        #         sys.exit()
        #12: Install Java 
        # res = installJava()
        # if not res:
        #     print(_red("Something went wrong while installing Java, please revise the process..."))
        #     sys.exit()       
        #13: Deploy elasticsearch
        # res = deployElasticSearch(node_type)
        # if not res:
        #     print(_red("Something went wrong while deploying ElasticSearch, please revise the process..."))
        #     sys.exit()
    end_time = (time.time() - start_time)/60
    print("Installation process took: %.2f minutes" % end_time)