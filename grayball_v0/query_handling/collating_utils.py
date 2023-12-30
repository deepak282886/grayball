import wikipedia 
import pandas as pd


def get_other_keys(result):
    list_other = {}
    for key in list(result.keys()):
        if key == 'format':
            if result['format'] != 'all':
                formats = [result['format']]
                list_other["format"] = formats
        if key == 'historic_event':
            if result['historic_event'] == 'yes':
                historic_event = result['historic_event']
                list_other["historic_event"] = historic_event

        if key == 'department':
            department = result['department']
            list_other["department"] = department

        if key == 'innings':
            if result['innings'] != 'all':
                innings = result['innings']
                list_other["innings"] = int(innings)
        if key == 'history':
            if result['history'] == 'all':
                list_other["history"] = "yes"
            else:
                history = result['history']
                list_other["history"] = history

        if key == 'overs_start':
            if result['overs_start'] != 'all':
                overs_start = result['overs_start']
                list_other["overs_start"] = int(overs_start)
        if key == 'overs_end':
            if result['overs_end'] != 'all':
                overs_end = result['overs_end']
                list_other["overs_end"] = int(overs_end)
        if key == 'recent_type':
            if result['recent_type'] != 'no':
                if result['recent_number'] != 'all':
                    recent_number = result['recent_number']
                    list_other["recent_number"] = int(recent_number)
        if key == 'tournament':
            if result['tournament'] != 'all':
                tournament = result['tournament']
                list_other["tournament"] = tournament
        if key == 'venue':
            if result['venue'] != 'all':
                venue = result['venue']
                venue_term = f"{venue} cricket stadium"
                venue_f = get_db_info(venue_term)
                list_other["venue"] = venue_f
        if key == 'opposing_venue':
            if result['opposing_venue'] != 'all':
                opposing_venue = result['opposing_venue']
                opp_venue_term = f"{opposing_venue} cricket stadium"
                opp_venue_f = get_db_info(opp_venue_term)
                list_other["opposing_venue"] = opp_venue_f
        if key == 'batsman_number':
            if result['batter_number'] != 'all':
                batsman_position_number = result['batter_number']
                list_other['batter_number'] = batsman_position_number

        if key == 'bowler_number':
            if result['bowler_number'] != 'all':
                bowler_position_number = result['bowler_number']
                list_other['bowler_number'] = bowler_position_number

        if key == 'fielding':
            if result['fielding'] == "True":
                fielding = result['fielding']
                list_other["fielding"] = fielding
        if key == 'city':
            if result['city'] != 'all':
                city = result['city']
                list_other["city"] = city
        if key == 'match_result':
            if result['match_result'] != 'all':
                match_result = result['match_result']
                list_other["match_result"] = match_result
        if key == 'margin_runs_start':
            if result['margin_runs_start'] != 'all':
                margin_runs_start = result['margin_runs_start']
                list_other["margin_runs_start"] = int(margin_runs_start)
        if key == 'margin_runs_end':
            if result['margin_runs_end'] != 'all':
                margin_runs_end = result['margin_runs_end']
                list_other["margin_runs_end"] = int(margin_runs_end)
        if key == 'margin_wickets_start':
            if result['margin_wickets_start'] != 'all':
                margin_wickets_start = result['margin_wickets_start']
                list_other["margin_wickets_start"] = int(margin_wickets_start)
        if key == 'margin_wickets_end':
            if result['margin_wickets_end'] != 'all':
                margin_wickets_end = result['margin_wickets_end']
                list_other["margin_wickets_end"] = int(margin_wickets_end)
        if key == 'date_start':
            if result['date_start'] != 'all':
                date_start = pd.to_datetime(result['date_start'], format='%Y-%m-%d')
                list_other["date_start"] = date_start
        if key == 'date_end':
            if result['date_end'] != 'all':
                date_end = pd.to_datetime(result['date_end'], format='%Y-%m-%d')
                list_other["date_end"] = date_end
        if key == 'toss_result':
            if result['toss_result'] != 'all':
                toss_result = result['toss_result']
                list_other["toss_result"] = toss_result
        if key == 'toss_decision':
            if result['toss_decision'] != 'all':
                toss_decision = result['toss_decision']
                list_other["toss_decision"] = toss_decision
        if key == 'top_k':
            if result['top_k'] != 'all':
                top_k = result['top_k']
                b_or_w = result['best_or_worst']
                sort_criteria = result['sort_criteria']
                sort_sub_criteria = result["sort_sub_criteria"]
                list_other["top_k"] = int(top_k)
                list_other["best_or_worst"] = b_or_w
                list_other["sort_criteria"] = sort_criteria
                list_other['sort_sub_criteria'] = sort_sub_criteria

    return list_other


def process_results(result):
    list_other = get_other_keys(result)
    if 'players_involved' in list(result.keys()):
        if result["players_involved"] == "single":
            plyr = result["player_name"]
            plyr_term = f"{plyr} cricketer"
            plyr_f = get_db_info(plyr_term)
            list_other["player"] = plyr_f
        if result["players_involved"] == "head_to_head":
            plyr = result["player_name"]
            plyr_term = f"{plyr} cricketer"
            plyr_f = get_db_info(plyr_term)
            list_other["player"] = plyr_f

            plyr = result["opponent_name"]
            plyr_term = f"{plyr} cricketer"
            plyr_f = get_db_info(plyr_term)
            list_other["opponent_name"] = plyr_f
        if result["players_involved"] == "multiple":
            list_other["player"] = "all"
    else:
        list_other["player"] = "all"
    if 'teams_involved' in list(result.keys()):
        if result["teams_involved"] == "single":
            team = result["team_name"]
            team_term = f"team {team} cricket"
            team_f = get_db_info(team_term)
            list_other["team"] = team_f

        if result["teams_involved"] == "head_to_head":
            team = result["team_name"]
            team_term = f"team {team} cricket"
            team_f = get_db_info(team_term)
            list_other["team"] = team_f

            team = result["opponent_team"]
            team_term = f"team {team} cricket"
            team_f = get_db_info(team_term)
            list_other["opponent_team"] = team_f
        if result["teams_involved"] == "multiple":
            list_other["team"] = "all"
    else:
        list_other["team"] = "all"
    return list_other


def get_db_info(search_term):
    if "cricketer" in search_term:
        names_df = pd.read_csv("final_name_df.csv")
        name = wikipedia.search(search_term, results=1, suggestion=True)[0][0]
        name = names_df[names_df["name"].str.lower() == name.lower()].iloc[0]["players"]
    if "stadium" in search_term:
        venue_df = pd.read_csv("venue_wiki.csv")
        name = wikipedia.search(search_term, results=1, suggestion=True)[0][0]
        name = venue_df[venue_df["wiki_names"].str.lower() == name.lower()].iloc[0]["venue"]
    if "team" in search_term:
        name = wikipedia.search(search_term, results=1, suggestion=True)[0][0]
        name = name.split("national")[0].rstrip().lstrip()
    return name
