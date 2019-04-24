import pandas as pd
import json
import re
from datetime import datetime

import time


def parse_multicol(filename, sortkey='PLAYER_ID', extra_cols=None):
    with open('data/' + filename + '.json', 'r') as infile:
        statline = json.load(infile)
    raw_cols = statline['resultSets']['headers'][1]['columnNames']
    offset = statline['resultSets']['headers'][0]['columnsToSkip']
    span = statline['resultSets']['headers'][0]['columnSpan']
    categories = statline['resultSets']['headers'][0]['columnNames']

    for i in range(len(categories)):
        prefix = categories[i].replace(" ", "_")
        for j in range(span):
            raw_cols[3*i+j+offset] = prefix + "_" + raw_cols[3*i+j+offset]

    imported_stat = pd.DataFrame(statline['resultSets']['rowSet'],
                                 columns=raw_cols)

    if sortkey is not None:
        imported_stat.sort_values(sortkey, inplace=True)
        imported_stat.set_index(sortkey, inplace=True)

    if extra_cols is not None:
        imported_stat.drop(extra_cols, inplace=True, axis=1)

    return imported_stat


def parse_stats(filename, sortkey='PLAYER_ID', extra_cols=None):
    with open('data/' + filename + '.json', 'r') as infile:
        statline = json.load(infile)

    imported_stat = pd.DataFrame(statline['resultSets'][0]['rowSet'],
                                 columns=statline['resultSets'][0]['headers'])

    if sortkey is not None:
        imported_stat.sort_values(sortkey, inplace=True)
        imported_stat.set_index(sortkey, inplace=True)

    if extra_cols is not None:
        imported_stat.drop(extra_cols, inplace=True, axis=1)

    for col in imported_stat.columns.values:
        if ('RANK'in col):
            imported_stat.drop(col, inplace=True, axis=1)

    return imported_stat


def load_player_stats(seasons):
    allplayers = {}
    cf = ['AGE', 'W_PCT', 'CFID', 'CFPARAMS']
    extra = ['PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION',
             'GP', 'W', 'L', 'MIN']
    bio = ['PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'GP', 'AST', 'REB', 
           'AGE', 'AST_PCT', 'DREB_PCT', 'NET_RATING', 'OREB_PCT', 'PTS',
           'TS_PCT', 'USG_PCT']
    base = ['REB', 'AST', 'DREB', 'OREB', 'TEAM_ID', 'DD2', 'TD3']
    fga = ['FGA', 'FGM', 'FG_PCT']
    blk = ['BLK', 'BLKA', 'PF', 'PFD']
    trackingPre = ['PLAYER_NAME', 'PLAYER_LAST_TEAM_ID',
                   'PLAYER_LAST_TEAM_ABBREVIATION', 'AGE', 'GP', 'G']

    for year in seasons:

        stats = []
        traditional = (parse_stats('Base'+'PerGame'+year,
                                   extra_cols=fga+blk+base+cf))
        stats.append(parse_stats('Advanced'+'PerGame'+year,
                                 extra_cols=fga+extra+cf))
        stats.append(parse_stats('Misc'+'PerGame'+year,
                                 extra_cols=extra+blk+cf))
        stats.append(parse_stats('biostats'+'PerGame'+year,
                                 extra_cols=bio))
        stats.append(parse_stats('PerGame'+'Efficiency'+year,
                                 extra_cols=extra))
        stats.append(parse_stats('PerGame'+'Passing'+year,
                                 extra_cols=extra))
        stats.append(parse_stats('PerGame'+'SpeedDistance'+year,
                                 extra_cols=extra))
        stats.append(parse_stats('PerGame'+'Rebounding'+year,
                                 extra_cols=extra))
        stats.append(parse_stats('PerGame'+'Possessions'+year,
                                 extra_cols=extra+['POINTS']))

        allplayers[year] = traditional.join(stats, how='inner')
        allplayers[year].fillna(value=0, inplace=True)
        allplayers[year].to_csv('processed/PlayerStats'+year+'.csv')

    return allplayers


