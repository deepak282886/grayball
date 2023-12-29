import pandas as pd

import sqlite3
from player_analysis import get_batting_stats, get_bowling_stats


def player_info_bat(player, format, team, gender):
  cols = ['match_id', 'team', 'innings_number','over_number', 'powerplay_type', 'powerplay_number', 'ball_number', 'batter', 'batter_number', 'non_striker_number',
          'bowler', 'bowler_number','non_striker', 'runs_batter', 'extras_total', 'target_overs', 'target_runs', 'wickets_player_out',
          'wickets_kind', 'fielder1_wicket', 'fielder2_wicket', 'fielder3_wicket', 'legbyes_extras','wides_extras', 'byes_extras',
          'noballs_extras' ,'penalty_extras', 'match_id_2', 'balls_per_over', 'city', 'dates', 'event_name', 'event_match_number', 'gender', 'match_type',
          'match_type_number', 'official_match_referees', 'official_reserve_umpires', 'official_tv_umpires', 'official_umpires',
          'outcome_winner', 'outcome_wickets', 'outcome_runs', 'overs', 'player_of_match', 'players_team1', 'players_team2', 'season',
          'team_type', 'teams', 'toss_decision', 'toss_winner', 'venue', 'team1', 'team2']

  query = f"""
      SELECT *
      FROM ball_by_ball_data b
      LEFT JOIN match_info m ON b.match_id = m.match_id
      WHERE m.match_type = '{format}' AND
      (b.batter = '{player}' OR b.non_striker = '{player}')
      AND (
            ',' || m.team1 || ',' LIKE '%{team}%'
            OR ',' || m.team2 || ',' LIKE '%{team}%'
          )
      AND m.gender = '{gender}';
  """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()
  batsman_df = pd.read_sql_query(query, conn)
  batsman_df.columns = cols

  return batsman_df


def player_info_ball(player, format, team, gender):
  cols = ['match_id', 'team', 'innings_number','over_number', 'powerplay_type', 'powerplay_number', 'ball_number', 'batter', 'batter_number', 'non_striker_number',
          'bowler', 'bowler_number','non_striker', 'runs_batter', 'extras_total', 'target_overs', 'target_runs', 'wickets_player_out',
          'wickets_kind', 'fielder1_wicket', 'fielder2_wicket', 'fielder3_wicket', 'legbyes_extras','wides_extras', 'byes_extras',
          'noballs_extras' ,'penalty_extras', 'match_id_2', 'balls_per_over', 'city', 'dates', 'event_name', 'event_match_number', 'gender', 'match_type',
          'match_type_number', 'official_match_referees', 'official_reserve_umpires', 'official_tv_umpires', 'official_umpires',
          'outcome_winner', 'outcome_wickets', 'outcome_runs', 'overs', 'player_of_match', 'players_team1', 'players_team2', 'season',
          'team_type', 'teams', 'toss_decision', 'toss_winner', 'venue', 'team1', 'team2']


  query = f"""
      SELECT *
      FROM ball_by_ball_data b
      LEFT JOIN match_info m ON b.match_id = m.match_id
      WHERE m.match_type = '{format}' AND
      b.bowler = '{player}'
      AND (
            ',' || m.team1 || ',' LIKE '%{team}%'
            OR ',' || m.team2 || ',' LIKE '%{team}%'
          )
      AND m.gender = '{gender}'
  """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()

  bowler_df = pd.read_sql_query(query, conn)
  bowler_df.columns = cols

  return bowler_df

def get_recent_fielding_stats(format, player, team, recent_number, gender):
  cols = ['match_id', 'team', 'innings_number','over_number', 'powerplay_type', 'powerplay_number', 'ball_number', 'batter', 'batter_number', 'non_striker_number',
          'bowler', 'bowler_number','non_striker', 'runs_batter', 'extras_total', 'target_overs', 'target_runs', 'wickets_player_out',
          'wickets_kind', 'fielder1_wicket', 'fielder2_wicket', 'fielder3_wicket', 'legbyes_extras','wides_extras', 'byes_extras',
          'noballs_extras' ,'penalty_extras', 'match_id_2', 'balls_per_over', 'city', 'dates', 'event_name', 'event_match_number', 'gender', 'match_type',
          'match_type_number', 'official_match_referees', 'official_reserve_umpires', 'official_tv_umpires', 'official_umpires',
          'outcome_winner', 'outcome_wickets', 'outcome_runs', 'overs', 'player_of_match', 'players_team1', 'players_team2', 'season',
          'team_type', 'teams', 'toss_decision', 'toss_winner', 'venue', 'team1', 'team2']

  query = f"""
        SELECT *
        FROM ball_by_ball_data b
        LEFT JOIN match_info m ON b.match_id = m.match_id
        WHERE m.match_type = '{format}' AND
        (b.wickets_kind = 'run out' OR b.wickets_kind = 'caught' OR b.wickets_kind = 'stumped')
        AND
          (
            ',' || m.players_team1 || ',' LIKE '%{player}%'
            OR ',' || m.players_team2 || ',' LIKE '%{player}%'
          )
        AND (
            ',' || m.team1 || ',' LIKE '%{team}%'
            OR ',' || m.team2 || ',' LIKE '%{team}%'
          )
        AND m.gender = '{gender}'
    """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()

  field_df = pd.read_sql_query(query, conn)
  field_df.columns = cols
  match_5 = list(field_df["match_id"].unique()[-recent_number:])
  recent_field = field_df[field_df["match_id"].isin(match_5)]

  run_out = len(recent_field[recent_field["wickets_kind"] == "run out"])
  stumped = len(recent_field[recent_field["wickets_kind"] == "stumped"])
  catches = len(recent_field[recent_field["wickets_kind"] == "caught"])
  return run_out, stumped, catches

