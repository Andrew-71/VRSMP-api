from flask import Flask, render_template

from api_blueprint import server_api, update_java_thread

app = Flask(__name__)

# Import server_api and register it as blueprint
app.register_blueprint(server_api)


@app.route('/')
def main():
    return render_template('base.html')


if __name__ == '__main__':
    update_java_thread()  # Start thread
    app.run()