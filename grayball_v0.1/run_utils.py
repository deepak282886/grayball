from query_handing.processing_utils import fill_result
from query_handing.collating_utils import process_results
from player.process_player import (process_player_recent_bat,process_player_recent_ball,
process_player_recent_field, process_player_bat, process_player_ball, 
process_player_field)
from team.process_team import (process_team_recent_bat,process_team_recent_ball,
process_team_recent_field, process_team_bat, process_team_ball, 
process_team_field)
import wikipedia
from other.process_other import process_others

def get_final_stats(result):
  try:
    result = fill_result(result)
    list_other = process_results(result)
    print(list_other)
    final_text = ""
    if list_other['player'] != "all":
      if list_other['recent_number'] != "all":
        if "bat" in list_other['department']:
          recent_text_bat = process_player_recent_bat(list_other)
          final_text += recent_text_bat
        if "ball" in list_other['department']:
          recent_text_ball = process_player_recent_ball(list_other)
          final_text += recent_text_ball
        if "field" in list_other['department']:
          recent_text_field = process_player_recent_field(list_other)
          final_text += recent_text_field

        if "all" in list_other['department']:
          recent_text_bat = process_player_recent_bat(list_other)
          recent_text_ball = process_player_recent_ball(list_other)
          recent_text_field = process_player_recent_field(list_other)
          final_text += recent_text_bat
          final_text += recent_text_ball
          final_text += recent_text_field
      elif list_other['history'] == "yes":
        if "bat" in list_other['department']:
          text_bat = process_player_bat(list_other)
          final_text += text_bat
        if "ball" in list_other['department']:
          text_ball = process_player_ball(list_other)
          final_text += text_ball
        if "field" in list_other['department']:
          text_field = process_player_field(list_other)
          final_text += text_field

        if "all" in list_other['department']:
          text_bat = process_player_bat(list_other)
          text_ball = process_player_ball(list_other)
          text_field = process_player_field(list_other)
          final_text += text_bat
          final_text += text_ball
          final_text += text_field
        
    elif list_other['team'] != "all":
      if list_other['recent_number'] != "all":
        if "bat" in list_other['department']:
          recent_text_bat = process_team_recent_bat(list_other)
          final_text += recent_text_bat
        if "ball" in list_other['department']:
          recent_text_ball = process_team_recent_ball(list_other)
          final_text += recent_text_ball
        if "field" in list_other['department']:
          recent_text_field = process_team_recent_field(list_other)
          final_text += recent_text_field

        if "all" in list_other['department']:
          recent_text_bat = process_team_recent_bat(list_other)
          recent_text_ball = process_team_recent_ball(list_other)
          recent_text_field = process_team_recent_field(list_other)
          final_text += recent_text_bat
          final_text += recent_text_ball
          final_text += recent_text_field
      elif list_other['history'] == "yes":
        if "bat" in list_other['department']:
          text_bat = process_team_bat(list_other)
          final_text += text_bat
        if "ball" in list_other['department']:
          text_ball = process_team_ball(list_other)
          final_text += text_ball
        if "field" in list_other['department']:
          text_field = process_team_field(list_other)
          final_text += text_field

        if "all" in list_other['department']:
          text_bat = process_team_bat(list_other)
          text_ball = process_team_ball(list_other)
          text_field = process_team_field(list_other)
          final_text += text_bat
          final_text += text_ball
          final_text += text_field
    elif 'tournament' in list(list_other.keys()):
      try:
        search_page = wikipedia.search(list_other["tournament"], results=1, suggestion=True)[0][0]
        page = wikipedia.page(search_page).content.encode('utf-8').strip()
        return page
      except:
        page = "sorry the stats are not available right now"
        return page
    elif 'historic_event' in list(list_other.keys()):
      try:
        search_page = wikipedia.search(list_other["historic_event"], results=1, suggestion=True)[0][0]
        page = wikipedia.page(search_page).content.encode('utf-8').strip()
        return page
      except:
        page = "sorry the stats are not available right now"
        return page
    else:
      recent_text, all_text, field_text = process_others(list_other)
    return recent_text, all_text, field_text
  except:
    page = "Please enter correct names"
    return page