from time import strftime
from flask import Flask

import threading

from java_server_utils import get_uuid, update_java_status
from json_utils import read_from_json

from api_blueprint import server_api, update_java_thread

app = Flask(__name__)

# Import server_api and register it as blueprint
app.register_blueprint(server_api)


@app.route('/')
def main():
    return "Hello World!"


if __name__ == '__main__':
    update_java_thread()  # Start thread
    app.run()  