from mcstatus import JavaServer

import time

vrsmp = JavaServer.lookup("villagerrights.xyz")


def update_java(data):
    try:
        query_response = vrsmp.query()
        player_names = query_response.players.names
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
    new_data['query'] = query_response  # TODO: is this needed?
    return new_data
        #update_stats(players=player_names)
        #write_to_json(w.WHITELIST_DICT, "data/stats.json")


def get_status():
    status = vrsmp.status()
    return {"latency": status.latency,
            "players": {"online": status.players.online,
                        "max": status.players.max},
            "version": str(status.version.name)}