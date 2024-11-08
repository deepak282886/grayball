import pandas as pd
from other_analysis import get_others_df, get_fielding_text_other, process_fielding
from other_db_calls import get_fielding_stats_other
from grayball_v0.team.team_analysis import (group_bat, group_bowl, get_bat_text, 
get_ball_text)
from grayball_v0.team.team_db_calls import recent_data_bat_team, recent_data_ball_team
from grayball_v0.query_handling.common_utils import slice_with_others


def process_others(list_other):
    gender = list_other["gender"]
    df, g_var = get_others_df(list_other)
    df["dates"] = pd.to_datetime(df["dates"])
    df = df.sort_values(by=["dates"])
    format_types = list(df["match_type"].unique())
    recent_text = ""
    all_text = ""
    field_stats_text = ""
    for format_type in format_types:
        sort_var = False
        df_bat = []
        df_ball = []
        u_df = df[df["match_type"] == format_type]
        u_df = slice_with_others(u_df, list_other)
        if "fielding" in list(list_other.keys()):
            field_df = get_fielding_stats_other(format_type, gender)
            field_df = process_fielding(field_df, g_var, list_other)
            field_text = get_fielding_text_other(field_df, format_type)
            field_stats_text += field_text
        if len(u_df):
            if "top_k" in list(list_other.keys()):
                sample = int(list_other["top_k"])
            else:
                sample = 5
            if "sort_criteria" in list(list_other.keys()):
                sort_criteria = list_other["sort_criteria"]
            else:
                sort_criteria = "all"
            if "sort_sub_criteria" in list(list_other.keys()):
                sub_criteria = list_other["sort_sub_criteria"]
            else:
                sub_criteria = "default"
            if "best_or_worst" in list(list_other.keys()):
                a_d = list_other["best_or_worst"]
                if a_d == "worst":
                    sort_var = True
            if sort_criteria == "bat":
                df_bat = group_bat(u_df)
            if sort_criteria == "ball":
                df_ball = group_bowl(u_df)
            if sort_criteria == "all":
                df_bat = group_bat(u_df)
                df_ball = group_bowl(u_df)
            if len(df_bat):
                if sub_criteria == "default":
                    df_bat = df_bat.sort_values(by=["runs_scored"], ascending=sort_var)
                else:
                    df_bat = df_bat.sort_values(by=[sub_criteria], ascending=sort_var)
                df_bat = df_bat.head(sample)
                text_bat = get_bat_text(df_bat)
                all_text += text_bat
                if "recent_number" in list(list_other.keys()):
                    text_5_bat = recent_data_bat_team(format_type,u_df,list_other["recent_number"])
                    recent_text += text_5_bat
            if len(df_ball):
                if sub_criteria == "default":
                    df_ball = df_ball.sort_values(by=["wickets_taken"], ascending=sort_var)
                else:
                    df_ball = df_ball.sort_values(by=[sub_criteria], ascending=sort_var)
                df_ball = df_ball.head(sample)
                text_ball = get_ball_text(df_ball)
                all_text += text_ball
                if "recent_number" in list(list_other.keys()):
                    text_5_ball = recent_data_ball_team(format_type,u_df,list_other["recent_number"])
                    recent_text += text_5_ball

    return recent_text, all_text, field_stats_text
