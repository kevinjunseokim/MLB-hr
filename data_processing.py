from datetime import date
from pybaseball import batting_stats, pitching_stats
from statsapi import schedule
import heapq

def calculate_top_hitters():
    team_mapping = {
        "Arizona Diamondbacks": "ARI",
        "Atlanta Braves": "ATL",
        "Baltimore Orioles": "BAL",
        "Boston Red Sox": "BOS",
        "Chicago White Sox": "CHW",
        "Chicago Cubs": "CHC",
        "Cincinnati Reds": "CIN",
        "Cleveland Guardians": "CLE",
        "Colorado Rockies": "COL",
        "Detroit Tigers": "DET",
        "Houston Astros": "HOU",
        "Kansas City Royals": "KCR",
        "Los Angeles Angels": "LAA",
        "Los Angeles Dodgers": "LAD",
        "Miami Marlins": "MIA",
        "Milwaukee Brewers": "MIL",
        "Minnesota Twins": "MIN",
        "New York Yankees": "NYY",
        "New York Mets": "NYM",
        "Oakland Athletics": "OAK",
        "Philadelphia Phillies": "PHI",
        "Pittsburgh Pirates": "PIT",
        "San Diego Padres": "SDP",
        "San Francisco Giants": "SFG",
        "Seattle Mariners": "SEA",
        "St. Louis Cardinals": "STL",
        "Tampa Bay Rays": "TBR",
        "Texas Rangers": "TEX",
        "Toronto Blue Jays": "TOR",
        "Washington Nationals": "WSN"
    }

    park_factor = {
        "default":1.00,
        "ARI":0.86,
        "ATL":1.10,
        "BAL":1.08,
        "BOS":0.98,
        "CHW":1.11,
        "CHC":1.06,
        "CIN":1.33,
        "CLE":0.91,
        "COL":1.08,
        "DET":0.77,
        "HOU":1.01,
        "KCR":0.80,
        "LAA":1.12,
        "LAD":1.23,
        "MIA":0.82,
        "MIL":1.09,
        "MIN":1.03,
        "NYY":1.16,
        "NYM":0.94,
        "OAK":0.84,
        "PHI":1.08,
        "PIT":0.82,
        "SDP":0.92,
        "SFG":0.84,
        "SEA":1.00,
        "STL":0.89,
        "TBR":0.94,
        "TEX":1.08,
        "TOR":1.06,
        "WSN":1.07 
    }

    #get today's game schedule
    start_date = date.today()
    games = schedule(start_date=start_date.strftime('%Y-%m-%d'))

    #pitching data
    pitching_data = pitching_stats(2023, league='all', qual=1)
    pitching_data_json = pitching_data.to_dict(orient='records')

    #pitcher index
    p_index = {}

    #find probable pitchers
    opposing_pitcher = {}

    home_away_teams = {}

    for game in games:
        home_team = game['home_name']
        away_team = game['away_name']
        home_pitcher = game['home_probable_pitcher']
        away_pitcher = game['away_probable_pitcher']

        home_away_teams[team_mapping[home_team]] = team_mapping[away_team]

        opposing_pitcher[team_mapping[home_team]] = away_pitcher
        opposing_pitcher[team_mapping[away_team]] = home_pitcher
    
    for pitcher in pitching_data_json:
        if pitcher['Name'] in opposing_pitcher.values():
            p_index[pitcher['Name']] = (200 + round(
                pitcher['HR/9+'] * 0.3 +
                pitcher['HR/FB%+'] * 0.25 +
                pitcher['HardHit%'] * 0.15 +
                pitcher['GB%+'] * 0.1 +
                pitcher['LD%+'] * 0.05 +
                pitcher['FB%+'] * 0.05 +
                pitcher['WHIP+'] * 0.1 +
                pitcher['K/9+'] * 0.05,
                3
            )) / 3

    #get all batter data with min. 100 ABs
    batter = batting_stats(2023, qual=100)
    batter_json = batter.to_dict(orient='records')

    top_20_heap = []
    park = "default"

    park = "default"

    for batter in batter_json:
        probable_pitcher = opposing_pitcher.get(batter['Team'])

        batter_index = round(
            10 * (batter['SLG'] * 0.15 +
                batter['ISO'] * 0.15 +
                batter['HR/FB'] * 0.12 +
                batter['Barrel%'] * 0.1 +
                batter['EV'] * 0.1 +
                batter['LA'] * 0.08 +
                batter['HardHit%'] * 0.1 +
                batter['wOBA'] * 0.12 +
                batter['Pull%'] * 0.08),
            3
        )
        # Pick home park
        for home_team, away_team in home_away_teams.items():
            if batter['Team'] == home_team or batter['Team'] == away_team:
                park = home_team

                if probable_pitcher:  # probable pitcher info exists
                    index = ((0.7 * batter_index + 0.3 * p_index[opposing_pitcher[batter['Team']]])) * (1 + (park_factor[park] - 1)/100)
                else:
                    index = ((0.7 * batter_index + 0.3)) * (1 + (park_factor[park] - 1)/100)

                heapq.heappush(top_20_heap, (index, batter['Name'], batter['Team']))

                if len(top_20_heap) > 20:
                    heapq.heappop(top_20_heap)

    top_20_hitters = [(name, index, team) for index, name, team in top_20_heap]
    top_20_hitters.sort(key= lambda x: -x[1])

    return top_20_hitters
