import requests
import re


def return_leagues_id(header, country, year):
    leagues = requests.get("https://api-football-v1.p.rapidapi.com/v2/leagues/country/" + str(country) + "/" + str(year),
                           headers=header).json()
    for league in leagues["api"]["leagues"]:
        print(league['league_id'], league['name'], league['country'], league['season'], league['is_current'])

def return_fixture_ids(header, league_id, date):
    fixtures = requests.get("https://api-football-v1.p.rapidapi.com/v2/fixtures/league/"+str(league_id)+"/"+date+
                            "?timezone=Europe/London", headers=header).json()
    for fix in fixtures["api"]["fixtures"]:
        print(fix['fixture_id'], ", Hemma:", fix['homeTeam']["team_name"], ", Borta:", fix['awayTeam']["team_name"])

def fixture_predictions(header, fixture_id):
    predictions = requests.get("https://api-football-v1.p.rapidapi.com/v2/predictions/" + str(fixture_id),
                               headers=header).json()
    percentage=(int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["winning_percent"]["goals_home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["winning_percent"]["goals_away"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["winning_percent"]["home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["winning_percent"]["draws"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["winning_percent"]["away"])[0]),
                "Hemma:" + predictions["api"]["predictions"][0]["teams"]["home"]["team_name"] + ", Borta: " + \
                predictions["api"]["predictions"][0]["teams"]["away"]["team_name"])
    return percentage


