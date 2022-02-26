import requests
import re
import pandas as pd

def return_leagues_id(header, country, year):
    #leagues = requests.get("https://api-football-v1.p.rapidapi.com/v2/leagues/country/" + str(country) + "/" + str(year),
    #                       headers=header).json()
    #leagues = requests.get("https://api-football-v1.p.rapidapi.com/v3" + str(country) + "&season=" + str(year), headers=header).json()
    querystring = {"country": country,
                   "season":year}

    leagues = requests.request("GET", "https://api-football-v1.p.rapidapi.com/v3/leagues",
                               headers=header, params=querystring).json()

    results = []
    for league in leagues["response"]:
        print(league)
        print(league["league"]["id"],
              league["league"]["name"],
              league["seasons"][0]["year"],
              league["country"]["name"],
              league["seasons"][0]["current"])


        temp_df = pd.DataFrame({"id":league["league"]["id"],
                                "name":league["league"]["name"],
                      "country":league["country"]["name"],
                                "season":league["seasons"][0]["year"],
                      "current":league["seasons"][0]["current"]},
                               index=[0])

        results.append(temp_df)

    results = pd.concat(results)

    results.reset_index(drop=True,inplace=True)

    return results

def return_fixture_ids(header, league_id, date):

    querystring = {"league": league_id, "season": date}

    fixtures = requests.request("GET", "https://api-football-v1.p.rapidapi.com/v3/fixtures",
                     headers=header, params=querystring).json()

    results = []
    for fixture in fixtures["response"]:
        temp_df = pd.DataFrame({"id": fixture["fixture"]["id"],
                                "date":fixture["fixture"]["date"],
                                "status": fixture["fixture"]["status"]["short"],
                                "league_id": fixture["league"]["id"],
                                "league_name": fixture["league"]["name"],
                                "home_team_id": fixture["teams"]["home"]["id"],
                                "home_team_name": fixture["teams"]["home"]["name"],
                                "away_team_id": fixture["teams"]["away"]["id"],
                                "away_team_name": fixture["teams"]["away"]["name"],
                                "goals_home": fixture["goals"]["home"],
                                "goals_away": fixture["goals"]["away"]}, index=[0])
        results.append(temp_df)

    return results


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


