'''
    This is a file that configures how your server runs
    You may eventually wish to have your own explicit config file
    that this reads from.

    For now this should be sufficient.

    Keep it clean and keep it simple, you're going to have
    Up to 5 people running around breaking this constantly
    If it's all in one file, then things are going to be hard to fix

    If in doubt, `import this`
'''

#-----------------------------------------------------------------------------
import os
import sys
from bottle import run, Bottle
import bcrypt
from geventwebsocket import WebSocketServer, WebSocketApplication
from geventwebsocket.handler import WebSocketHandler
from bottle_websocket import websocket, GeventWebSocketServer
# from bottle.ext.websocket import WebSocketPlugin


#-----------------------------------------------------------------------------
# You may eventually wish to put these in their own directories and then load 
# Each file separately

# For the template, we will keep them together

import model
import view
import controller
import no_sql_db
from app import app
import ssl

#-----------------------------------------------------------------------------

# It might be a good idea to move the following settings to a config file and then load them
# Change this to your IP address or 0.0.0.0 when actually hosting
host = '0.0.0.0'

# Test port, change to the appropriate port to host
port = 8084

# Turn this off for production
debug = True

# clients = []

# class ChatWebSocket(WebSocketApplication):
#     def on_open(self):
#         # Add client to the list of connected clients
#         clients.append(self)

#     def on_message(self, message):
#         # Broadcast the message to all connected clients
#         for client in clients:
#             client.ws.send(message)

#     def on_close(self, reason):
#         # Remove client from the list of connected clients
#         clients.remove(self)

def run_server():    
    '''
        run_server
        Runs a bottle server
    '''
    cert_key = './certificates/0.0.0.0-key.pem'
    cert_file = './certificates/0.0.0.0.pem'
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(cert_file, keyfile=cert_key)
    
    # run(app, host=host, port=port, debug=debug, server='gunicorn', keyfile='./certificates/0.0.0.0-key.pem', certfile='./certificates/0.0.0.0.pem')
    
    manage_db()
    
    run(host=host, port=port, server='gunicorn', keyfile='./certificates/0.0.0.0-key.pem', certfile='./certificates/0.0.0.0.pem')
    # run(host=host, port=port, server=GeventWebSocketServer, keyfile='./certificates/0.0.0.0-key.pem', certfile='./certificates/0.0.0.0.pem', ssl_context=ssl_context)
    # server = GeventWebSocketServer(host=host, port=port, handler_class=WebSocketHandler, keyfile=cert_key, certfile=cert_file)
    # run(server=server)

#-----------------------------------------------------------------------------


def manage_db():
    '''
        Blank function for database support, use as needed
    '''
    salt = generate_salt()
    no_sql_db.database.create_table_entry('users', ['0', 'liam', 'password', salt])
    
    salt = generate_salt()
    no_sql_db.database.create_table_entry('users', ['1', 'tyra', 'password', salt])
    
    
def generate_salt() -> str:
    salt = bcrypt.gensalt().decode('utf-8')
    print(salt)
    return salt


#-----------------------------------------------------------------------------

# What commands can be run with this python file
# Add your own here as you see fit

command_list = {
    'manage_db' : manage_db,
    'server'       : run_server
}

# The default command if none other is given
default_command = 'server'

def run_commands(args):
    '''
        run_commands
        Parses arguments as commands and runs them if they match the command list

        :: args :: Command line arguments passed to this function
    '''
    commands = args[1:]

    # Default command
    if len(commands) == 0:
        commands = [default_command]

    for command in commands:
        if command in command_list:
            command_list[command]()
        else:
            print("Command '{command}' not found".format(command=command))

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    run_commands(sys.argv)