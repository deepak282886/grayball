import pandas as pd

import sqlite3

# Assuming you are using SQLite as the database
conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

def slice_with_others(df, list_other):
  df["dates"] = pd.to_datetime(df["dates"])
  for key in list(list_other.keys()):
    if key == 'innings':
      df = df[df["innings_number"] == int(list_other["innings"])]

    elif key == 'overs_start':
      overs_start = list_other['overs_start']
      df = df[df["overs"] >= overs_start]
    elif key == 'overs_end':
      overs_end = list_other['overs_end']
      df = df[df["overs"] <= overs_end]
    elif key == "tournament":
      tournament = list_other['tournament']
      df = df[df["event_name"] == tournament]

    elif key =="venue":
      venue = list_other['venue']
      if 'opposing_venue' in list(list_other.keys()):
        opposing_venue = list_other['opposing_venue']
        df = df[df["venue"].isin([venue, opposing_venue])]
      else:
        df = df[df["venue"] == venue]

    elif key =="city":
      city = list_other['city']
      df = df[df["city"] == city]

    elif key == "margin_runs_start":
      margin_runs_start = list_other['margin_runs_start']
      df = df[df["outcome_runs"] >= margin_runs_start]

    elif key == "margin_runs_end":
      margin_runs_end = list_other['margin_runs_end']
      df = df[df["outcome_runs"] <= margin_runs_end]

    elif key == "margin_wickets_start":
      margin_wickets_start = list_other['margin_wickets_start']
      df = df[df["outcome_wickets"] >= margin_wickets_start]

    elif key == "margin_wickets_end":
      margin_wickets_end = list_other['margin_wickets_end']
      df = df[df["outcome_wickets"] <= margin_wickets_end]

    elif key == 'date_start':
      date_start = list_other['date_start']
      df = df[df["dates"] >= date_start]
    elif key == 'date_end':
      date_end = list_other['date_end']
      df = df[df["dates"] <= date_end]

    elif key == 'toss_result':
      toss_result = list_other['toss_result']
      df = df[df["toss_winner"] == toss_result]

    elif key == 'toss_decision':
      toss_decision = list_other['toss_decision']
      df = df[df["toss_decision"] == toss_result]

    elif key == 'batter_number':
      batter_number = list_other['batter_number']
      df = df[df["batter_number"].isin(batter_number)]
    
    elif key == 'bowler_number':
      bowler_number = list_other['bowler_number']
      df = df[df["bowler_number"].isin(bowler_number)]

  return df