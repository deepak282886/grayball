from other_db_calls import (ground_info,
tournament_info,format_info,innings_info,
overs_info, city_info, margin_runs_info, 
margin_wickets_info, dates_info, toss_info)
import pandas as pd

def get_others_df(list_other):
  gender = list_other["gender"]
  g_var = ""
  if "venue" in list(list_other.keys()):
    df = ground_info(list_other["venue"], gender)
    g_var = "venue"
  elif "tournament" in list(list_other.keys()):
    df = tournament_info(list_other["tournament"], gender)
    g_var = "tournament"
  elif "format" in list(list_other.keys()):
    df = format_info(list_other["format"], gender)
    g_var = "format"

  elif "innings" in list(list_other.keys()):
    df = innings_info(list_other["innings"], gender)
    g_var = "innings"

  elif "overs_start" in list(list_other.keys()):
    df = overs_info(list_other["overs_start"],list_other["overs_end"], gender)
    g_var = "overs_start"

  elif "city" in list(list_other.keys()):
    df = city_info(list_other["city"], gender)
    g_var = "city"

  elif "margin_runs_start" in list(list_other.keys()):
    df = margin_runs_info(list_other["margin_runs_start"], list_other["margin_runs_end"], gender)
    g_var = "margin_runs_start"

  elif "margin_wickets_start" in list(list_other.keys()):
    df = margin_wickets_info(list_other["margin_wickets_start"], list_other["margin_wickets_end"], gender)
    g_var = "margin_wickets_start"

  elif "date_start" in list(list_other.keys()):
    df = dates_info(list_other["date_start"], list_other["date_end"], gender)
    g_var = "date_start"

  elif "toss_result" in list(list_other.keys()):
    df = toss_info(list_other["toss_result"], gender)
    g_var = "toss_result"

  return df, g_var

def process_fielding(df, g_var, list_other):
  if g_var == "venue":
    df = df[df["venue"] == list_other["venue"]]
  elif g_var == "tournament":
    df = df[df["tournament"] == list_other["tournament"]]
  elif g_var == "innings":
    df = df[df["innings_number"] == list_other["innings"]]
  elif g_var == "overs_start":
    df = df[df["over_number"] >= list_other["overs_start"]]
    df = df[df["over_number"] >= list_other["overs_end"]]

  elif g_var == "city":
    df = df[df["city"] == list_other["city"]]
  elif g_var == "margin_runs_start":
    df = df[df["margin_runs"] >= list_other["margin_runs_start"]]
    df = df[df["margin_runs"] <= list_other["margin_runs_end"]]
  elif g_var == "margin_wickets_start":
    df = df[df["margin_wickets"] >= list_other["margin_wickets_start"]]
    df = df[df["margin_wickets"] <= list_other["margin_wickets_end"]]

  elif g_var == "date_start":
    df = df[df["dates"] >= list_other["date_start"]]
    df = df[df["dates"] <= list_other["date_end"]]
  elif g_var == "toss_result":
    df = df[df["toss_result"] == list_other["toss_result"]]
  return df



def get_fielding_text_other(field_df, format):
  field_text = ""
  if len(field_df):
    field_list = ["run out", "stumped", "caught"]

    for para in field_list:
      run_df1 = pd.DataFrame(field_df[(field_df["wickets_kind"] == f"{para}") ].groupby(["fielder1_wicket"])["wickets_kind"].count())
      run_df2 = pd.DataFrame(field_df[(field_df["wickets_kind"] == f"{para}") ].groupby(["fielder2_wicket"])["wickets_kind"].count())
      run_df = pd.concat([run_df1, run_df2]).reset_index()
      run_df = pd.DataFrame(run_df.groupby(["index"])["wickets_kind"].sum()).reset_index()
      run_df = run_df.sort_values(by=["wickets_kind"], ascending=False).head(15)
      field_text += f"In the {format}"
      for idx, row in run_df.iterrows():
        if para == "run out":
          value = "run outs"
        if para == "stumped":
          value = "stumps"
        if para == "caught":
          value = "catches"
        field_text += f" {row['index']} has {row['wickets_kind']} {value}"

  return field_text



