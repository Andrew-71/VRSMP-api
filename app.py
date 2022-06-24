from time import strftime
from flask import Flask

import threading

from java_server_utils import get_uuid, update_java_status
from json_utils import read_from_json

app = Flask(__name__)

players = update_java_status({'online': False, 'players': []})

# Run update_java_stats every 10 seconds with players as argument
def update_java_thread():
    global players
    players = update_java_status(players)
    # include current time in the log
    threading.Timer(10, update_java_thread).start()

# TODO: seperate the stats into a blueprint

# Create page for getting stats of a user
@app.route('/stats/<username>')
def get_user_stats(username):
    data = read_from_json("data/stats.json")
    
    # We need to check for Bedrock players who have a dot as first character in their username
    # For them we will use their username as id since they don't have a UUID
    if username[0] == ".":
        uuid = username
    else:
        uuid = get_uuid(username)
        
    if uuid in data:
        return data[uuid]
    else:
        return {"code": 404, "message": "User not found"}


# Create page for leaderboard that returns top 10 players
@app.route('/stats/leaderboard')
def get_leaderboard():
    data = read_from_json("data/stats.json")
    sorted_data = sorted(data.items(), key=lambda x: x[1]['playtime'], reverse=True)
    return {"leaderboard": sorted_data[:10]}


# Create page to return stats of all players
@app.route('/stats/all')
def get_all_stats():
    data = read_from_json("data/stats.json")
    return {"stats": data}


@app.route('/')
def main():
    return players


if __name__ == '__main__':
    update_java_thread()  # Start thread
    app.run()