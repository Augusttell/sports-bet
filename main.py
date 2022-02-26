import pandas as pd
import numpy as np
import datacollection as dc
import os
import tqdm


# league_id=1329
# date="2020-09-06"
# fixture_id=560041




current_wd = os.getcwd()
f = open("./apikey.txt", "r")
apikey = f.read()

header = {"X-RapidAPI-Key": apikey}


dc.return_leagues_id(header, "sweden", "2020")
dc.return_fixture_ids(header, 1312, "2020-09-12")


# Match 1
match1 = dc.fixture_predictions(header, 592144)

# Match 2
match2 = dc.fixture_predictions(header, 592142)

# Match 3
match3 = dc.fixture_predictions(header, 592148)

# Match 4
match4 = dc.fixture_predictions(header, 592883)

# Match 5
match5 = dc.fixture_predictions(header, 592882)

# Match 6
match6 = dc.fixture_predictions(header, 592885)

# Match 7
match7 = dc.fixture_predictions(header, 592886)

# Match 8
match8 = dc.fixture_predictions(header, 592887)

# Match 9
match9 = dc.fixture_predictions(header, 592888)

# Match 10
match10 = dc.fixture_predictions(header, 592889)

# Match 11
match11 = dc.fixture_predictions(header, 592890)

# Match 12
match12 = dc.fixture_predictions(header, 592891)

# Match 13
match13 = dc.fixture_predictions(header, 567046)

# Alla matcher
matcher = pd.DataFrame([match1, match2, match3, match4, match5, match6, match7,
                        match8,
                        match9, match10, match11, match12, match13],
                       columns=["forme_home", "forme_away", "att_home", "att_away", "def_home", "def_away",
                                "fish_law_home", "fish_law_away", "h2h_home", "h2h_away", "goals_h2h_home",
                                "goals_h2h_away", "Hemma_mål", "Borta_mål", "Hemma_vinst", "Oavgjort", "Borta_vinst",
                                "Match"])



# Predikterad vinst
matcher["Hemma_Oavgjort"]=np.abs(matcher["Hemma_vinst"]-matcher["Oavgjort"]) # Stort tal stor slh för hemma vinst
matcher["Hemma_borta"]=np.abs(matcher["Hemma_vinst"]-matcher["Borta_vinst"]) # Stort tal stor slh för oavgjort
matcher["Oavgjort_vinst"]=np.abs(matcher["Oavgjort"]-matcher["Borta_vinst"]) # Stort tal stor slh för borta vinst

matcher["Totalt"] = matcher["Hemma_Oavgjort"]+ matcher["Hemma_borta"]+matcher["Oavgjort_vinst"]
# matcher=matcher.sort_values(by="Totalt")

# Antal mål
matcher["Målskillnad, hemma plus borta minus"] = np.abs(matcher["Hemma_mål"])-np.abs(matcher["Borta_mål"])


# fish_law, h2h och h2h goal
matcher["Medelvärdet_score_hemma"] = (matcher["fish_law_home"]+matcher["h2h_home"]+matcher["goals_h2h_home"])/3
matcher["Medelvärdet__score_borta"] = (matcher["fish_law_away"]+matcher["h2h_away"]+matcher["goals_h2h_away"])/3

# Form
matcher["Medelvärdet_form_hemma"] = (matcher["forme_home"]+matcher["att_home"]+matcher["def_home"])/3
matcher["Medelvärdet_form_borta"] = (matcher["forme_away"]+matcher["att_away"]+matcher["def_away"])/3

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(matcher)


current_wd=os.getcwd()
os.mkdir(current_wd + "/tips/")
matcher.to_csv(path_or_buf=current_wd + "/tips/" + "strykTips_vecka_37_utanLag.csv", sep=","
                                          , header=True, index=False, decimal=".")