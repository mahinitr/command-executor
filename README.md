# command-executor
## Introduction
This contains the code for command executor tool.
It contains the below componets.
1. The UI for selecting and sending the execution request to backend.
2. The BE for loading, executing the commands, storing the results in the sqlite DB and sending the output to UI.
3. SQlite DB file for storing the results.
4. Commands Json file for storing the commands.
5. Modules directory with python modules that contain the code for commands

## Check it live
I will deploy in AWS and share the link here. It is still in progress.

## Setup and run the tool
Pre-requisites: Python 2.7 with flask, sqlite3

1. Install python and its modules flask and sqlite3 using pip
2. Clone the repo to local/remote machine
3. Start the web server: python server.py
4. Open the web application in the browser using the url: <machine_ip>:<machine_port>, ex: http://127.0.0.1:5000

## Details of implementation
1. The UI/BE routes are served by the same web server
2. UI routes: GET /
3. BE routes: POST /execute/<cmd_id>, GET /commands, GET /healthcheck

The UI route renders the html pages with js & css.
