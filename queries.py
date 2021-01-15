import requests

name = 'chrizdashiz'
key = '?api_key=RGAPI-8c0b84bc-529d-4a49-a61c-6c12b10b5c84'
version = '10.16.1'


def champion_name_query(champion_id):  # returns a champion name given an id
    champion_query = requests.get('http://ddragon.leagueoflegends.com/cdn/' + version + '/data/en_US/champion.json')
    champ_query = champion_query.json()
    c_q = champ_query['data']

    champ_dict = {}
    for key in c_q:
        row = c_q[key]
        champ_dict[row['key']] = row['id']

    return champ_dict[champion_id]


def account_id_query(summoner_name):  # returns an account number given a summoner name
    account_query = requests.get(
        'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + key)
    account_q = account_query.json()
    account_id = account_q['accountId']
    return account_id


def match_history_query(account_id):  # returns the match history given an account id
    match_history_query = requests.get(
        'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id + key)
    match_history = match_history_query.json()
    matches = match_history['matches']
    return matches


def game_info_query(champion_id, game_id):  # returns a particpant id given champion id and game id
    game_info_query = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/' + game_id + key)
    game_info = game_info_query.json()

    for x in range(len(game_info['participants'])):
        if (game_info['participants'][x]['championId'] == champion_id):
            champion_name = champion_name_query(str(champion_id))
            kills = game_info['participants'][x]['stats']['kills']
            deaths = game_info['participants'][x]['stats']['deaths']
            assists = game_info['participants'][x]['stats']['assists']


def champion_stats(name):
    print("Match History for " + name)
    account_query = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + key)
    account_q = account_query.json()
    account_id = account_q['accountId']  # account id of given summoner name

    match_history_query = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id + key)
    match_history = match_history_query.json()
    matches = match_history['matches']

    game_id = []                    # match id
    champion_id = []                # champion id
    champion_name = []              # champion name

    champion_played = []            # list of champions played out of games played
    champion_kills = []             # kills of specific champion out of games played
    champion_deaths = []            # deaths of specific champion out of games played
    champion_assists = []           # assists of specific champion out of games played
    champion_games = []             # games played of specific champion out of games played
    champion_wins = []
    champion_losses = []
    champion_kda = []
    champion_winrate = []

    game_kills = []
    game_deaths = []
    game_assists = []

    date_played = []
    game_outcome = []

    for x in range(len(matches)):
        if matches[x]['queue'] == 420:
            game_id.append(matches[x]['gameId'])  # game id
            champion_id.append(matches[x]['champion'])  # champion id
            champion_name.append(champion_name_query(str(matches[x]['champion'])))  # champion name
            date_played.append(matches[x]['timestamp'])

    for x in range(20):  # iterates to next game
        game_info_query = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/' + str(game_id[x]) + key)
        game_info = game_info_query.json()

        y = 0
        while y < 10:
            if game_info['participants'][y]['championId'] == champion_id[x]:
                game_kills.append(game_info['participants'][y]['stats']['kills'])
                game_deaths.append(game_info['participants'][y]['stats']['deaths'])
                game_assists.append(game_info['participants'][y]['stats']['assists'])

                team_id = ((game_info['participants'][y]['teamId']) / 100) - 1
                game_outcome.append(game_info['teams'][int(team_id)]['win'])                    # win/loss
            y = y + 1
        print(str(date_played[x]) + " Game " + str(x + 1)
              + "   Champion: " + str(champion_name[x])
              + " | KDA: " + str(game_kills[x])
              + "/" + str(game_deaths[x])
              + "/" + str(game_assists[x])
              + "   " + game_outcome[x])

    for x in range(20):
        if champion_name[x] not in champion_played:
            champion_played.append(champion_name[x])
            champion_games.append(1)
            champion_kills.append(game_kills[x])
            champion_deaths.append(game_deaths[x])
            champion_assists.append(game_assists[x])
            if game_outcome[x] == 'Win':
                champion_wins.append(1)
                champion_losses.append(0)
            else:
                champion_losses.append(1)
                champion_wins.append(0)

        else:
            for y in range(len(champion_played)):
                if champion_name[x] == champion_played[y]:
                    champion_games[y] = champion_games[y] + 1
                    champion_kills[y] = champion_kills[y] + game_kills[x]
                    champion_deaths[y] = champion_deaths[y] + game_deaths[x]
                    champion_assists[y] = champion_assists[y] + game_assists[x]
                    if game_outcome[x] == 'Win':
                        champion_wins[y] = champion_wins[y] + 1
                    else:
                        champion_losses[y] = champion_losses[y] + 1

    for x in range(len(champion_wins)):
        winrate = (champion_wins[x]/(champion_wins[x]+champion_losses[x])) * 100
        champion_winrate.append(round(winrate))

        if champion_deaths[x] == 0:
            kda = round(champion_kills[x] + champion_assists[x], 2)
        else:
            kda = round((champion_kills[x] + champion_assists[x]) / champion_deaths[x], 2)
        champion_kda.append(kda)


    print(" ")
    print("Last 20 Game Stats: ")
    for x in range(len(champion_played)):
        print(champion_played[x] + " | Games Played: " + str(champion_games[x])
              + " | KDA: " + str(champion_kda[x])
              + ', ' + str(round(champion_kills[x]/champion_games[x], 2))
              + "/" + str(round(champion_deaths[x]/champion_games[x], 2))
              + "/" + str(round(champion_assists[x]/champion_games[x], 2))
              + " | Winrate: " + str(champion_winrate[x]) + "%")


champion_stats(name)