def get_team_stats(header, league, year, team_id, date):
    # https://www.api-football.com/documentation-v3#operation/get-teams-statistics
    querystring = {"league": league,
                   "season": year,
                   "team": team_id,
                   "date": date}


    stats = requests.request("GET",
                             "https://api-football-v1.p.rapidapi.com/v3/teams/statistics",
                             headers=header, params=querystring).json()

    print(stats)
    try:
        results = pd.DataFrame({"league_id": stats["response"]["league"]["id"],
                             "league_season": stats["response"]["league"]["season"],
                             "date": stats["parameters"]["date"],
                             "team_id": stats["response"]["team"]["id"],
                             "team_name": stats["response"]["team"]["name"],
                             "form": stats["response"]["form"],
                             "fixtures_wins_home": stats["response"]["fixtures"]["wins"][
                                 "home"],
                             "fixtures_wins_away": stats["response"]["fixtures"]["wins"][
                                 "away"],
                             "fixtures_draws_home":
                                 stats["response"]["fixtures"]["draws"]["home"],
                             "fixtures_draws_away":
                                 stats["response"]["fixtures"]["draws"]["away"],
                             "fixtures_loses_home":
                                 stats["response"]["fixtures"]["loses"]["home"],
                             "fixtures_loses_away":
                                 stats["response"]["fixtures"]["loses"]["away"],
                             "goals_for_total_home":
                                 stats["response"]["goals"]["for"]["total"]["home"],
                             "goals_for_total_away":
                                 stats["response"]["goals"]["for"]["total"]["away"],
                             "goals_for_total_total":
                                 stats["response"]["goals"]["for"]["total"]["total"],
                             "goals_for_average_home":
                                 stats["response"]["goals"]["for"]["average"]["home"],
                             "goals_for_average_away":
                                 stats["response"]["goals"]["for"]["average"]["away"],
                             "goals_for_average_total":
                                 stats["response"]["goals"]["for"]["average"]["total"],
                             "goals_for_total_home":
                                 stats["response"]["goals"]["for"]["total"]["home"],
                             "goals_for_total_away":
                                 stats["response"]["goals"]["for"]["total"]["away"],
                             "goals_for_total_total":
                                 stats["response"]["goals"]["for"]["total"]["total"],
                             "goals_for_average_home":
                                 stats["response"]["goals"]["for"]["average"]["home"],
                             "goals_for_average_away":
                                 stats["response"]["goals"]["for"]["average"]["away"],
                             "goals_for_average_total":
                                 stats["response"]["goals"]["for"]["average"]["total"],
                             "goals_for_minute_0-15_total":
                                 stats["response"]["goals"]["for"]["minute"]['0-15'][
                                     "total"],
                             "goals_for_minute_0-15_percentage":
                                 stats["response"]["goals"]["for"]["minute"]['0-15'][
                                     "percentage"],
                             "goals_for_minute_16-30_total":
                                 stats["response"]["goals"]["for"]["minute"]['16-30'][
                                     "total"],
                             "goals_for_minute_16-30_percentage":
                                 stats["response"]["goals"]["for"]["minute"]['16-30'][
                                     "percentage"],
                             "goals_for_minute_31-45_total":
                                 stats["response"]["goals"]["for"]["minute"]['31-45'][
                                     "total"],
                             "goals_for_minute_31-45_percentage":
                                 stats["response"]["goals"]["for"]["minute"]['31-45'][
                                     "percentage"],
                             "goals_for_minute_46-60_total":
                                 stats["response"]["goals"]["for"]["minute"]['46-60'][
                                     "total"],
                             "goals_for_minute_46-60_percentage":
                                 stats["response"]["goals"]["for"]["minute"]['46-60'][
                                     "percentage"],
                             "goals_for_minute_61-75_total":
                                 stats["response"]["goals"]["for"]["minute"]['61-75'][
                                     "total"],
                             "goals_for_minute_61-75_percentage":
                                 stats["response"]["goals"]["for"]["minute"]['61-75'][
                                     "percentage"],
                             "goals_for_minute_76-90_total":
                                 stats["response"]["goals"]["for"]["minute"]['76-90'][
                                     "total"],
                             "goals_for_minute_76-90_percentage":
                                 stats["response"]["goals"]["for"]["minute"]['76-90'][
                                     "percentage"],
                             "goals_for_minute_91-105_total":
                                 stats["response"]["goals"]["for"]["minute"]['91-105'][
                                     "total"],
                             "goals_for_minute_91-105_percentage":
                                 stats["response"]["goals"]["for"]["minute"]['91-105'][
                                     "percentage"],
                             "goals_for_minute_106-120_total":
                                 stats["response"]["goals"]["for"]["minute"]['106-120'][
                                     "total"],
                             "goals_for_minute_106-120_percentage":
                                 stats["response"]["goals"]["for"]["minute"]['106-120'][
                                     "percentage"],
                             "goals_against_total_home":
                                 stats["response"]["goals"]["against"]["total"]["home"],
                             "goals_against_total_away":
                                 stats["response"]["goals"]["against"]["total"]["away"],
                             "goals_against_total_total":
                                 stats["response"]["goals"]["against"]["total"]["total"],
                             "goals_for_average_home":
                                 stats["response"]["goals"]["for"]["average"]["home"],
                             "goals_for_average_away":
                                 stats["response"]["goals"]["for"]["average"]["away"],
                             "goals_for_average_total":
                                 stats["response"]["goals"]["for"]["average"]["total"],
                             "goals_for_minute_0-15_total":
                                 stats["response"]["goals"]["against"]["minute"]['0-15'][
                                     "total"],
                             "goals_for_minute_0-15_percentage":
                                 stats["response"]["goals"]["against"]["minute"]['0-15'][
                                     "percentage"],
                             "goals_for_minute_16-30_total":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '16-30']["total"],
                             "goals_for_minute_16-30_percentage":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '16-30']["percentage"],
                             "goals_for_minute_31-45_total":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '31-45']["total"],
                             "goals_for_minute_31-45_percentage":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '31-45']["percentage"],
                             "goals_for_minute_46-60_total":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '46-60']["total"],
                             "goals_for_minute_46-60_percentage":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '46-60']["percentage"],
                             "goals_for_minute_61-75_total":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '61-75']["total"],
                             "goals_for_minute_61-75_percentage":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '61-75']["percentage"],
                             "goals_for_minute_76-90_total":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '76-90']["total"],
                             "goals_for_minute_76-90_percentage":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '76-90']["percentage"],
                             "goals_for_minute_91-105_total":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '91-105']["total"],
                             "goals_for_minute_91-105_percentage":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '91-105']["percentage"],
                             "goals_for_minute_106-120_total":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '106-120']["total"],
                             "goals_for_minute_106-120_percentage":
                                 stats["response"]["goals"]["against"]["minute"][
                                     '106-120']["percentage"],
                             "biggest_streak_wins":
                                 stats["response"]["biggest"]['streak']['wins'],
                             "biggest_streak_draws":
                                 stats["response"]["biggest"]['streak']['draws'],
                             "biggest_streak_loses":
                                 stats["response"]["biggest"]['streak']['loses'],
                             "biggest_wins_home": stats["response"]["biggest"]['wins'][
                                 "home"],
                             "biggest_wins_away": stats["response"]["biggest"]['wins'][
                                 "away"],
                             "biggest_loses_home": stats["response"]["biggest"]['loses'][
                                 "home"],
                             "biggest_loses_away": stats["response"]["biggest"]['loses'][
                                 "away"],
                             "biggest_goals_for_home":
                                 stats["response"]["biggest"]['goals']["for"]["home"],
                             "biggest_goals_for_away":
                                 stats["response"]["biggest"]['goals']["for"]["away"],
                             "biggest_goals_against_home":
                                 stats["response"]["biggest"]['goals']["against"][
                                     "home"],
                             "biggest_goals_against_away":
                                 stats["response"]["biggest"]['goals']["against"][
                                     "away"],
                             "clean_sheet_home": stats["response"]["clean_sheet"][
                                 "home"],
                             "clean_sheet_away": stats["response"]["clean_sheet"][
                                 "away"],
                             "clean_sheet_total": stats["response"]["clean_sheet"][
                                 "total"],
                             "failed_to_score_home":
                                 stats["response"]["failed_to_score"]["home"],
                             "failed_to_score_away":
                                 stats["response"]["failed_to_score"]["away"],
                             "failed_to_score_total":
                                 stats["response"]["failed_to_score"]["total"],
                             "penalty_scored_total":
                                 stats["response"]["penalty"]["scored"]["total"],
                             "penalty_scored_percentage":
                                 stats["response"]["penalty"]["scored"]["percentage"],
                             "penalty_missed_total":
                                 stats["response"]["penalty"]["missed"]["total"],
                             "penalty_missed_percentage":
                                 stats["response"]["penalty"]["missed"]["percentage"],
                             "lineups": str(
                                 [x["formation"] + "_" + str(x["played"]) for x in
                                  stats["response"]["lineups"]]),
                             "cards_yellow_0-15_total":
                                 stats["response"]["cards"]["yellow"]["0-15"]["total"],
                             "cards_yellow_16-30_total":
                                 stats["response"]["cards"]["yellow"]["16-30"]["total"],
                             "cards_yellow_31-45_total":
                                 stats["response"]["cards"]["yellow"]["31-45"]["total"],
                             "cards_yellow_46-60_total":
                                 stats["response"]["cards"]["yellow"]["46-60"]["total"],
                             "cards_yellow_61-75_total":
                                 stats["response"]["cards"]["yellow"]["61-75"]["total"],
                             "cards_yellow_76-90_total":
                                 stats["response"]["cards"]["yellow"]["76-90"]["total"],
                             "cards_yellow_91-105_total":
                                 stats["response"]["cards"]["yellow"]["91-105"]["total"],
                             "cards_yellow_106-120_total":
                                 stats["response"]["cards"]["yellow"]["106-120"][
                                     "total"],
                             "cards_yellow_0-15_percentage":
                                 stats["response"]["cards"]["yellow"]["0-15"][
                                     "percentage"],
                             "cards_yellow_16-30_percentage":
                                 stats["response"]["cards"]["yellow"]["16-30"][
                                     "percentage"],
                             "cards_yellow_31-45_percentage":
                                 stats["response"]["cards"]["yellow"]["31-45"][
                                     "percentage"],
                             "cards_yellow_46-60_percentage":
                                 stats["response"]["cards"]["yellow"]["46-60"][
                                     "percentage"],
                             "cards_yellow_61-75_percentage":
                                 stats["response"]["cards"]["yellow"]["61-75"][
                                     "percentage"],
                             "cards_yellow_76-90_percentage":
                                 stats["response"]["cards"]["yellow"]["76-90"][
                                     "percentage"],
                             "cards_yellow_91-105_percentage":
                                 stats["response"]["cards"]["yellow"]["91-105"][
                                     "percentage"],
                             "cards_yellow_106-120_percentage":
                                 stats["response"]["cards"]["yellow"]["106-120"][
                                     "percentage"],
                             "cards_red_0-15_total":
                                 stats["response"]["cards"]["red"]["0-15"]["total"],
                             "cards_red_16-30_total":
                                 stats["response"]["cards"]["red"]["16-30"]["total"],
                             "cards_red_31-45_total":
                                 stats["response"]["cards"]["red"]["31-45"]["total"],
                             "cards_red_46-60_total":
                                 stats["response"]["cards"]["red"]["46-60"]["total"],
                             "cards_red_61-75_total":
                                 stats["response"]["cards"]["red"]["61-75"]["total"],
                             "cards_red_76-90_total":
                                 stats["response"]["cards"]["red"]["76-90"]["total"],
                             "cards_red_91-105_total":
                                 stats["response"]["cards"]["red"]["91-105"]["total"],
                             "cards_red_106-120_total":
                                 stats["response"]["cards"]["red"]["106-120"]["total"],
                             "cards_red_0-15_percentage":
                                 stats["response"]["cards"]["red"]["0-15"]["percentage"],
                             "cards_red_16-30_percentage":
                                 stats["response"]["cards"]["red"]["16-30"][
                                     "percentage"],
                             "cards_red_31-45_percentage":
                                 stats["response"]["cards"]["red"]["31-45"][
                                     "percentage"],
                             "cards_red_46-60_percentage":
                                 stats["response"]["cards"]["red"]["46-60"][
                                     "percentage"],
                             "cards_red_61-75_percentage":
                                 stats["response"]["cards"]["red"]["61-75"][
                                     "percentage"],
                             "cards_red_76-90_percentage":
                                 stats["response"]["cards"]["red"]["76-90"][
                                     "percentage"],
                             "cards_red_91-105_percentage":
                                 stats["response"]["cards"]["red"]["91-105"][
                                     "percentage"],
                             "cards_red_106-120_percentage":
                                 stats["response"]["cards"]["red"]["106-120"][
                                     "percentage"]}, index=[0])
    except Exception:
        print("no data")
        results = pd.DataFrame()


    return results


