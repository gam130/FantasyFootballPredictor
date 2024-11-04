from src.calculator.draftkings.GenericSingleStatisticWeekPredictor import GenericSingleStatisticWeekPredictor
from src.calculator.draftkings.GenericCumulativeOddsWeekPredictor import GenericCumulativeOddsWeekPredictor
from src.scraper.draftkings import DraftKingsRequest

def run():
  passing_yds_data = DraftKingsRequest('PASS_YDS').execute()
  passing_tds_data = DraftKingsRequest('PASS_TDS').execute()
  rushing_yds_data = DraftKingsRequest('RUSH_YDS').execute()

  passing_yds_predictor = GenericCumulativeOddsWeekPredictor(passing_yds_data, fantasy_value=0.04)
  passing_tds_predictor = GenericCumulativeOddsWeekPredictor(passing_tds_data, fantasy_value=4)
  rushing_yds_predictor = GenericCumulativeOddsWeekPredictor(rushing_yds_data, fantasy_value=0.1)

  passing_tds_fantasy_points = passing_tds_predictor.get_all_expectations()
  passing_yds_fantasy_points = passing_yds_predictor.get_all_expectations()
  rushing_yds_fantasy_points = rushing_yds_predictor.get_all_expectations()


  test_dict = {}

  # for player, value in passing_tds_fantasy_points.items():
  #   test_dict[player] = value
  #   if player in passing_yds_fantasy_points:
  #     test_dict[player] += passing_yds_fantasy_points[player]

  #   print(f"{player} is predicted to get {test_dict[player]} points from passing statistics this weekend")

  print(f"passing tds: {passing_tds_fantasy_points}")
  print(f"passing yards: {passing_yds_fantasy_points}")
  print(f"rushing yards: {rushing_yds_fantasy_points}")

if __name__=="__main__":
  run()