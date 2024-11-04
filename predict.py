from src.calculator.draftkings.GenericSingleStatisticWeekPredictor import GenericSingleStatisticWeekPredictor
from src.calculator.draftkings.GenericCumulativeOddsWeekPredictor import GenericCumulativeOddsWeekPredictor
from src.scraper.draftkings import DraftKingsRequest

def run():
  passing_yds_data = DraftKingsRequest('PASS_YDS').execute()
  passing_tds_data = DraftKingsRequest('PASS_TDS').execute()
  rushing_yds_data = DraftKingsRequest('RUSH_YDS').execute()
  receiving_yds_data = DraftKingsRequest('REC_YDS').execute()

  passing_yds_predictor = GenericCumulativeOddsWeekPredictor(passing_yds_data, fantasy_value=0.04, statistic='PASS_YDS')
  passing_tds_predictor = GenericCumulativeOddsWeekPredictor(passing_tds_data, fantasy_value=4, statistic='PASS_TDS')
  rushing_yds_predictor = GenericCumulativeOddsWeekPredictor(rushing_yds_data, fantasy_value=0.1, statistic='RUSH_YDS')
  receiving_yds_predictor = GenericCumulativeOddsWeekPredictor(receiving_yds_data, fantasy_value=0.1, statistic='REC_YDS')

  passing_tds = passing_tds_predictor.get_all_expectations()
  passing_yds = passing_yds_predictor.get_all_expectations()
  rushing_yds = rushing_yds_predictor.get_all_expectations()
  receiving_yds = receiving_yds_predictor.get_all_expectations()

  print(f"passing tds: {passing_tds}")
  print(f"passing yards: {passing_yds}")
  print(f"rushing yards: {rushing_yds}")
  print(f"receiving yards: {receiving_yds}")

if __name__=="__main__":
  run()