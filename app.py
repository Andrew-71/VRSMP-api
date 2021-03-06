from flask import Flask, redirect, render_template

from api_blueprint import server_api, update_java_thread
from system_status_blueprint import system_stats

from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.config['SECRET_KEY'] = open('data/app_secret_key.txt').read().strip()


app.register_blueprint(server_api)
app.register_blueprint(system_stats)


@app.route('/')
def main():
    return redirect('/docs')


if __name__ == '__main__':
    update_java_thread()  # Start thread

    debug = False
    if debug:
        app.run()
    else:
        http_server = WSGIServer(('', 80), app)
        http_server.serve_forever()