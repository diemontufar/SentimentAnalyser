Orchestration Module
===================

- - - - 

This module is in charge of automating deployment process using a prowerful tool called Ansible. It will execute all the steps necessary to set up and configure all the modules, dependencies and software needed for this Project. Then (depending on your cloud instances configuration and availability) you will be able to have a distributed enviroment with technologies such as elascticsearch, couchdb as well as a framework for harvesting tweets from the Twitter API, in few minutes. 

## Requirements

This module assumes the existence of at least one remote server/instance which will serve as a master node so called 'coordinator'. Possible configurations can scale perfectly depending on the amount of slave nodes so called 'shards'. Thus, If you have 2 instances available on the cloud or somewhere else, you can execute this Ansible program to configure for you: 1 coordinator/1 shard or if you have more resources: up to N coordinators/M shards.

This version of the orchestrer module only deploys the application on Ubuntu linux-based systems.

## Considerations

There are two possible configurations as mentioned above:

* **Coordinator (master)**: Configured as an elasticsearch coordinator node. Runs the main instance of a couchdb server and will serve the web module on apache2. Although it is not meant to be executing a harvesting process, it can be configured to do so.
* **Harvester (shard)**: Configured as an elasticsearch shard node. Runs an instance of a couchdb server and will be executing one or more harvesting processes depending on your configuration in the harvester module.

Ansible cannot decide which configuration suits the best for you, as it depends on available resources and different possible configurations for each module of this Project. By default you could deploy just a Coordinator node and configure it as a harvester as well. Keeping in mind that this means that we may be overloading our single instance with several servers and processes running on it. Thus, if performance and high availability is important for you, is strongly recommended to use more than one isntance to alevite (distribute) computing power. 

## Dependencies

* Ubuntu linux-based system (Installed on your remote instance/machine)
* Your .pem key for accessing your remote instance/server (because we are going to connect through ssh)
* python 2.7-
* pip
* ansible

```
 $ sudo pip install ansible
```
 
## Configuration

You must specify host names and ip addresses from your instances in the 'production' file. A possible configuration may be:

```
#Harvester nodes
[harvesters] #Leave it as is
node1 ansible_ssh_host={192.168.1.5}    #Put your remote instance ip
node2 ansible_ssh_host={192.168.1.6}    #Put your remote instance ip
node2 ansible_ssh_host={192.168.1.7}    #Put your remote instance ip

#Master nodes
[masters] #Leave it as is
master1 ansible_ssh_host={192.168.1.2}   #Put your remote instance ip
master2 ansible_ssh_host={192.168.1.3}   #Put your remote instance ip
```
Here you can see another example of a single node configuration:

```
#Master nodes
[masters] #Leave it as is
master ansible_ssh_host={192.168.1.2}   #Put your remote instance ip
```

## Deploying an instance

Deploy all instances defined on the 'production' file:

```
$ ansible-playbook --private-key {path-to-your-pem-file} -uubuntu -i production site.yml
```

If only a specific group of actions is required:

```
ansible-playbook --private-key {path-to-your-pem-file} -uubuntu -i production site.yml  --tags "apache"
```

If you want to limit the deployment process only to a pacticular hostname:

```
$ ansible-playbook --private-key {path-to-your-pem-file} -uubuntu -i production site.yml  --limit {name-of-host: ie node1}
```
