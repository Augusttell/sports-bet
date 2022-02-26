import pandas as pd
import os
from datetime import timedelta
from tqdm import tqdm

# Setup
current_wd = os.getcwd()
f = open("./apikey.txt", "r")
apikey = f.read()



#england = return_leagues_id(headers, "England", "2020")
#sweden = return_leagues_id(headers, "Sweden", "2020")

# Selected countries and years
countries = ["Sweden",
             "England"
             ]
years = [#"2017"
     #"2018"
    #"2019"
    "2020","2021"
    ]

# competitions
eng_comps = [#"Premier League",
   "FA Cup",
    "Community Shield"
  #"Championship"
             ]
swe_comps = [#"Superettan",
           # "Allsvenskan"#,
           # "Svenska Cupen"
            ]
sel_comps = eng_comps + swe_comps

# Extract leagues
all_leagues = []
for year in tqdm(years):
    for country in countries:
        temp_leagues = return_leagues_id(headers, country, year)
        all_leagues.append(temp_leagues)

all_leagues = pd.concat(all_leagues)
all_leagues.reset_index(drop=True, inplace=True)
# Filter out unwanted leagues
all_leagues = all_leagues.loc[all_leagues.name.isin(sel_comps)]

## Extract all the fixtures
all_fixtures = []
for year in tqdm(years):
    for league in all_leagues["id"].astype(str).values:
        temp_fixture = return_fixture_ids(headers, league, year)
        temp_fixture = pd.concat(temp_fixture)
        all_fixtures.append(temp_fixture)

all_fixtures = pd.concat(all_fixtures)
all_fixtures.reset_index(drop=True, inplace=True)
all_fixtures["date"] = pd.to_datetime(all_fixtures["date"]) # Convert to date for proper usage


all_fixtures = all_fixtures.loc[all_fixtures["league_name"] != "EFL Trophy"]
all_fixtures = all_fixtures.loc[all_fixtures["date"] <"2022-02-05"]
# Extract match stats for allall_fixtures[all_fixtures["league_name"] != "EFL Trophy"]
# Predict fixture stats as a betting model??
fixture_stats = []
for fix in tqdm(range(0, all_fixtures.shape[0])):
    print(all_fixtures["id"].iloc[fix])
    fixture_stats.append(get_fix_stats(headers, all_fixtures["id"].iloc[fix]))
fixture_stats = pd.concat(fixture_stats) # Combine all seasons
fixture_stats.reset_index(drop=True, inplace=True)

# Drop fixtures with missing data
all_fixtures = all_fixtures.loc[all_fixtures["id"].isin(fixture_stats["fixture"])]

# Extract team stats
all_teams_stats = []
for fixture in tqdm(range(0, all_fixtures.shape[0])):
        # Fetch day before fixture
    day_before = all_fixtures["date"].iloc[fixture].date() - timedelta(days=1)
    home_team_id = all_fixtures["home_team_id"].iloc[fixture]
    away_team_id = all_fixtures["away_team_id"].iloc[fixture]

    # Fetch home team data
    home_team = get_team_stats(headers,
        all_fixtures["league_id"].iloc[fixture],
        all_fixtures["date"].iloc[fixture].strftime("%Y"),
        all_fixtures["home_team_id"].iloc[fixture],
        day_before)

    # fetch away team data
    away_team = get_team_stats(headers,
        all_fixtures["league_id"].iloc[fixture],
        all_fixtures["date"].iloc[fixture].strftime("%Y"),
        all_fixtures["away_team_id"].iloc[fixture],
        day_before)

    home_team["fixture_id"] = all_fixtures["id"].iloc[fixture]
    away_team["fixture_id"] = all_fixtures["id"].iloc[fixture]
    fixture_team_stats_temp = home_team.merge(away_team, on="fixture_id",
                                              suffixes=["_home", "_away"])
    all_teams_stats.append(fixture_team_stats_temp)

all_teams_stats = pd.concat(all_teams_stats)
all_teams_stats.reset_index(inplace=True)

all_teams_stats_copy=all_teams_stats.copy()
fixture_stats_copy=fixture_stats.copy()
all_fixtures_copy=all_fixtures.copy()

#all_teams_stats_copy.to_csv(os.getcwd() + "/data/all_fixture_stats_2020_prem_champ.csv", index=None)
#fixture_stats_copy.to_csv(os.getcwd() + "/data/fixture_stats_2020_prem_champ.csv", index=None)
#all_fixtures_copy.to_csv(os.getcwd() + "/data/all_fixtures_2020_prem_champ.csv", index=None)

# Merge match stats  with fixture
all_fixtures_copy["id"] = all_fixtures_copy["id"].astype(str)
combined_data  = all_fixtures_copy.merge(fixture_stats_copy, left_on=["id"], right_on=["fixture"], how="inner")

# Change back date for matching with fixture
all_teams_stats_copy["date_home"] = pd.to_datetime(all_teams_stats_copy["date_home"]).dt.date +timedelta(days=1)
all_teams_stats_copy["date_away"] = pd.to_datetime(all_teams_stats_copy["date_away"]).dt.date +timedelta(days=1)

# Add on team stas
all_teams_stats_copy["fixture_id"] = all_teams_stats_copy["fixture_id"].astype(str)
combined_data = combined_data.merge(all_teams_stats_copy, left_on="id", right_on="fixture_id")


try:
    os.makedirs(os.getcwd() + "/data")
except FileExistsError:
    print("Folder already exists")

combined_data.to_csv(os.getcwd() + "/data/unprocessed_data_2020_2021_fa_com.csv", index=None)


# allsvenskan har sedan 2017
# Championship har sedan 2017
# Premier league ha sedan 2017
# Superettan har inte sedan 2017/2019
# Svenska Cupen har inte sedan 2017/2019
# FA Cup
# EFL Trophy
# Community Shield



fix = 380
seasons = 1
leagues = 2
t_stats = 2
teams = 2

tot_fixes = fix*seasons*leagues
queries = tot_fixes + (tot_fixes*teams*t_stats)
print(queries, queries/7500)


