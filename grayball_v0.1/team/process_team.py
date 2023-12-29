import pandas as pd
import re
from team_db_calls import (team_info_bat,team_info_ball, get_distinct_formats_team,
recent_data_ball_team, recent_data_bat_team, get_fielding_recent_stats_team,
get_fielding_stats_team)
from team_analysis import (group_bat, group_bowl, get_ball_text, get_bat_text,
get_fielding_text_team)
from query_handing.common_utils import slice_with_others

def process_team_recent_bat(list_other):
  team_u = list_other["team"]
  gender = list_other["gender"]
  if 'format' in list(list_other.keys()):
    formats = list_other["format"]
  else:
    formats = get_distinct_formats_team(team_u, gender)

  batsman_df = team_info_bat(team_u, gender)
  batsman_df["dates"] = pd.to_datetime(batsman_df["dates"])
  batsman_df = batsman_df.sort_values(by=["dates"])
  
  recent_text = ""

  for format in formats:
    bat_df = batsman_df[batsman_df["match_type"] == format]
    bat_df = slice_with_others(bat_df, list_other)
    if len(bat_df):
      text_5_bat = recent_data_bat_team(format,bat_df, list_other["recent_number"])
      text_5_bat = re.sub(' +', ' ', text_5_bat)
      recent_text += f"For {team_u}"
      recent_text += text_5_bat

  return recent_text

def process_team_recent_ball(list_other):
  team_u = list_other["team"]
  gender = list_other["gender"]
  if 'format' in list(list_other.keys()):
    formats = list_other["format"]
  else:
    formats = get_distinct_formats_team(team_u, gender)

  bowler_df = team_info_ball(team_u, gender)
  bowler_df["dates"] = pd.to_datetime(bowler_df["dates"])
  bowler_df = bowler_df.sort_values(by=["dates"])
  
  recent_text = ""

  for format in formats:
    bowl_df = bowler_df[bowler_df["match_type"] == format]
    bowl_df = slice_with_others(bowl_df, list_other)
    if len(bowl_df):
      text_5_ball = recent_data_ball_team(format,bowl_df, list_other["recent_number"])
      text_5_ball = re.sub(' +', ' ', text_5_ball)
      recent_text += f"For {team_u}"
      recent_text += text_5_ball

  return recent_text

def process_team_recent_field(list_other):
  team_u = list_other["team"]
  gender = list_other["gender"]
  if 'format' in list(list_other.keys()):
    formats = list_other["format"]
  else:
    formats = get_distinct_formats_team(team_u, gender)

  field_stats_text = ""

  field_df = get_fielding_recent_stats_team(format, team_u, list_other["recent_number"], gender)
  field_text = get_fielding_text_team(field_df, team_u, format)
  field_stats_text += field_text

  return field_stats_text

def process_team_bat(list_other):
  team_u = list_other["team"]
  gender = list_other["gender"]

  if 'format' in list(list_other.keys()):
    formats = list_other["format"]
  else:
    formats = get_distinct_formats_team(team_u, gender)

  batsman_df = team_info_bat(team_u, gender)
  batsman_df["dates"] = pd.to_datetime(batsman_df["dates"])
  batsman_df = batsman_df.sort_values(by=["dates"])

  all_text = ""
  for format in formats:
    bat_df = batsman_df[batsman_df["match_type"] == format]
    bat_df = slice_with_others(bat_df, list_other)
    
    if len(bat_df):
        df_bat = group_bat(bat_df)
        text_bat = get_bat_text(df_bat)
        text_bat = re.sub(' +', ' ', text_bat)
        all_text += f"For {team_u}"
        all_text += text_bat

  return all_text

def process_team_ball(list_other):
  team_u = list_other["team"]
  gender = list_other["gender"]

  if 'format' in list(list_other.keys()):
    formats = list_other["format"]
  else:
    formats = get_distinct_formats_team(team_u, gender)

  bowler_df = team_info_ball(team_u, gender)
  bowler_df["dates"] = pd.to_datetime(bowler_df["dates"])
  bowler_df = bowler_df.sort_values(by=["dates"])

  all_text = ""
  for format in formats:
    bowl_df = bowler_df[bowler_df["match_type"] == format]
    bowl_df = slice_with_others(bowl_df, list_other)
    if len(bowl_df):
        df_ball = group_bowl(bowl_df)
        text_ball = get_ball_text(df_ball)
        text_ball = re.sub(' +', ' ', text_ball)
        all_text += f"For {team_u}"
        all_text += text_ball

  return all_text

def process_team_field(list_other):
  team_u = list_other["team"]
  gender = list_other["gender"]

  if 'format' in list(list_other.keys()):
    formats = list_other["format"]
  else:
    formats = get_distinct_formats_team(team_u, gender)

  field_stats_text = ""

  field_df = get_fielding_stats_team(format, team_u, gender)
  field_text = get_fielding_text_team(field_df, team_u, format)
  field_stats_text += field_text

  return field_stats_text