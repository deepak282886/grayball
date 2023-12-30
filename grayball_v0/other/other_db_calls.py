import pandas as pd
import sqlite3


def ground_info(stadium, gender):
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
      WHERE m.venue = '{stadium}'
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")
    ground_df = pd.read_sql_query(query, conn)
    ground_df.columns = cols

    return ground_df


def tournament_info(tournament, gender):
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
      WHERE m.event_name = '{tournament}'
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")

    tour_df = pd.read_sql_query(query, conn)
    tour_df.columns = cols

    return tour_df


def get_matches_player(player, format_type, team, gender):
    query = f"""
    SELECT
        COUNT(DISTINCT m.match_id) AS total_matches
    FROM match_info m
    WHERE
        m.match_type = '{format_type}'
        AND (
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
    cursor = conn.execute(query)
    result = cursor.fetchone()
    total_matches = result[0]

    return total_matches


def format_info(format_type, gender):
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
      WHERE m.match_type = '{format_type}'
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")

    format_df = pd.read_sql_query(query, conn)
    format_df.columns = cols

    return format_df

def innings_info(innings, gender):
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
      WHERE b.innings_number = '{innings}'
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")
    innings_df = pd.read_sql_query(query, conn)
    innings_df.columns = cols

    return innings_df


def overs_info(overs_start, overs_end, gender):
    cols = ['match_id', 'team', 'innings_number','over_number', 'powerplay_type', 'powerplay_number', 'ball_number', 'batter', 'batter_number', 'non_striker_number',
          'bowler', 'bowler_number','non_striker', 'runs_batter', 'extras_total', 'target_overs', 'target_runs', 'wickets_player_out',
          'wickets_kind', 'fielder1_wicket', 'fielder2_wicket', 'fielder3_wicket', 'legbyes_extras','wides_extras', 'byes_extras',
          'noballs_extras' ,'penalty_extras', 'match_id_2', 'balls_per_over', 'city', 'dates', 'event_name', 'event_match_number', 'gender', 'match_type',
          'match_type_number', 'official_match_referees', 'official_reserve_umpires', 'official_tv_umpires', 'official_umpires',
          'outcome_winner', 'outcome_wickets', 'outcome_runs', 'overs', 'player_of_match', 'players_team1', 'players_team2', 'season',
          'team_type', 'teams', 'toss_decision', 'toss_winner', 'venue', 'team1', 'team2']

    if len(overs_start):
        if int(overs_start) > 0:
            overs_start = int(overs_start)
        else:
            overs_start = 0

    if len(overs_end):
        if int(overs_end) > 0:
            overs_end = int(overs_end)
        else:
            overs_end = 1000

    query = f"""
      SELECT *
      FROM ball_by_ball_data b
      LEFT JOIN match_info m ON b.match_id = m.match_id
      WHERE (b.over_number BETWEEN '{overs_start}' AND '{overs_end}')
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")
    overs_df = pd.read_sql_query(query, conn)
    overs_df.columns = cols

    return overs_df


def city_info(city, gender):
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
      WHERE m.city = '{city}'
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")
    city_df = pd.read_sql_query(query, conn)
    city_df.columns = cols

    return city_df


def margin_runs_info(margin_runs_start, margin_runs_end, gender):
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
      WHERE (m.outcome_runs BETWEEN '{margin_runs_start}' AND '{margin_runs_end}')
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")
    margin_runs_df = pd.read_sql_query(query, conn)
    margin_runs_df.columns = cols

    return margin_runs_df


def margin_wickets_info(margin_wickets_start, margin_wickets_end, gender):
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
      WHERE (m.outcome_wickets BETWEEN '{margin_wickets_start}' AND '{margin_wickets_end})
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")
    margin_wickets_df = pd.read_sql_query(query, conn)
    margin_wickets_df.columns = cols

    return margin_wickets_df


def dates_info(date_start, date_end, gender):
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
      WHERE (m.dates BETWEEN '{date_start}' AND '{date_end}')
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")
    dates_df = pd.read_sql_query(query, conn)
    dates_df.columns = cols

    return dates_df


def toss_info(toss_result, gender):
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
      WHERE m.toss_winner = '{toss_result}'
      AND m.gender = '{gender}';
    """
    conn = sqlite3.connect("cricket.db")
    toss_df = pd.read_sql_query(query, conn)
    toss_df.columns = cols

    return toss_df


def get_fielding_stats_other(format_type, gender):
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
        WHERE m.match_type = '{format_type}' AND
        (b.wickets_kind = 'run out' OR b.wickets_kind = 'caught' OR b.wickets_kind = 'stumped')
        AND m.gender = '{gender}'
    """
    conn = sqlite3.connect("cricket.db")
    field_df = pd.read_sql_query(query, conn)
    field_df.columns = cols

    return field_df









