import pandas as pd
import re


def group_bat(odi_bat):
    innings_df = []
    indi_df = []
    for i, j in odi_bat.groupby(["batter", "match_type"]):
        innings_played = j.groupby(["match_id","innings_number"])["innings_number"].unique().count()
        total_runs = j["runs_batter"].sum()
        total_balls = j[j["wides_extras"] == 0]["ball_number"].count()
        strike_rate = round(total_runs / total_balls * 100,2)
        all_scores = list(j.groupby(["match_id", "innings_number"])["runs_batter"].sum())
        hundred = len([x for x in all_scores if x >= 100])
        fifty = len([x for x in all_scores if x >= 50])
        thirties = len([x for x in all_scores if x >= 30])
        zeros = len([x for x in all_scores if x == 0])
        innings_got_out = j[j["wickets_player_out"] == i[0]].groupby(["match_id", "innings_number"])["innings_number"].unique().count().sum()
        not_out = innings_played - innings_got_out
        sixes = len(j[j["runs_batter"] == 6])
        fours = len(j[j["runs_batter"] == 4])
        doubles = len(j[j["runs_batter"] == 2])
        singles = len(j[j["runs_batter"] == 1])
        threes = len(j[j["runs_batter"] == 3])
        dot_balls = len(j[j["runs_batter"] == 0])
        average_bat = round(total_runs / innings_got_out,2)
        best_bat = pd.DataFrame(j.groupby(["match_id", "innings_number"])["runs_batter"].sum()).sort_values(by=["runs_batter"], ascending=False).reset_index()
        best_final = best_bat.head(1)
        scor = best_final.iloc[0]["runs_batter"]
        mat_t = j[(j["match_id"] == best_final.iloc[0]["match_id"]) & (j["innings_number"] == best_final.iloc[0]["innings_number"])]
        ball_t = mat_t[mat_t["wides_extras"] == 0]["ball_number"].count()
        o_df = j[j["match_id"] == best_final.iloc[0]["match_id"]]
        o_dff = odi_bat[odi_bat["match_id"] == best_final.iloc[0]["match_id"]]
        team_o = o_df["team"].iloc[0]
        f = o_df["teams"].iloc[0]
        dates = o_df['dates'].iloc[0]
        g = f.replace(team_o, "")
        g = g.replace("'", "")
        g = g.replace(",", "")
        g = g.lstrip()
        g = g.rstrip()
        not_df = o_dff[o_dff["wickets_player_out"] == i[0]]
        if len(not_df):
            nt_out = ""
        else:
            nt_out = "not out"
        venue_o = o_df["venue"].iloc[0]

        innings_df.append({"innings": innings_played, "batter": i[0], "match_type": i[1],
                          "runs_scored": total_runs, "balls_faced": total_balls, "strike_rate": strike_rate,
                          "hundred":hundred, "fifty":fifty, "thirties":thirties, "zeros":zeros, "average": average_bat,
                          "not_out": not_out, "sixes": sixes, "fours":fours, "doubles": doubles, "singles": singles,
                          "threes": threes, "dot_balls": dot_balls, "highest_score": scor, "balls_taken":ball_t,
                          "not_out": nt_out, "opponent":g, "venue": venue_o, "date": dates})
    if len(innings_df):
        innings_df = pd.DataFrame(innings_df)

    return innings_df


def get_bat_text(bat_df):
    all_text = ""
    for idx, row in bat_df.iterrows():
        text = f"""In the {row["match_type"]}, {row["batter"]} has played {row["innings"]} innings, taking {row["balls_faced"]}
                  balls to score {row["runs_scored"]} runs.
                  Scored runs with a strike rate of {row["strike_rate"]} and average of {row["average"]}. {row["batter"]} scored {row["hundred"]} hundreds,
                  {row["fifty"]} fifties, {row["thirties"]} thirties and {row["zeros"]} zeros. {row["batter"]} remained
                  not out in {row["not_out"]} matches and hit {row["sixes"]} sixes, {row["fours"]} fours, {row["threes"]} threes,
                  {row["doubles"]} doubles, {row["singles"]} singles and
                  {row["dot_balls"]} dot balls. {row["batter"]}'s highest
                  score was {row["highest_score"]} runs in {row["balls_taken"]} balls against {row["opponent"]} at
                  {row["venue"]} on {row["date"]}"""
        all_text += text
    all_text = re.sub(' +', ' ', all_text)
    return all_text


