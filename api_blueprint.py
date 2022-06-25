# Create flask blueprint for Minecraft server api with all routes from app.py
import threading
from flask import Blueprint, request

from java_server_utils import get_uuid, update_java_status
from json_utils import read_from_json


server_api = Blueprint('server_api', __name__)

players = update_java_status({'online': False, 'players': []})


# Run update_java_stats every 10 seconds with players as argument
def update_java_thread():
    global players
    players = update_java_status(players)
    threading.Timer(10, update_java_thread).start()


# Create page for getting stats of a user
@server_api.route('/stats/player/<username>')
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


# Create page for leaderboard
# It returns top 10 players by default, but you can specify a number of players in request.args (key: top)
@server_api.route('/stats/leaderboard')
def get_leaderboard():
    data = read_from_json("data/stats.json")
    top = 10
    if 'top' in request.args:
        top = int(request.args['top'])
        if top > len(data):
            top = len(data)
        if top < 1:
            top = 1
    return sorted(data.values(), key=lambda x: x['playtime'], reverse=True)[:top]


# Create page to return stats of all players
@server_api.route('/stats/all')
def get_all_stats():
    data = read_from_json("data/stats.json")
    return {"stats": data}

@server_api.route('/current_players')
def get_current_players():
    return players

@server_api.route('/log/connections')
def get_connections():
    if 'last' in request.args:
        last = int(request.args['last'])
        if last < 1:
            last = 1
    else:
        last = 10
    with open("connections.log", "r") as f:
        return f.readlines()[-last:]