from flask import Flask, render_template
from pybaseball import batting_stats, pitching_stats
from statsapi import schedule
from datetime import date
import concurrent.futures

app = Flask(__name__)

@app.route('/')
def main():
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
        "ARI":86,
        "ATL":110,
        "BAL":108,
        "BOS":98,
        "CHW":111,
        "CHC":106,
        "CIN":133,
        "CLE":91,
        "COL":108,
        "DET":77,
        "HOU":101,
        "KCR":80,
        "LAA":112,
        "LAD":123,
        "MIA":82,
        "MIL":109,
        "MIN":103,
        "NYY":116,
        "NYM":94,
        "OAK":84,
        "PHI":108,
        "PIT":82,
        "SDP":92,
        "SFG":84,
        "SEA":100,
        "STL":89,
        "TBR":94,
        "TEX":108,
        "TOR":106,
        "WSN":107 
    }

    #get today's game schedule
    start_date = date.today()
    games = schedule(start_date=start_date.strftime('%m/%d/%Y'))

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
            p_index[pitcher['Name']] = round(
                pitcher['HR/9+'] * 0.3 +
                pitcher['HR/FB%+'] * 0.25 +
                pitcher['HardHit%'] * 0.15 +
                pitcher['GB%+'] * 0.1 +
                pitcher['LD%+'] * 0.05 +
                pitcher['FB%+'] * 0.05 +
                pitcher['WHIP+'] * 0.1 +
                pitcher['K/9+'] * 0.05,
                3
            )

    #get all batter data with min. 100 ABs
    batter = batting_stats(2023, qual=100)
    batter_json = batter.to_dict(orient='records')

    #index map to each batter
    hitter_index = {}

    # Calculate the index for each batter and print it
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
        #pick home park
        for home_team, away_team in home_away_teams.items():
            if batter['Team'] == home_team or batter['Team'] == away_team: #if batter's team is equal to home team or away team
                park = home_team
        if probable_pitcher: #probable pitcher info exists
            hitter_index[batter['Name']] = (0.75 * batter_index + 0.15 * p_index[opposing_pitcher[batter['Team']]] + 0.1 * park_factor[park])
        else:
            hitter_index[batter['Name']] = (0.85 * batter_index + 0.15 * park_factor[park])

    sorted_hitter_index = dict(sorted(hitter_index.items(), key=lambda item: item[1], reverse=True))
    return render_template('index.html', hitter_index=sorted_hitter_index)
                           
if __name__ == '__main__':
    app.run(debug=True)