import pandas as pd
def get_batting_stats(odi_batt, player, format):
  odi_bat = odi_batt[odi_batt["batter"] == player].copy()
  gender = odi_bat.iloc[0]["gender"]
  inngs  = odi_bat.groupby(["match_id", "innings_number"])["innings_number"].unique().count()
  odi_bat["bowler_extras"] = odi_bat.apply(lambda x: x["noballs_extras"] + x["wides_extras"], axis=1)
  total_runs = odi_bat["runs_batter"].sum()
  total_balls = odi_bat[odi_bat["wides_extras"] == 0]["ball_number"].count()
  strike_rate = round(total_runs / total_balls * 100,2)
  all_scores = list(odi_bat.groupby(["match_id", "innings_number"])["runs_batter"].sum())
  hundred = len([x for x in all_scores if x >= 100])
  fifty = len([x for x in all_scores if x >= 50])
  thirties = len([x for x in all_scores if x >= 30])
  zeros = len([x for x in all_scores if x == 0])
  innings_got_out = odi_batt[odi_batt["wickets_player_out"] == player].groupby(["match_id", "innings_number"])["innings_number"].unique().count().sum()
  average_bat = round(total_runs / innings_got_out,2)
  not_out = inngs - innings_got_out
  sixes = len(odi_bat[odi_bat["runs_batter"] == 6])
  fours = len(odi_bat[odi_bat["runs_batter"] == 4])
  doubles = len(odi_bat[odi_bat["runs_batter"] == 2])
  singles = len(odi_bat[odi_bat["runs_batter"] == 1])
  threes = len(odi_bat[odi_bat["runs_batter"] == 3])
  dot_balls = len(odi_bat[odi_bat["runs_batter"] == 0])
  best_bat = pd.DataFrame(odi_bat.groupby(["match_id", "innings_number"])["runs_batter"].sum()).sort_values(by=["runs_batter"], ascending=False).reset_index()
  best_final = best_bat.head(5)

  best_text = ""
  for i in range(len(best_final)):
    scor = best_final.iloc[i]["runs_batter"]
    mat_t = odi_bat[(odi_bat["match_id"] == best_final.iloc[i]["match_id"]) & (odi_bat["innings_number"] == best_final.iloc[i]["innings_number"])]
    ball_t = mat_t[mat_t["wides_extras"] == 0]["ball_number"].count()
    o_df = odi_bat[odi_bat["match_id"] == best_final.iloc[i]["match_id"]]
    o_dff = odi_batt[odi_batt["match_id"] == best_final.iloc[i]["match_id"]]
    team_o = o_df["team"].iloc[0]
    f = o_df["teams"].iloc[0]
    in_number = o_df['innings_number'].iloc[0]
    dates = o_df['dates'].iloc[0]
    g = f.replace(team_o, "")
    g = g.replace("'", "")
    g = g.replace(",", "")
    g = g.lstrip()
    g = g.rstrip()
    not_df = o_dff[o_dff["wickets_player_out"] == player]
    if len(not_df):
      nt_out = ""
    else:
      nt_out = "not out"
    venue_o = o_df["venue"].iloc[0]
    best_text += f" {i}. scored {scor} runs {nt_out} in {ball_t} balls against {g} in the innings number {in_number} at {venue_o} on {dates}."

  text = f"""In the {format}, {player} has played {inngs} innings, taking {total_balls} balls to score {total_runs} runs.
  Scored runs with a strike rate of {strike_rate} and average of {average_bat}. {player} scored {hundred} hundreds,
  {fifty} fifties, {thirties} thirties and {zeros} zeros. {player} remained not out in {not_out} matches and got out in
  {innings_got_out} matches. {player} hit {sixes} sixes, {fours} fours, {threes} threes, {doubles} doubles, {singles} singles and
  {dot_balls} dot balls. {player} best performances are as follows:- {best_text}"""

  return text

