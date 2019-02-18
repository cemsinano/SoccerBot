from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionLeaderName(Action):
	def name(self):
		return 'action_leader_name'

	def run(self, dispatcher, tracker, domain):
        import requests as req

        resp = req.get("https://projects.fivethirtyeight.com/soccer-predictions/data.json")

		lig = tracker.get_slot('league_name')
        # need to find an elegant solution to make a proper league name matching...
        if(lig == "Turkish Super League"):
            lig = "super-lig"
        else if(lig == "Bundesliga" | lig == 'bundesliga'):
            lig = "bundesliga"
        else if(lig == 'La Liga'):
            lig = 'la-ligas'

        leagues = resp["leagues"]
        league = next(item for item in leagues if item["slug"] == lig)
        league_id = league['id']
        forecasts = resp["forecasts"]
        standings = next(item for item in forecasts if item["league_id"] == league_id)
        team_code = standings['teams'][0]['code']
        teams = resp['teams']
        team = next(item for item in teams if item["code"] == team_code)
        response = """The current leader of {} is {}.""".format(lig, team['name'])

		dispatcher.utter_message(response)
		return [SlotSet('league_name',lig)]
