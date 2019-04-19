import pandas as pd
import json
import re
from datetime import datetime

import time


def parse_multicol(filename, sortKey='PLAYER_ID', extraColumns=None):
    with open('data/' + filename + '.json', 'r') as infile:
        statLine = json.load(infile)
    rawColumns = statLine['resultSets']['headers'][1]['columnNames']
    offset = statLine['resultSets']['headers'][0]['columnsToSkip']
    span = statLine['resultSets']['headers'][0]['columnSpan']
    categories = statLine['resultSets']['headers'][0]['columnNames']

    for i in range(len(categories)):
        prefix = categories[i].replace(" ", "_")
        for j in range(span):
            rawColumns[3*i+j+offset] = prefix + "_" + rawColumns[3*i+j+offset]

    importedStat = pd.DataFrame(statLine['resultSets']['rowSet'],
                                columns=rawColumns)

    if sortKey is not None:
        importedStat.sort_values(sortKey, inplace=True)
        importedStat.set_index(sortKey, inplace=True)

    if extraColumns is not None:
        importedStat.drop(extraColumns, inplace=True, axis=1)

    return importedStat


def parse_stats(filename, sortKey='PLAYER_ID', extraColumns=None):
    with open('data/' + filename + '.json', 'r') as infile:
        statLine = json.load(infile)

    importedStat = pd.DataFrame(statLine['resultSets'][0]['rowSet'],
                                columns=statLine['resultSets'][0]['headers'])
    
    if sortKey is not None:
        importedStat.sort_values(sortKey, inplace=True)
        importedStat.set_index(sortKey, inplace=True)

    if extraColumns is not None:
        importedStat.drop(extraColumns, inplace=True, axis=1)

    for col in importedStat.columns.values:
        if ('RANK'in col):
            importedStat.drop(col, inplace=True, axis=1)

    return importedStat


def load_player_stats(timeSpan):
    allPlayers = {}
    cf = ['AGE', 'W_PCT', 'CFID', 'CFPARAMS']
    extra = ['PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'GP', 'W', 'L', 'MIN']
    bio = ['PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'GP', 'AST', 'REB', 'AGE', 'AST_PCT', 'DREB_PCT', 'NET_RATING', 'OREB_PCT', 'PTS', 'TS_PCT', 'USG_PCT']
    base = ['REB', 'AST', 'DREB', 'OREB', 'TEAM_ID', 'DD2', 'TD3']
    fga = ['FGA', 'FGM', 'FG_PCT']
    blk = ['BLK', 'BLKA', 'PF', 'PFD']
    trackingPre = ['PLAYER_NAME', 'PLAYER_LAST_TEAM_ID', 'PLAYER_LAST_TEAM_ABBREVIATION', 'AGE', 'GP', 'G']

    for year in timeSpan:

        stats = []
        traditional = (parse_stats('Base'+'PerGame'+year, extraColumns=fga+blk+base+cf))
        stats.append(parse_stats('Advanced'+'PerGame'+year, extraColumns=fga+extra+cf))
        stats.append(parse_stats('Misc'+'PerGame'+year, extraColumns=extra+blk+cf))
        stats.append(parse_stats('biostats'+'PerGame'+year, extraColumns=bio))
        stats.append(parse_stats('PerGame'+'Efficiency'+year, extraColumns=extra))
        stats.append(parse_stats('PerGame'+'Passing'+year, extraColumns=extra))
        stats.append(parse_stats('PerGame'+'SpeedDistance'+year, extraColumns=extra))
        stats.append(parse_stats('PerGame'+'Rebounding'+year, extraColumns=extra))
        stats.append(parse_stats('PerGame'+'Possessions'+year, extraColumns=extra+['POINTS']))

        allPlayers[year] = traditional.join(stats, how='inner')
        allPlayers[year].fillna(value=0, inplace=True)
        allPlayers[year].to_csv('processed/PlayerStats'+year+'.csv')

    return allPlayers


def load_gamelogs(timeSpan):
    allGames = {}
    allPlayerGameLogs = {}

    for year in timeSpan:
        print('Loading season %d...' % year)

        with open('data/' + year + '.json', 'r') as in_file:
            gameJson = json.load(in_file)

        gameList = pd.DataFrame(gameJson['resultSets'][0]['rowSet'],
                                columns=gameJson['resultSets'][0]['headers'])
        gameList.sort_values('GAME_ID', inplace=True)
        listByGameID = gameList[gameList. WL == 'W'].set_index('GAME_ID')['GAME_DATE']
        gameid_keys = listByGameID.index.values

        with open('data/Games'+year+'.json', 'r') as infile:
            gameString = infile.read().splitlines()
        gameString.pop(0)

        gameScores = pd.DataFrame(columns=['HOME_TEAM', 'HOME_SCORE', 'AWAY_TEAM', 'AWAY_SCORE'])
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
  
            playerBoxScore = pd.DataFrame(data['resultSets'][0]['rowSet'], columns=data['resultSets'][0]['headers'])
            tempGameList.append(playerBoxScore[boxScoreCols].set_index('GAME_ID'))

        allGames[year] = pd.concat([scoreList, listByGameID], axis=1)

        allPlayerGameLogs[year] = pd.concat(tempGameList)
        allPlayerGameLogs[year].set_index(allPlayerGameLogs[year].index + '-' + allPlayerGameLogs[year]['TEAM_ABBREVIATION'])

        return [allGames, allPlayerGameLogs]


def get_last_game(gameList, boxScores):
    boxScores['LAST_GAME'] = 0

    for gameid, g in gameList:
        thisGameDate = datetime.strptime(gameList.loc[gameid].GAME_DATE, '%Y-%m-%d')
        ind = gameList.index.get_loc(gameid)      # Position of the game on the season game list

        teamArray = [gameList.loc[gameid].HOME_TEAM,
                     gameList.loc[gameid].AWAY_TEAM]
        daysSinceLastGame = [0, 0]

        for TEAM in teamArray:
            i = ind-1

            while (i > 0 and (TEAM != games.iloc[i].HOME_TEAM
                         and TEAM != games.iloc[i].AWAY_TEAM)):
                i -= 1 

            if(i >= 0):
                lastGameID[j] = games.index[i]
                lastGameDate = datetime.strptime(games.iloc[i].GAME_DATE,
                                                 '%Y-%m-%d')  # Date of this game
                daysSinceLastGame[j] = min(5, (thisGameDate-lastGameDate).days)

        #for playerid, player in boxScores[gameid].iterrows():
            #j = team.index(player.TEAM_ABBREVIATION)		  
            #boxScores.set_value(gameid+'-'+TEAM, 'LAST_GAME', daysSinceLastGame[j]) 
                #FIND THE TEAM

            #minutesLastPlayed = 0
            #try: 
                #timeLastPlayed = boxScores[lastGameID[j]].MIN.loc[playerid]
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
