from src.calculator.draftkings.generic import GenericSingleStatisticWeekPredictor
from src.calculator.draftkings.passingTDs import PassingTDsWeekPredictor
from src.scraper.draftkings import DraftKingsRequest

def run():
  passing_yds_data = DraftKingsRequest('PASS_YDS').execute()
  passing_tds_data = DraftKingsRequest('PASS_TDS').execute()

  passing_yds_predictor = GenericSingleStatisticWeekPredictor(passing_yds_data, fantasy_value=0.04)
  passing_tds_predictor = PassingTDsWeekPredictor(passing_tds_data, fantasy_value=4)

  passing_tds_fantasy_points = passing_tds_predictor.get_all_expected_passing_td_fantasy_points()
  passing_yds_fantasy_points = passing_yds_predictor.get_all_expected_fantasy_points()

  test_dict = {}

  for player, value in passing_tds_fantasy_points.items():
    test_dict[player] = value
    if player in passing_yds_fantasy_points:
      test_dict[player] += passing_yds_fantasy_points[player]

    print(f"{player} is predicted to get {test_dict[player]} points from passing statistics this weekend")

if __name__=="__main__":
  run()