def get_fielding_stats(format, player, team, gender):
  cols = ['match_id', 'team', 'innings_number','over_number', 'powerplay_type', 'powerplay_number', 'ball_number', 'batter', 'batter_number', 'non_striker_number',
          'bowler', 'bowler_number','non_striker', 'runs_batter', 'extras_total', 'target_overs', 'target_runs', 'wickets_player_out',
          'wickets_kind', 'fielder1_wicket', 'fielder2_wicket', 'fielder3_wicket', 'legbyes_extras','wides_extras', 'byes_extras',
          'noballs_extras' ,'penalty_extras', 'match_id_2', 'balls_per_over', 'city', 'dates', 'event_name', 'event_match_number', 'gender', 'match_type',
          'match_type_number', 'official_match_referees', 'official_reserve_umpires', 'official_tv_umpires', 'official_umpires',
          'outcome_winner', 'outcome_wickets', 'outcome_runs', 'overs', 'player_of_match', 'players_team1', 'players_team2', 'season',
          'team_type', 'teams', 'toss_decision', 'toss_winner', 'venue', 'team1', 'team2']

  query = f"""
        SELECT *
        FROM ball_by_ball_data b
        LEFT JOIN match_info m ON b.match_id = m.match_id
        WHERE m.match_type = '{format}' AND
        (b.wickets_kind = 'run out' OR b.wickets_kind = 'caught' OR b.wickets_kind = 'stumped')
        AND
            (
              ',' || b.fielder1_wicket || ',' LIKE '%{player}%'
              OR ',' || b.fielder2_wicket || ',' LIKE '%{player}%'
            )
        AND (
            ',' || m.team1 || ',' LIKE '%{team}%'
            OR ',' || m.team2 || ',' LIKE '%{team}%'
          )
        AND m.gender = '{gender}'
    """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()

  field_df = pd.read_sql_query(query, conn)
  field_df.columns = cols

  run_out = len(field_df[field_df["wickets_kind"] == "run out"])
  stumped = len(field_df[field_df["wickets_kind"] == "stumped"])
  catches = len(field_df[field_df["wickets_kind"] == "caught"])
  return run_out, stumped, catches

def get_distinct_formats(player, gender):
  query = f"""
      SELECT
          DISTINCT m.match_type
      FROM match_info m
      WHERE (
              ',' || m.players_team1 || ',' LIKE '%{player}%'
              OR ',' || m.players_team2 || ',' LIKE '%{player}%'
            )
      AND m.gender = '{gender}'
    """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()

  format_df = pd.read_sql_query(query, conn)
  formats = list(format_df["match_type"].unique())

  return formats

def get_distinct_teams(player, gender):
  query = f"""
      SELECT
          m.players_team1, m.players_team2,
          m.team1, m.team2
      FROM match_info m
      WHERE (
              ',' || m.players_team1 || ',' LIKE '%{player}%'
              OR ',' || m.players_team2 || ',' LIKE '%{player}%'
            )
      AND m.gender = '{gender}'
    """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()
  
  format_df = pd.read_sql_query(query, conn)
  team1_df = format_df[format_df["players_team1"].str.contains(player)]
  team1_dis = list(team1_df["team1"].unique())
  team2_df = format_df[format_df["players_team2"].str.contains(player)]
  team2_dis = list(team2_df["team2"].unique())
  final_dis = list(set(team1_dis + team2_dis))

  return final_dis

def recent_data_bat(match_type,odi_bat, player, recent_number):
  recent = f"last {recent_number} {match_type} matches"
  match_5 = list(odi_bat["match_id"].unique()[-recent_number:])
  recent_bat = odi_bat[odi_bat["match_id"].isin(match_5)]
  text_5 = get_batting_stats(recent_bat, player, recent)
  return text_5

def recent_data_ball(match_type,odi_ball, player, recent_number):
  recent = f"last {recent_number} {match_type} matches"
  match_5 = list(odi_ball["match_id"].unique()[-recent_number:])
  recent_ball = odi_ball[odi_ball["match_id"].isin(match_5)]
  text_5 = get_bowling_stats(recent_ball, player, recent)
  return text_5

