import pandas as pd
from player_db_calls import (player_info_bat, player_info_ball, recent_data_bat, recent_data_ball, get_recent_fielding_stats, get_fielding_stats
, get_distinct_formats, get_distinct_teams)
from grayball_v0.query_handling.common_utils import slice_with_others
from player_analysis import get_batting_stats, get_bowling_stats, get_fielding_text_player


def process_player_recent_bat(list_other):
    player = list_other["player"]
    gender = list_other["gender"]
    if 'format_type' in list(list_other.keys()):
        format_types = list_other["format_type"]
    else:
        format_types = get_distinct_formats(player, gender)
    if 'team' in list(list_other.keys()):
        unique_teams = list([list_other["team"]])
    else:
        unique_teams = get_distinct_teams(player, gender)
  
    recent_text = ""
    for u_team in unique_teams:
        for format_type in format_types:
            batsman_df = player_info_bat(player, format_type, u_team, gender)
            batsman_df["dates"] = pd.to_datetime(batsman_df["dates"])
            batsman_df = batsman_df.sort_values(by=["dates"])
            bat_df = slice_with_others(batsman_df, list_other)
            if len(bat_df):
                text_5_bat = recent_data_bat(format_type,bat_df, player, list_other["recent_number"])
                recent_text += f"For {u_team}"
                recent_text += text_5_bat

    return recent_text


def process_player_recent_ball(list_other):
    player = list_other["player"]
    gender = list_other["gender"]
    if 'format_type' in list(list_other.keys()):
        format_types = list_other["format_type"]
    else:
        format_types = get_distinct_formats(player, gender)
    if 'team' in list(list_other.keys()):
        unique_teams = list([list_other["team"]])
    else:
        unique_teams = get_distinct_teams(player, gender)
    recent_text = ""

    for u_team in unique_teams:
        for format_type in format_types:
            bowler_df = player_info_ball(player, format_type, u_team, gender)
            bowler_df["dates"] = pd.to_datetime(bowler_df["dates"])
            bowler_df = bowler_df.sort_values(by=["dates"])
            bowl_df = slice_with_others(bowler_df, list_other)
            if len(bowl_df):
                text_5_ball = recent_data_ball(format_type,bowl_df, player, list_other["recent_number"])
                recent_text += f"For {u_team}"
                recent_text += text_5_ball

    return recent_text


def process_player_recent_field(list_other):
    player = list_other["player"]
    gender = list_other["gender"]
    if 'format_type' in list(list_other.keys()):
        format_types = list_other["format_type"]
    else:
        format_types = get_distinct_formats(player, gender)
    if 'team' in list(list_other.keys()):
        unique_teams = list([list_other["team"]])
    else:
        unique_teams = get_distinct_teams(player, gender)

    field_text = ""
    field_stats_list = []
    for u_team in unique_teams:
        for format_type in format_types:
            field_stats = get_recent_fielding_stats(format_type, player, u_team, list_other["recent_number"], gender)
            field_stats_list.append({"team": u_team, "player": player, "stats": field_stats, "format_type": format_type})

    if len(field_stats_list):
        field_text = get_fielding_text_player(field_stats_list)
    return field_text


def process_player_field(list_other):
    player = list_other["player"]
    gender = list_other["gender"]
    if 'format_type' in list(list_other.keys()):
        format_types = list_other["format_type"]
    else:
        format_types = get_distinct_formats(player, gender)
    if 'team' in list(list_other.keys()):
        unique_teams = list([list_other["team"]])
    else:
        unique_teams = get_distinct_teams(player, gender)

    field_text = ""
    field_stats_list = []
    for u_team in unique_teams:
        for format_type in format_types:
            field_stats = get_fielding_stats(format_type, player, u_team, gender)
            field_stats_list.append({"team": u_team, "player": player, "stats": field_stats, "format_type": format_type})

    if len(field_stats_list):
        field_text = get_fielding_text_player(field_stats_list)
    return field_text


def process_player_bat(list_other):
    player = list_other["player"]
    gender = list_other["gender"]
    if 'format_type' in list(list_other.keys()):
        format_types = list_other["format_type"]
    else:
        format_types = get_distinct_formats(player, gender)
    if 'team' in list(list_other.keys()):
        unique_teams = list([list_other["team"]])
    else:
        unique_teams = get_distinct_teams(player, gender)

    all_text = ""

    for u_team in unique_teams:
        for format_type in format_types:
            batsman_df = player_info_bat(player, format_type, u_team, gender)
            batsman_df["dates"] = pd.to_datetime(batsman_df["dates"])
            batsman_df = batsman_df.sort_values(by=["dates"])

            bat_df = slice_with_others(batsman_df, list_other)

            if len(bat_df):
                text_bat = get_batting_stats(bat_df, player, format_type)
                all_text += f"For {u_team} {text_bat}"

    return all_text


def process_player_ball(list_other):
    player = list_other["player"]
    gender = list_other["gender"]
    if 'format_type' in list(list_other.keys()):
        format_types = list_other["format_type"]
    else:
        format_types = get_distinct_formats(player, gender)
    if 'team' in list(list_other.keys()):
        unique_teams = list([list_other["team"]])
    else:
        unique_teams = get_distinct_teams(player, gender)

    all_text = ""
    for u_team in unique_teams:
        for format_type in format_types:
            bowler_df = player_info_ball(player, format_type, u_team, gender)
            bowler_df["dates"] = pd.to_datetime(bowler_df["dates"])
            bowler_df = bowler_df.sort_values(by=["dates"])
            bowl_df = slice_with_others(bowler_df, list_other)
            if len(bowl_df):
                text_ball = get_bowling_stats(bowl_df, player, format_type)
                all_text += f"For {u_team} {text_ball}"
        
    return all_text
