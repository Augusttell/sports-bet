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
    percentage=(int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["forme"]["home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["forme"]["away"])[0]),

                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["att"]["home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["att"]["away"])[0]),

                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["def"]["home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["def"]["away"])[0]),

                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["fish_law"]["home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["fish_law"]["away"])[0]),

                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["h2h"]["home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["h2h"]["away"])[0]),

                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["goals_h2h"]["home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["comparison"]["goals_h2h"]["away"])[0]),

                predictions["api"]["predictions"][0]["goals_home"],
                predictions["api"]["predictions"][0]["goals_away"],

                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["winning_percent"]["home"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["winning_percent"]["draws"])[0]),
                int(re.findall('[0-9]+', predictions["api"]["predictions"][0]["winning_percent"]["away"])[0]),

                "Hemma:" + predictions["api"]["predictions"][0]["teams"]["home"]["team_name"] + ", Borta: " + \
                predictions["api"]["predictions"][0]["teams"]["away"]["team_name"])
    return percentage