def load_gamelogs(seasons):
    allgames = {}
    allplayer_gamelogs = {}

    for year in seasons:
        print('Loading season %d...' % year)

        with open('data/' + year + '.json', 'r') as in_file:
            gameJson = json.load(in_file)

        gamelist = pd.DataFrame(gameJson['resultSets'][0]['rowSet'],
                                columns=gameJson['resultSets'][0]['headers'])
        gamelist.sort_values('GAME_ID', inplace=True)
        listByGameID = gamelist[gamelist. WL == 'W'].set_index('GAME_ID')['GAME_DATE']
        gameid_keys = listByGameID.index.values

        with open('data/Games'+year+'.json', 'r') as infile:
            gameString = infile.read().splitlines()
        gameString.pop(0)

        gameScores = pd.DataFrame(columns=['HOME_TEAM', 'HOME_SCORE',
                                           'AWAY_TEAM', 'AWAY_SCORE'])
        boxScoreCols = ['GAME_ID', 'TEAM_ABBREVIATION', ' PLAYER_ID', 'MIN']
        tempGameList = []

        for line in gameString:
            data = json.loads(line)
            gameid = data['parameters']['GameID']

            teamBoxScore = pd.DataFrame(data['resultSets'][1]['rowSet'],
                                        columns=data['resultSets'][1]['headers'])
            scoreList.loc[gameid] = [teamBoxScore.TEAM_ABBREVIATION[0],
                                     teamBoxScore.PTS[0],
                                     teamBoxScore.TEAM_ABBREVIATION[1],
                                     teamBoxScore.PTS[1]
                                     ]
  
            playerBoxScore = pd.DataFrame(data['resultSets'][0]['rowSet'],
                                          columns=data['resultSets'][0]['headers'])
            tempGameList.append(playerBoxScore[boxScoreCols].set_index('GAME_ID'))

        allgames[year] = pd.concat([scoreList, listByGameID], axis=1)

        allplayer_gamelogs[year] = pd.concat(tempGameList)
        allplayer_gamelogs[year].set_index(allplayer_gamelogs[year].index + '-' +
                                           allplayer_gamelogs[year]['TEAM_ABBREVIATION'])

        return [allgames, allplayer_gamelogs]


def get_last_game(gamelist, boxscores):
    boxscores['LAST_GAME'] = 0

    for gameid, g in gamelist:
        gamedate = datetime.strptime(gamelist.loc[gameid].GAME_DATE,
                                     '%Y-%m-%d')
        ind = gamelist.index.get_loc(gameid)

        teamArray = [gamelist.loc[gameid].HOME_TEAM,
                     gamelist.loc[gameid].AWAY_TEAM]
        daysSinceLastGame = [0, 0]

        for TEAM in teamArray:
            i = ind-1

            while (i > 0 and (TEAM != games.iloc[i].HOME_TEAM
                   and TEAM != games.iloc[i].AWAY_TEAM)):
                i -= 1 

            if(i >= 0):
                last_gameid[j] = games.index[i]
                laste_gamedate = datetime.strptime(games.iloc[i].GAME_DATE,
                                                   '%Y-%m-%d')
                daysSinceLastGame[j] = min(5, (gamedate-laste_gamedate).days)

        #for playerid, player in boxscores[gameid].iterrows():
            #j = team.index(player.TEAM_ABBREVIATION)		  
            #boxscores.set_value(gameid+'-'+TEAM, 'LAST_GAME', daysSinceLastGame[j]) 
                #FIND THE TEAM

            #minutesLastPlayed = 0
            #try: 
                #timeLastPlayed = boxscores[last_gameid[j]].MIN.loc[playerid]
                #if timeLastPlayed is not None:
                    #minutesLastPlayed = int(timeLastPlayed.split(':')[0])
            #except KeyError:
                #pass


def scale_vector(data, a=None, b=None, mode='mean'):
    if isinstance(data, pd.DataFrame):
        x = data._get_numeric_data()
    else:
        x = data

    if (mode == 'mean'):
        if(a is not None and b is not None):
            return (x-a)/b, a, b
        else:
            return (x-x.mean())/x.std(), x.mean(), x.std()

    if (mode == 'range'):
        if(a is not None and b is not None):
            return (x-b)/(a-b), a, b
        else:
            return (x-x.min())/(x.max()-x.min()), x.max(), x.min()


def unscale(y, a, b, mode='mean'):

    if (mode == 'mean'):
        return y*b+a

    if (mode == 'range'):
        return y*(a-b)+b

    return 0
