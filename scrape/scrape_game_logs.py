from nba_scrape import url_to_json
import json

lastGameScraped = 21600760

seasons = [('http://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom='
            '&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=T&Season='),
           '&SeasonType=Regular+Season&Sorter=PTS'
           ]

url = [('http://stats.nba.com/stats/boxscoretraditionalv2?'
        'EndPeriod=10&EndRange='),
       '&GameID=',
       '&RangeType=0&Season=',
       '&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
       ]

for year in seasons:
    season_log = url_to_json(seasons, [year, ''])
    with open('data/' + season_log + '.json', 'r') as in_file:
        gamelist = json.load(in_file)['resultSets'][0]['rowSet']

    gameids = sorted(gamelist, key=lambda game: game[4])[1::2]
    for game in gameids:
        if (int(game[4]) > lastGameScraped):
            print('Scraping game %d' % game[4])
            url_to_json(url,
                        [str(game[8]*120), str(game[4]), year, ''],
                        mode='a')
