from nba_scrape import url_to_json
seasons = ['2013-14', '2014-15', '2015-16', '2016-17']


urls = ['http://stats.nba.com/stats/',
        '?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=',
        '&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=',
        '&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=',
        '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
        ]

for year in seasons:
    url_to_json(urls, ['leaguedashplayerstats', 'Base', 'PerGame', year, '']) 
    url_to_json(urls, ['leaguedashplayerstats', 'Advanced', 'PerGame', year,'']) 
    url_to_json(urls, ['leaguedashplayerstats', 'Misc', 'PerGame', year,''])

urls = ['http://stats.nba.com/stats/leaguedashplayer',
        '?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=',
        '&Period=0&PlayerExperience=&PlayerPosition=&Season=',
        '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
        ]
for year in seasons:
    url_to_json(urls, ['biostats', 'PerGame',year,''])

urls = ['http://stats.nba.com/stats/',
        '?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=',
        '&PlayerExperience=&PlayerOrTeam=',
        '&PlayerPosition=&PtMeasureType=',
        '&Season=',
        '&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
        ]

for year in seasons:
    url_to_json(urls, ['leaguedashptstats','PerGame', 'Team', 'Efficiency', year, ''])
    url_to_json(urls, ['leaguedashptstats','PerGame', 'Team', 'Passing', year, ''])
    url_to_json(urls, ['leaguedashptstats','PerGame', 'Team', 'SpeedDistance', year, ''])
    url_to_json(urls, ['leaguedashptstats','PerGame', 'Team', 'Rebounding', year, ''])
    url_to_json(urls, ['leaguedashptstats','PerGame', 'Team', 'Possessions', year, ''])

urls = ['http://stats.nba.com/stats/',
        '?College=&Conference=&Country=&DateFrom=&DateTo=&DistanceRange=By+Zone&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=',
        '&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=',
        '&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=',
        '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=',
        ]
for year in seasons:
    url_to_json(urls, ['leaguedashplayershotlocations', 'Base', 'PerGame', year, ''])

urls = ['http://stats.nba.com/stats/',	
        '?College=&Conference=&Country=&DateFrom=&DateTo=&DefenseCategory=',
        '&Division=&DraftPick=&DraftYear=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=',
        '&Period=0&PlayerExperience=&PlayerPosition=&Season=',
        '&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
        ]

for year in seasons:
    url_to_json(urls, ['leaguedashptdefend', 'Less+Than+6Ft','PerGame', year, ''])
    url_to_json(urls, ['leaguedashptdefend', 'Less+Than+10Ft','PerGame', year, ''])
    url_to_json(urls, ['leaguedashptdefend', 'Greater+Than+15Ft','PerGame', year, ''])
    url_to_json(urls, ['leaguedashptdefend', '2+Pointers','PerGame', year, ''])
    url_to_json(urls, ['leaguedashptdefend', '3+Pointers','PerGame', year, ''])