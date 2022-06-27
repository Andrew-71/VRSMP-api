from flask import Flask, redirect, render_template

from api_blueprint import server_api, update_java_thread
from system_status_blueprint import system_stats

app = Flask(__name__)

app.register_blueprint(server_api)
app.register_blueprint(system_stats)


@app.route('/')
def main():
    return redirect('/docs')


if __name__ == '__main__':
    update_java_thread()  # Start thread
    app.run()