
# Gets values of a single statistic for all players
class GenericSingleStatisticWeekPredictor:
  def __init__(self, data, fantasy_value):
    self.data = data
    self.fantasy_value = fantasy_value
    self.playerData = {}

    def preprocess():
      selections = self.data["selections"]
      for s in selections:
        participants = s["participants"]

        for p in participants:
          playerName = p["name"]
          if playerName not in self.playerData:
            self.playerData[playerName] = {
              'expectation' : '',
              'under_odds' : '',
              'over_odds' : ''
            }

          self.playerData[playerName]['expectation'] = s["points"]
          outcomeType = s["outcomeType"]
          if outcomeType == "Under": 
            self.playerData[playerName]['under_odds'] = s["displayOdds"]["american"]
          if outcomeType == "Over":
            self.playerData[playerName]['over_odds'] = s["displayOdds"]["american"]

    preprocess()

  def get_all_player_data(self):
    return self.playerData
  
  def get_all_expectations(self):
    return { k:v["expectation"] for k,v in self.playerData.items() }

  def get_player_expectations(self, player: str):
    return self.playerData[player]['expectation']
  
  def get_all_expected_fantasy_points(self):
    return { k:v * self.fantasy_value for k,v in self.get_all_expectations().items() }
