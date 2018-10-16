"""
Web Server using Flask
Author: Maheshwar
"""
import os
import sys
import json
from flask import Flask, render_template, request, jsonify
import traceback
import importlib
import sqlite3
import datetime
from db import create_execution_history_table, insert_command_result

app = Flask(__name__)
conn = sqlite3.connect('example.db')
COMMANDS_JSON = os.path.dirname(os.path.realpath(__file__)) + "/commands.json"
MODULE_DIR = os.path.dirname(os.path.realpath(__file__)) + "/modules"
sys.path.append(MODULE_DIR)
COMMANDS = None

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'App is Running'

@app.route('/favicon.ico')
def facicon():
    return 'favicon'

@app.route('/commands')
def fetch_commands():
    if COMMANDS == None or not isinstance(COMMANDS, list) or len(COMMANDS) == 0:
        return jsonify(commands=[])
    try:
        commands = []
        for cmd in COMMANDS:
            commands.append({"name" : cmd['name'], "args_help" : cmd['args_help']})
        return jsonify(commands=commands)
    except:
        print traceback.format_exc()
        return jsonify(commands=[])

@app.route('/execute/<int:id>', methods=['POST'])
def execute(id):
    try:
        cmd_id = int(id)
        print request.data
        print "Received Command id " + str(cmd_id)
        command = COMMANDS[cmd_id - 1]
        command_name = command["name"]
        module_name = command["module"]
        cmd_method = command["cmd"]
        loaded_module = __import__(module_name)
        if not hasattr(loaded_module, cmd_method):
            raise Exception("Failed to load module")
        meth = getattr(loaded_module, cmd_method)
        result = meth()
        time_now = datetime.datetime.now()
        insert_command_result(command_name, result, time_now)
        return jsonify(message=result, status="success")
    except:
        print traceback.format_exc()
        insert_command_result(command_name, "Failed to execute", datetime.datetime.now())
        return jsonify(message="Failed to execute in the backend", status="failed")

@app.route('/')
def default_route():
    return render_template('index.html')

if __name__ == "__main__":
    print "Starting the server"
    global COMMANDS
    try:
        with open(COMMANDS_JSON) as fp:
            data = json.load(fp)
            COMMANDS = data["commands"]
    except:
        print traceback.format_exc()
        print "failed to load commands json"
        sys.exit(0)
    if len(COMMANDS) == 0:
        print "No commands found"
        sys.exit(0)
    print "Commands loaded - " + str(COMMANDS)
    create_execution_history_table()
    app.run(host='0.0.0.0')
