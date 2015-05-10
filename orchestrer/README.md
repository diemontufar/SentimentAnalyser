Orchestration module
===================

- - - - 

Authors:

* Ilkan Esiyok - 616394
* Andres Chaves - 706801
* Gustavo Carrion - 667597
* Clifford Siu - 591158
* Diego Montufar - 661608

## Purpose

Automate the host software installation in order to have a centralized and repeatable configuration process.

## Dependencies

We need Ansible and Python 2 to run the Playbooks. More info (http://docs.ansible.com/intro_installation.html)
 
## Installation

To install the Orchestation scripts just checkout the project

## How to Run
Provided this if a complete run is needed this command should be executed:

ansible-playbook --private-key /pathToPrivateKey -uubuntu -i (stage|production) site.yml

The Playbooks also have tags if only a specific group of actions is required:

ansible-playbook --private-key /pathToPrivateKey -uubuntu -i (stage|production) site.yml  --tags "install_harvester"

Finally if you want to setup a new equipments these are the steps to follow:

   1. Insert the new host on production bellow the assigned role
   2. Run ansible-playbook --private-key /pathToPrivateKey -uubuntu -i (stage|production) site.yml  --limit theNewHost
