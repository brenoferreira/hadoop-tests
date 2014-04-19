#!/bin/bash
echo "STEP: updating"
sudo apt-get update
echo "STEP: Python Version"
python --version
echo "STEP: installing python"
sudo apt-get install -y python
echo "STEP: Python Version"
python --version
sudo apt-get install -y python-pip
sudo pip install --upgrade simplejson

echo "STEP: Installing Requests"
sudo pip install requests

echo "STEP: Installing Textblob"
sudo pip install -U textblob

echo "STEP: Python Version"
python --version

echo "STEP: Downloading Textblob corpora"
sudo python -m textblob.download_corpora

echo "STEP: Installing boto"
sudo pip install --upgrade boto

echo "STEP: Installing boto"
sudo pip install --upgrade warc


# --bootstrap 'sudo pip install --upgrade simplejson'

#Reading package lists...
#Building dependency tree...
#Reading state information...
#Some packages could not be installed. This may mean that you have
#requested an impossible situation or if you are using the unstable
#distribution that some required packages have not yet been created
#or been moved out of Incoming.
#The following information may help to resolve the situation:

#The following packages have unmet dependencies:
#  python-pip: Depends: python-support (>= 0.90.0) but 0.8.4lenny2 is to be installed


## See here for more:
# http://slid.es/bearrito/pittsburgh-nosql-_-mapreduce

