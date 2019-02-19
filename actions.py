from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionLeader(Action):
    def name(self):
        return 'action_leader'

    def run(self, dispatcher, tracker, domain):

        import requests as req
        resp = req.get("https://projects.fivethirtyeight.com/soccer-predictions/data.json")
        resp = resp.json()
        lig = tracker.get_slot('league_name')
        #need to find an elegant solution to make a proper league name matching...
        if(lig == "turkish super league"):
            lig = "super-lig"
        if(lig == 'bundesliga'):
             lig = "bundesliga"
        if(lig == 'la liga'):
            lig = 'la-liga'

        leagues = resp["leagues"]
        league = next(item for item in leagues if item["slug"] == lig)
        league_id = league['id']
        forecasts = resp["forecasts"]
        standings = next(item for item in forecasts if item["league_id"] == league_id)
        team_code = standings['teams'][0]['code']
        teams = resp['teams']
        team = next(item for item in teams if item["code"] == team_code)
        response = """The current leader of {} is {}.""".format(lig, team['name'])
        #response = """The current leader of {} is Basaksehir.""".format(lig)
        dispatcher.utter_message(response)
        return [SlotSet('league_name',lig)]


class ActionTeaminfo(Action):
    def name(self):
        return 'action_teaminfo'

    def run(self, dispatcher, tracker, domain):

        import requests as req
        resp = req.get("https://projects.fivethirtyeight.com/soccer-predictions/data.json")
        resp = resp.json()
        lig = tracker.get_slot('team_name')
        #need to find an elegant solution to make a proper league name matching...
        if(lig == "turkish super league"):
            lig = "super-lig"
        elif(lig == "Bundesliga" | lig == 'bundesliga'):
            lig = "bundesliga"
        elif(lig == 'La Liga'):
            lig = 'la-liga'

        leagues = resp["leagues"]
        league = next(item for item in leagues if item["slug"] == lig)
        league_id = league['id']
        forecasts = resp["forecasts"]
        standings = next(item for item in forecasts if item["league_id"] == league_id)
        team_code = standings['teams'][0]['code']
        teams = resp['teams']
        team = next(item for item in teams if item["code"] == team_code)
        response = """The current leader of {} is {}.""".format(lig, team['name'])
        #response = """The current leader of {} is Basaksehir.""".format(lig)
        dispatcher.utter_message(response)
        return [SlotSet('league_name',lig)]
