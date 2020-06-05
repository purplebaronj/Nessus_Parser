This parser is designed to parse Tenable Nessus scans (.nessus format) and send parsed output to an external tool for further analysis.

Third Party Tools Supported
Currently, the application supports sending data into Postgres, Splunk and ElasticSearch but it has been architected in such a way as to allow adding additional support without requiring major changes to the codebase. 

Custom Parsing of Nessus Plugins
In addition to allowing for multiple tools for output and storage of Nessus data, there is also the ability to add or remove custom parsers for specific Nessus plugins. This is necessary since various Nessus plugins do not provide output that allows security practitioners to view each item as its own individual event. For example, software, service, and user centered plugins are a few that can be parsed specifically to provide a cleaner breakdown of individual events.

Usage - 

By default, the nessus_parser script will look for a .parser_config file in the source code directory. This file will be used to store any credentials needed to authenticate to the various supported "outputters" or data storage tools. Examples of what this file should look like are as follows;

Setting up for ElasticSearch - 
[Credentials]
TITLE=Elasticsearch
INDEX=test
HOST=127.0.0.1
PORT=9200
<USER>=admin
<PASSWORD>=password

Setting up for Postgres - 
[Credentials2]
TITLE=Postgres
DATABASE=test
USER=postgres
PASSWORD=password
HOST=127.0.0.1
PORT=5432

Setting up for Splunk - 
[Credentials2]
TITLE=Splunk
INDEX=test
USER=admin
PASSWORD=password
HOST=127.0.0.1
PORT=8089

If no parser_config is specified, the default is to print all parsed data back to the screen.

Once you have made a decision on which output method you would like to use, you must point the script to where your Nessus files are actually located. Script execution can be accomplished as follows;

python nessus_parser.py --directory=/Users/julian/Nessus_Scans

or if you only wish to parse an individual scan

python nessus_parser.py --scan=/Users/julian/Nessus_Scans/test.nessus