def get_bowling_stats(odi_ball, player, format):
  inngs  = odi_ball.groupby(["match_id", "innings_number"])["innings_number"].unique().count()
  odi_ball["bowler_extras"] = odi_ball.apply(lambda x: x["noballs_extras"] + x["wides_extras"], axis=1)
  total_bowler_runs = odi_ball["bowler_extras"].sum() + odi_ball["runs_batter"].sum()
  no_balls_total = odi_ball["noballs_extras"].sum()
  wides_total = odi_ball["wides_extras"].sum()

  runs_each_over_bat = list(odi_ball.groupby(["match_id", "innings_number", "over_number"])["runs_batter"].sum())
  runs_each_over_extra = list(odi_ball.groupby(["match_id", "innings_number", "over_number"])["bowler_extras"].sum())

  maiden = len([x+y for x, y in zip(runs_each_over_bat, runs_each_over_extra) if x+y == 0])
  fife = len([x+y for x, y in zip(runs_each_over_bat, runs_each_over_extra) if x+y <= 5])
  ten = len([x+y for x, y in zip(runs_each_over_bat, runs_each_over_extra) if x+y <= 10])
  ten_more = len([x+y for x, y in zip(runs_each_over_bat, runs_each_over_extra) if x+y > 10])

  wickets_taken = len(odi_ball[(~odi_ball["wickets_player_out"].isnull()) & (~odi_ball["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))])
  wickets_each_match = list(odi_ball[(~odi_ball["wickets_player_out"].isnull()) & (~odi_ball["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))].groupby(["match_id"])["wickets_kind"].count())
  wickets_each_innings = list(odi_ball[(~odi_ball["wickets_player_out"].isnull()) & (~odi_ball["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))].groupby(["match_id", "innings_number"])["wickets_kind"].count())

  one_innings = len([x for x in wickets_each_innings if x == 1])
  two_innings = len([x for x in wickets_each_innings if x == 2])
  fifer_innings = len([x for x in wickets_each_innings if x >= 5])

  one_match = len([x for x in wickets_each_match if x == 1])
  two_match = len([x for x in wickets_each_match if x == 2])
  fifer_match = len([x for x in wickets_each_match if x >= 5])

  total_overs = len(runs_each_over_bat)
  economy_rate = round(total_bowler_runs / total_overs, 2)
  
  all_wickets_innings = pd.DataFrame(odi_ball[(~odi_ball["wickets_player_out"].isnull()) & (~odi_ball["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))].groupby(["match_id"])["wickets_kind", "innings_number"].count()).reset_index()
  all_wickets_matches = pd.DataFrame(odi_ball[(~odi_ball["wickets_player_out"].isnull()) & (~odi_ball["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))].groupby(["match_id"])["wickets_kind"].count()).reset_index()
  
  best_matches_wickets = all_wickets_matches[all_wickets_matches["wickets_kind"] == all_wickets_matches["wickets_kind"].max()]
  if not len(best_matches_wickets):
    all_runs_matches = pd.DataFrame(odi_ball.groupby(["match_id"])["runs_batter"].sum()).reset_index()
    best_matches_wickets = all_runs_matches.sort_values(by=["runs_batter"]).head(5)
    best_matches_wickets["wickets_kind"] = 0
  else:
      best_matches_wickets = best_matches_wickets.head(5)
  dot_balls = len(odi_ball[(odi_ball["runs_batter"] == 0) & (odi_ball["bowler_extras"] == 0)])
  bowling_average = round(total_bowler_runs / wickets_taken,2)
  valid_balls = odi_ball[odi_ball["bowler_extras"] == 0]["ball_number"].count()
  valid_overs = round(valid_balls/6,1)
  strike_rate = round(valid_balls/wickets_taken,2)

  best_list = list(best_matches_wickets["match_id"])
  best_df = odi_ball[odi_ball["match_id"].isin(best_list)]
  best_df = best_df[best_df["bowler"] == player]
  best_runs_final = best_df["bowler_extras"] + best_df["runs_batter"]
  best_df.loc[:,"runs_given"] = best_runs_final
  runs_given_best = pd.DataFrame(best_df.groupby(["match_id"])["runs_given"].sum()).reset_index()
  best_final = best_matches_wickets.merge(runs_given_best, on=["match_id"])
  best_final = best_final.sort_values(["wickets_kind", "runs_given"], ascending=False)
  best_text = ""
  for i in range(len(best_final)):
    wick = best_final.iloc[i]["wickets_kind"]
    runs_g = best_final.iloc[i]["runs_given"]
    o_df = odi_ball[odi_ball["match_id"] == best_final.iloc[i]["match_id"]]
    o_df = o_df[o_df["bowler"] == player]
    valid_b = o_df[o_df["bowler_extras"] == 0]["ball_number"].count()
    valid_overs = round(valid_b/6,1)
    team_o = o_df["team"].iloc[0]
    in_number = o_df['innings_number'].iloc[0]

    dates = o_df['dates'].iloc[0]
    venue_o = o_df["venue"].iloc[0]
    best_text += f" {i}. {wick} wickets for {runs_g} runs in {valid_overs} overs against {team_o} in the innings number {in_number} at {venue_o} on {dates}."
  
  text = f"""In the {format}, {player} has bowled in {inngs} innings, bowled {valid_balls} balls i.e. {valid_overs} overs giving away {total_bowler_runs} runs.
  In the process bowled {maiden} maiden overs, {fife} overs with 5 runs or less, {ten} overs with 10 runs or less,
  {ten_more} overs with more than 10 runs. {player} bowled {dot_balls} dot balls. {player} got {wickets_taken} wickets in total. {player} got 1 wicket {one_match} times,
  got 2 wickets {two_match} times and got 5 wickets or more {fifer_match} times. {player}'s economy rate is {economy_rate}, bowling average is
  {bowling_average} and strike rate is {strike_rate}. In total {player} bowled {no_balls_total} noballs and {wides_total} wides.
  {player} best performances are as follows:- {best_text}"""

  return text

def get_fielding_text_player(field_stats):
  field_text = ""
  if len(field_stats):
    field_df = pd.DataFrame(field_stats)
    for idx, row in field_df.iterrows():
      field_text += f"In the {row['format']}, {row['player']} has done {row['stats'][0]} run outs and {row['stats'][1]} stumpings and took {row['stats'][2]} catches."

  return field_text
