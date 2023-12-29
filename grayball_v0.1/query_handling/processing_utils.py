def fill_result(model_output):
  output_json = model_output[0]["generated_text"].split("[/INST]")[1].replace("\\", "")
  output_json = output_json.replace("empty", "")
  output_json = output_json.replace("none", "all")
  output_json = output_json.replace("\n", "")
  output_json = output_json.replace('}', '"}')
  result = eval(output_json)

  if "gender" in list(result.keys()):
    if result["gender"] == "default":
      result["gender"] = "male"
    else:
      result["gender"] = result["gender"]
  else:
    result["gender"] = "male"
  
  if "department" in list(result.keys()):
    result["department"] = result["department"]
  else:
    result["department"] = "all"
  
  if "historic_event" in list(result.keys()):
    result["historic_event"] = result["historic_event"]
  else:
    result["historic_event"] = "no"
  
  if "history" in list(result.keys()):
    result["history"] = result["history"]
  else:
    result["history"] = "yes"

  if "players_involved" in list(result.keys()):
    result["players_involved"] = result["players_involved"]
  else:
    result["players_involved"] = "multiple"

  if "player_name" in list(result.keys()):
    result["player_name"] = result["player_name"]
    result["players_involved"] = "single"
  else:
    result["player_name"] = "all"

  if "opponent_player" in list(result.keys()):
    result["opponent_player"] = result["opponent_player"]
    result["players_involved"] = "head_to_head"
  else:
    result["opponent_player"] = "all"

  if "teams_involved" in list(result.keys()):
    result["teams_involved"] = result["teams_involved"]
  else:
    result["teams_involved"] = "multiple"

  if "team_name" in list(result.keys()):
    result["team_name"] = result["team_name"]
    result["teams_involved"] = "single"
  else:
    result["team_name"] = "all"

  if "opposing_team" in list(result.keys()):
    result["opposing_team"] = result["opposing_team"]
    result["teams_involved"] = "head_to_head"
  else:
    result["opposing_team"] = "all"

  if "format" in list(result.keys()):
    result["format"] = result["format"]
  else:
    result["format"] = "all"

  if "innings" in list(result.keys()):
    result["innings"] = result["innings"]
  else:
    result["innings"] = "all"

  if "overs_start" in list(result.keys()):
    result["overs_start"] = result["overs_start"]
  else:
    result["overs_start"] = "all"

  if "overs_end" in list(result.keys()):
    result["overs_end"] = result["overs_end"]
  else:
    result["overs_end"] = "all"

  if "recent_type" in list(result.keys()):
    result["recent_type"] = result["recent_type"]
  else:
    result["recent_type"] = "all"

  if "recent_number" in list(result.keys()):
    result["recent_number"] = result["recent_number"]
  else:
    result["recent_number"] = "all"

  if "tournament" in list(result.keys()):
    result["tournament"] = result["tournament"]
  else:
    result["tournament"] = "all"

  if "venue" in list(result.keys()):
    result["venue"] = result["venue"]
  else:
    result["venue"] = "all"

  if "opposing_venue" in list(result.keys()):
    result["opposing_venue"] = result["opposing_venue"]
  else:
    result["opposing_venue"] = "all"

  if "fielding" in list(result.keys()):
    if result["fielding"] == "all":

      result["fielding"] = result["fielding"]
    else:
        result["fielding"] = "no"
  else:
    result["fielding"] = "no"

  if "batter_number" in list(result.keys()):
    result["batter_number"] = result["batter_number"]
  else:
    result["batter_number"] = "all"

  if "bowler_number" in list(result.keys()):
    result["bowler_number"] = result["bowler_number"]
  else:
    result["bowler_number"] = "all"

  if "city" in list(result.keys()):
    result["city"] = result["city"]
  else:
    result["city"] = "all"

  if "match_result" in list(result.keys()):
    result["match_result"] = result["match_result"]
  else:
    result["match_result"] = "all"

  if "margin_runs_start" in list(result.keys()):
    result["margin_runs_start"] = result["margin_runs_start"]
  else:
    result["margin_runs_start"] = "all"

  if "margin_runs_end" in list(result.keys()):
    result["margin_runs_end"] = result["margin_runs_end"]
  else:
    result["margin_runs_end"] = "all"

  if "margin_wickets_start" in list(result.keys()):
    result["margin_wickets_start"] = result["margin_wickets_start"]
  else:
    result["margin_wickets_start"] = "all"

  if "margin_wickets_end" in list(result.keys()):
    result["margin_wickets_end"] = result["margin_wickets_end"]
  else:
    result["margin_wickets_end"] = "all"

  if "date_start" in list(result.keys()):
    result["date_start"] = result["date_start"]
  else:
    result["date_start"] = "all"

  if "date_end" in list(result.keys()):
    result["date_end"] = result["date_end"]
  else:
    result["date_end"] = "all"

  if "toss_result" in list(result.keys()):
    result["toss_result"] = result["toss_result"]
  else:
    result["toss_result"] = "all"

  if "toss_decision" in list(result.keys()):
    result["toss_decision"] = result["toss_decision"]
  else:
    result["toss_decision"] = "all"

  if "top_k" in list(result.keys()):
    result["top_k"] = result["top_k"]
  else:
    result["top_k"] = "all"

  if "best_or_worst" in list(result.keys()):
    result["best_or_worst"] = result["best_or_worst"]
  else:
    result["best_or_worst"] = "all"

  if "sort_criteria" in list(result.keys()):
    result["sort_criteria"] = result["sort_criteria"]
  else:
    result["sort_criteria"] = "all"

  if "sort_sub_criteria" in list(result.keys()):
    result["sort_sub_criteria"] = result["sort_sub_criteria"]
  else:
    result["sort_sub_criteria"] = "all"

  return result