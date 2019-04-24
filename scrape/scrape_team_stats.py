from nba_scrape import url_to_json
seasons = ['2013-14', '2014-15', '2015-16', '2016-17']


urls = ['http://stats.nba.com/stats/',
        ('?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment='
         '&LastNGames=0&LeagueID=00&Location=&MeasureType='),
        '&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=',
        ('&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&'
         'Season='),
        ('&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange='
         '&StarterBench=&TeamID=0&VsConference=&VsDivision=')
        ]
for year in seasons:
    url_to_json(urls,
                ['leaguedashteamstats', 'Base', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashteamstats', 'Advanced', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashteamstats', 'Four+Factors', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashteamstats', 'Defense', 'PerGame', year, ''])

urls = ['http://stats.nba.com/stats/',
        ('?Conference=&DateFrom=&DateTo=&DistanceRange=By+Zone&Division='
         '&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location='
         '&MeasureType='),
        ('&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust='
         'N&PerMode='),
        ('&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus='
         'N&Rank=N&Season='),
        ('&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange='
         '&StarterBench=&TeamID=0&VsConference=&VsDivision=')
        ]
for year in seasons:
        url_to_json(urls,
                    ['leaguedashteamshotlocations',
                     'Base', 'PerGame', year, ''])
        url_to_json(urls,
                    ['leaguedashteamshotlocations',
                     'Opponent', 'PerGame', year, ''])

urls = ['http://stats.nba.com/stats/',
        '?Conference=&DateFrom=&DateTo=&DefenseCategory=',
        ('&Division=&GameSegment=&LastNGames=0&LeagueID=00&Location='
         '&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode='),
        '&Period=0&Season=',
        ('&SeasonSegment=&SeasonType=Regular+Season&TeamID='
         '0&VsConference=&VsDivision=')
        ]
for year in seasons:
    url_to_json(urls,
                ['leaguedashptteamdefend',
                 'Less+Than+6Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashptteamdefend',
                 'Less+Than+10Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashptteamdefend',
                 'Greater+Than+15Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashptteamdefend',
                 '2+Pointers', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashptteamdefend',
                 '3+Pointers', 'PerGame', year, ''])

urls = ['http://stats.nba.com/stats/',
        '?CloseDefDistRange=',
        ('&College=&Conference=&Country=&DateFrom=&DateTo='
         '&Division=&DraftPick=&DraftYear=&DribbleRange='),
        '&GameScope=&GameSegment=&GeneralRange=',
        ('&Height=&LastNGames=0&LeagueID=00&Location=&Month=0'
         '&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode='),
        ('&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus='
         'N&Rank=N&Season='),
        ('&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange='
         '&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange='
         '&VsConference=&VsDivision=&Weight=')
        ]
for year in seasons:
    url_to_json(urls,
                ['leaguedashteamptshot', '', '',
                 'Less+Than+6Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashteamptshot', '', '',
                 'Greater+Than+15Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashplayerptshot', '', '',
                 'Less+Than+6Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashplayerptshot', '', '',
                 'Greater+Than+15Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashteamptshot', '', '',
                 'Less+Than+10Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashteamptshot', '', '',
                 'Overall', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashplayerptshot', '', '',
                 'Less+Than+10Ft', 'PerGame', year, ''])
    url_to_json(urls,
                ['leaguedashplayerptshot', '', '',
                 'Overall', 'PerGame', year, ''])
