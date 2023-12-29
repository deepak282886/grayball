import pandas as pd
from team_analysis import (group_bat, group_bowl, get_bat_text, 
get_ball_text)
import sqlite3

def team_info_bat(team, gender):
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
      WHERE '{team}' IN (m.team1, m.team2)
      AND b.team = '{team}'
      AND m.gender = '{gender}';
  """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()

  team_df = pd.read_sql_query(query, conn)
  team_df.columns = cols

  return team_df

def team_info_ball(team, gender):
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
      WHERE '{team}' IN (m.team1, m.team2)
      AND b.team != '{team}'
      AND m.gender = '{gender}';
  """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()

  team_df = pd.read_sql_query(query, conn)
  team_df.columns = cols

  return team_df

def get_distinct_formats_team(team, gender):
  query = f"""
      SELECT
          DISTINCT m.match_type
      FROM match_info m
      WHERE (
              ',' || m.team1 || ',' LIKE '%{team}%'
              OR ',' || m.team2 || ',' LIKE '%{team}%'
            )
      AND m.gender LIKE '%{gender}%'
    """
  conn = sqlite3.connect("cricket.db")
  cursor = conn.cursor()

  format_df = pd.read_sql_query(query, conn)
  formats = list(format_df["match_type"].unique())

  return formats

def get_fielding_stats_team(format, team, gender):
  cols = ['match_id', 'team', 'innings_number','over_number', 'powerplay_type', 'powerplay_number', 'ball_number', 'batter',
            'bowler', 'non_striker', 'runs_batter', 'extras_total', 'target_overs', 'target_runs', 'wickets_player_out',
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

  return field_df

def get_fielding_recent_stats_team(format, team, recent_number, gender):
  cols = ['match_id', 'team', 'innings_number','over_number', 'powerplay_type', 'powerplay_number', 'ball_number', 'batter',
            'bowler', 'non_striker', 'runs_batter', 'extras_total', 'target_overs', 'target_runs', 'wickets_player_out',
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

  return recent_field


def recent_data_bat_team(match_type,odi_bat, recent_number):
  match_5 = list(odi_bat["match_id"].unique()[-recent_number:])
  recent_bat = odi_bat[odi_bat["match_id"].isin(match_5)]
  text_5 = group_bat(recent_bat)
  text_bat = get_bat_text(text_5)
  return text_bat

def recent_data_ball_team(match_type,odi_ball, recent_number):
  match_5 = list(odi_ball["match_id"].unique()[-recent_number:])
  recent_ball = odi_ball[odi_ball["match_id"].isin(match_5)]
  text_5 = group_bowl(recent_ball)
  text_ball = get_ball_text(text_5)
  return text_ball

