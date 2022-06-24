from flask import Flask

from java_server_utils import update_java, get_status

app = Flask(__name__)
#players = update_java({'online': False, 'players': []})


@app.route('/status/ping')
def quick_status():  # put application's code here
    return get_status()


@app.route('/')
def main():  # put application's code here
    return get_status()


if __name__ == '__main__':
    app.run()
