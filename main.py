import pandas as pd
import numpy as np
import datacollection as dc
import os


# league_id=1329
# date="2020-09-06"
# fixture_id=567040

dc.return_leagues_id(header, "sweden", "2020")
dc.return_fixture_ids(header, 1312, "2020-09-06")


current_wd = os.getcwd()
f = open("./apikey.txt", "r")
apikey = f.read()

header = {"X-RapidAPI-Key": apikey}


# TODO Most form strong matches
# Match 1
match1 = dc.fixture_predictions(header, 567041)

# Match 2
match2 = dc.fixture_predictions(header, 567042)

# Match 3
match3 = dc.fixture_predictions(header, 567045)

# Match 4
match4 = dc.fixture_predictions(header, 362041)

# Match 5
match5 = dc.fixture_predictions(header, 565041)

# Match 6
match6 = dc.fixture_predictions(header, 563041)

# Match 7
match7 = dc.fixture_predictions(header, 562041)

# Match 8
match8 = dc.fixture_predictions(header, 561041)

# Match 9
match9 = dc.fixture_predictions(header, 560041)

# Match 10
match10 = dc.fixture_predictions(header, 541041)

# Match 11
match11 = dc.fixture_predictions(header, 531041)

# Match 12
match12 = dc.fixture_predictions(header, 521041)

# Match 13
match13 = dc.fixture_predictions(header, 512041)

# Alla matcher
matcher = pd.DataFrame([match1, match2, match3, match4, match5, match6, match7,
                        match8, match9, match10, match11, match12, match13],
                       columns=["Hemma_mål", "Borta_mål", "Hemma_vinst", "Oavgjort", "Borta_vinst", "Match"])


matcher["Hemma_Oavgjort"]=np.abs(matcher["Hemma_vinst"]-matcher["Oavgjort"]) # Stort tal stor slh för hemma vinst
matcher["Hemma_borta"]=np.abs(matcher["Hemma_vinst"]-matcher["Borta_vinst"]) # Stort tal stor slh för oavgjort
matcher["Oavgjort_vinst"]=np.abs(matcher["Oavgjort"]-matcher["Borta_vinst"]) # Stort tal stor slh för borta vinst

matcher["Totalt"] = matcher["Hemma_Oavgjort"]+ matcher["Hemma_borta"]+matcher["Oavgjort_vinst"]


matcher=matcher.sort_values(by="Totalt")

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(matcher)