def group_bowl(odi_ball):
    innings_df = []
    indi_df = []
    odi_ball["bowler_extras"] = odi_ball.apply(lambda x: x["noballs_extras"] + x["wides_extras"], axis=1)
    for i, j in odi_ball.groupby(["bowler", "match_type"]):
        innings_bowled = j.groupby(["match_id","innings_number"])["innings_number"].unique().count()
        j["bowler_extras"] = j.apply(lambda x: x["noballs_extras"] + x["wides_extras"], axis=1)
        total_bowler_runs = j["bowler_extras"].sum() + j["runs_batter"].sum()
        no_balls_total = j["noballs_extras"].sum()
        wides_total = j["wides_extras"].sum()
        runs_each_over_bat = list(j.groupby(["match_id", "innings_number", "over_number"])["runs_batter"].sum())
        runs_each_over_extra = list(j.groupby(["match_id", "innings_number", "over_number"])["bowler_extras"].sum())

        maiden = len([x+y for x, y in zip(runs_each_over_bat, runs_each_over_extra) if x+y == 0])
        fife = len([x+y for x, y in zip(runs_each_over_bat, runs_each_over_extra) if x+y <= 5])
        ten = len([x+y for x, y in zip(runs_each_over_bat, runs_each_over_extra) if x+y <= 10])
        ten_more = len([x+y for x, y in zip(runs_each_over_bat, runs_each_over_extra) if x+y > 10])

        wickets_taken = len(j[(~j["wickets_player_out"].isnull()) & (~j["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))])
        wickets_each_match = list(j[(~j["wickets_player_out"].isnull()) & (~j["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))].groupby(["match_id"])["wickets_kind"].count())
        wickets_each_innings = list(j[(~j["wickets_player_out"].isnull()) & (~j["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))].groupby(["match_id", "innings_number"])["wickets_kind"].count())

        one_innings = len([x for x in wickets_each_innings if x == 1])
        two_innings = len([x for x in wickets_each_innings if x == 2])
        fifer_innings = len([x for x in wickets_each_innings if x >= 5])

        one_match = len([x for x in wickets_each_match if x == 1])
        two_match = len([x for x in wickets_each_match if x == 2])
        fifer_match = len([x for x in wickets_each_match if x >= 5])

        total_overs = len(runs_each_over_bat)
        economy_rate = round(total_bowler_runs / total_overs, 2)

        all_wickets_innings = pd.DataFrame(j[(~j["wickets_player_out"].isnull()) & (~j["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))].groupby(["match_id"])["wickets_kind", "innings_number"].count()).reset_index()
        all_wickets_matches = pd.DataFrame(j[(~j["wickets_player_out"].isnull()) & (~j["wickets_kind"].isin(['run out','retired hurt','obstructing the field','timed out']))].groupby(["match_id"])["wickets_kind"].count()).reset_index()

        dot_balls = len(j[(j["runs_batter"] == 0) & (j["bowler_extras"] == 0)])
        bowling_average = round(total_bowler_runs / wickets_taken,2)
        valid_balls = j[j["bowler_extras"] == 0]["ball_number"].count()
        valid_overs = round(valid_balls/6,1)
        strike_rate = round(valid_balls/wickets_taken,2)

        best_matches_wickets = all_wickets_matches[all_wickets_matches["wickets_kind"] == all_wickets_matches["wickets_kind"].max()]
        if not len(best_matches_wickets):
            all_runs_matches = pd.DataFrame(j.groupby(["match_id"])["runs_batter"].sum()).reset_index()
            best_matches_wickets = all_runs_matches.sort_values(by=["runs_batter"]).head(1)
            best_matches_wickets["wickets_kind"] = 0

        else:
            best_matches_wickets = best_matches_wickets.head(1)

        best_list = list(best_matches_wickets["match_id"])
        best_df = odi_ball[odi_ball["match_id"].isin(best_list)]
        best_df = best_df[best_df["bowler"] == i[0]]
        best_runs_final = best_df["bowler_extras"] + best_df["runs_batter"]
        best_df.loc[:,"runs_given"] = best_runs_final
        runs_given_best = pd.DataFrame(best_df.groupby(["match_id"])["runs_given"].sum()).reset_index()
        best_final = best_matches_wickets.merge(runs_given_best, on=["match_id"])
        best_final = best_final.sort_values(["wickets_kind", "runs_given"], ascending=False)
        wick = best_final.iloc[0]["wickets_kind"]
        runs_g = best_final.iloc[0]["runs_given"]
        o_df = odi_ball[odi_ball["match_id"] == best_final.iloc[0]["match_id"]]
        o_df = o_df[o_df["bowler"] == i[0]]
        team_o = o_df["team"].iloc[0]
        in_number = o_df['innings_number'].iloc[0]
        valid_b = o_df[o_df["bowler_extras"] == 0]["ball_number"].count()
        valid_o = round(valid_b/6,1)
        dates = o_df['dates'].iloc[0]
        venue_o = o_df["venue"].iloc[0]

        innings_df.append({"innings": innings_bowled, "bowler": i[0], "match_type": i[1], "balls_bowled": valid_balls, "overs_bowled" : valid_overs,
                          "runs_given": total_bowler_runs, "wickets_taken": wickets_taken, "maiden_overs": maiden, "overs_with_5_or_less_runs": fife,
                          "overs_with_10_or_less_runs": ten, "overs_with_10_or_more_runs": ten_more, "dot_balls" : dot_balls, "times_taken_one_wicket": one_match,
                          "times_taken_two_wicket": two_match, "times_taken_five_wicket":fifer_match, "economy_rate": economy_rate, "bowling_average": bowling_average,
                          "strike_rate": strike_rate, "no_balls_total": no_balls_total, "wides_total": wides_total,
                          "highest_wickets": wick, "runs_given_g": runs_g, "overs_bowled_g": valid_o, "opponent":team_o,
                          "venue": venue_o, "date": dates})
    if len(innings_df):
        innings_df = pd.DataFrame(innings_df)

    return innings_df


def get_ball_text(ball_df):
    all_text = ""
    for idx, row in ball_df.iterrows():

        text = f"""In the {row["match_type"]}, {row["bowler"]} has bowled in {row["innings"]} innings, bowled {row["balls_bowled"]} balls i.e.
        {row["overs_bowled"]} overs giving away {row["runs_given"]} runs.
        In the process bowled {row["maiden_overs"]} maiden overs, {row["overs_with_5_or_less_runs"]} overs with 5 runs or less,
        {row["overs_with_10_or_less_runs"]} overs with 10 runs or less,
        {row["overs_with_10_or_more_runs"]} overs with more than 10 runs. {row["bowler"]} bowled {row["dot_balls"]} dot balls
        and got {row["wickets_taken"]} wickets in total. {row["bowler"]} got 1 wicket {row["times_taken_one_wicket"]} times,
        got 2 wickets {row["times_taken_two_wicket"]} times and got 5 wickets or more {row["times_taken_five_wicket"]} times.
        {row["bowler"]}'s economy rate is {row["economy_rate"]}, bowling average is
        {row["bowling_average"]} and strike rate is {row["strike_rate"]}. In total {row["bowler"]} bowled {row["no_balls_total"]}
        noballs and {row["wides_total"]} wides. {row["bowler"]} took
        {row["highest_wickets"]} wickets for {row["runs_given_g"]} runs in {row["overs_bowled_g"]} overs
        against {row["opponent"]} at {row["venue"]} on {row["date"]}."""

        all_text += text
    all_text = re.sub(' +', ' ', all_text)
    return all_text


def get_fielding_text_team(field_df, team, format_type):
    field_text = ""
    if len(field_df):
        field_list = ["run out", "stumped", "caught"]

        for para in field_list:
            run_df1 = pd.DataFrame(field_df[(field_df["wickets_kind"] == f"{para}") & (field_df["team"] != f"{team}")].groupby(["fielder1_wicket"])["wickets_kind"].count())
            run_df2 = pd.DataFrame(field_df[(field_df["wickets_kind"] == f"{para}") & (field_df["team"] != f"{team}")].groupby(["fielder2_wicket"])["wickets_kind"].count())
            run_df = pd.concat([run_df1, run_df2]).reset_index()
            run_df = pd.DataFrame(run_df.groupby(["index"])["wickets_kind"].sum()).reset_index()
            run_df = run_df.sort_values(by=["wickets_kind"], ascending=False).head(15)
            field_text += f"In the {format_type} for {team}"
            for idx, row in run_df.iterrows():
                if para == "run out":
                    value = "run outs"
                if para == "stumped":
                    value = "stumps"
                if para == "caught":
                    value = "catches"
                field_text += f"{row['index']} has {row['wickets_kind']} {value}"

    return field_text