def get_injuries():
    # Get for each team in fixture: https://www.api-football.com/documentation-v3#tag/Injuries
    # Being a new endpoint, the data is only available from April 2021.

    return

def get_fix_stats(header, fixture_id):
    querystring = {"fixture": fixture_id}
    # https://www.api-football.com/documentation-v3#operation/get-fixtures-statistics

    stats = requests.request("GET",
                             "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics",
                             headers=header, params=querystring).json()

    try:
        results = pd.DataFrame({"ht_id": stats["response"][0]["team"]["id"],
                                "ht_name": stats["response"][0]["team"]["name"],
                                "at_id": stats["response"][1]["team"]["id"],
                                "at_name": stats["response"][1]["team"]["name"],
                                "fixture": stats["parameters"]["fixture"]}, index=[0])

        # Extract team 1 data
        df_1 = []
        for x in stats["response"][0]["statistics"]:
            df_1.append([x["type"], x["value"]])

        df_1 = pd.DataFrame([[x[1] for x in df_1]], columns=[x[0] for x in df_1])
        df_1.columns = ["ht_" + x for x in df_1.columns.str.replace(" ", "_")]

        # Extract team 2 data
        df_2 = []
        for x in stats["response"][1]["statistics"]:
            df_2.append([x["type"], x["value"]])

        df_2 = pd.DataFrame([[x[1] for x in df_2]], columns=[x[0] for x in df_2])

        df_2.columns = ["at_" + x for x in df_2.columns.str.replace(" ", "_")]

        results = pd.concat([results, df_1, df_2], axis=1)
    except Exception:
        results = pd.DataFrame()

    return results