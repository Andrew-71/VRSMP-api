import json
from mcstatus import JavaServer
from requests import request

from json_utils import read_from_json, write_to_json

import time


# Get Minecraft user's UUID from their username
def get_uuid(username):
    if username[0] == '.':
        return username
    url = "https://api.mojang.com/users/profiles/minecraft/" + username
    response = request("GET", url)
    return response.json()['id']

# Get Minecraft user's username from their username
def get_username(uuid):
    if uuid[0] == '.':
        return uuid
    url = "https://api.mojang.com/user/profiles/" + uuid + "/names"
    response = request("GET", url)
    return response.json()[0]['name']


def log_connections(new_players, old_players):
    # Log players that have connected and those that have left to connections.log with time
    with open("data/connections.log", "a") as f:
        for i in list(filter(lambda x: x not in new_players, old_players)):
            f.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + " " + i + " has left the server\n")
        for i in list(filter(lambda x: x not in old_players, new_players)):
            f.write(time.strftime("%H:%M:%S", time.localtime(time.time())) + " " + i + " has joined the server\n")


# Update our status of current online players
def update_java_status(data):
    try:
        query_response = request("GET", "https://api.mcsrvstat.us/2/villagerrights.xyz").json()  #vrsmp.query()
        try:
            player_names = query_response['players']['list']
        except KeyError:
            player_names = query_response['info']['raw']
    except TimeoutError:
        return {"online": False, "players": []}

    new_data = {"online": True, 'players': []}
    old_players = list(map(lambda x: x['username'], data['players']))
    for i in player_names:
        if i in old_players:
            for j in range(len(data['players'])):
                if data['players'][j]['username'] == i:
                    new_data['players'].append(data['players'][j])
                    break
        else:
            new_data['players'].append({'username': i, 'join_time': time.time()})
    new_data['query'] = query_response

    log_connections(player_names, old_players)

    update_stats(new_data['players'])

    return new_data


# Update stats of players in the Java server
def update_stats(players):
    data = read_from_json("data/stats.json")
    for i in players:
        uuid = get_uuid(i['username'])  # Java player

        if uuid in data:
            data[uuid]['playtime'] += 10  # Add 10 seconds to their playtime since we check the server every 10 seconds
        else:
            data[uuid] = {'playtime': 10, "first_seen": time.time()}
        data[uuid]['last_seen'] = time.time()
        data[uuid]['username'] = get_username(uuid)
    write_to_json(data, "data/stats.json")
