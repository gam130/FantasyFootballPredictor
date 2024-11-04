# Predict statistics that have cumulative lines
#
# This is useful for categories that have separate lines
# that accumulate into each other. This means a player that hits
# for a less likely line is guaranteed to hit for a lower, more-
# likely line
#
# An example of such a line could be pass TDs, where a player could
# have the following odds:
#
# 1+ : -150
# 2+ : +300 
# 3+ : +700
#
# Note how a player that scores 2+ TDs will also hit for the 1+ bet.


# These are statistics where the true value of the statistic is likely 
# to not be one of the exact numbers in the line. Mostly for yardage totals 
# TODO: Figure out what actually should go here, if anything
TRUE_VALUE_UNLIKELY = ['PASS_YDS', 'RUSH_YDS', 'REC_YDS'] 
MIN_ASSUMPTION_FACTOR = 1.0

class GenericCumulativeOddsWeekPredictor:
    def __init__(self, data, fantasy_value, statistic = ''):
        self.data = data
        self.adjust_probs = statistic in TRUE_VALUE_UNLIKELY
        self.fantasy_value = fantasy_value

    def _parse_player_cumulative_odds_json(self, name: str):
        selections = self.data["selections"]
        odds = {}
        for s in selections:
            participants = s["participants"]
            for p in participants:
                if p["name"] == name:
                    label = s["label"]
                    odds[label] = s["displayOdds"]["american"]

        return odds

    def _convert_to_implied_probability(self, odds):
        positive = odds[0] == '+'
        odds = int(odds[1:])
        if positive:
            return 100 / (odds + 100)
        else:
            return odds / (odds + 100)

    def _devig_multiplicative(self, implied_probabilities):
        # TODO: fix this
        total_probability = sum(implied_probabilities.values())
        
        devigged_probabilities = {
            k: v / total_probability 
            for k, v in implied_probabilities.items()
        }
        
        return devigged_probabilities
    
    def _find_assumptions(self, implied_probabilities):
        nums = sorted(implied_probabilities.keys())

        if len(nums) < 2:
            raise Exception("Error: Cumulative line only contains one line")
        
        # Assume that statistic will be over this 100% of time
        min_assumption = nums[0] - (MIN_ASSUMPTION_FACTOR * (nums[1] - nums[0]))

        return min_assumption

    def _adjust_probabiltiies(self, exact_probabilities):
        stat_values = sorted(exact_probabilities.keys())
        for i in range(len(stat_values) - 1):
            new_stat_value = (stat_values[i] + stat_values[i + 1]) / 2
            exact_probabilities[new_stat_value] = exact_probabilities.pop(stat_values[i])

        adjusted_max_stat = stat_values[-1] + ((stat_values[-1] - stat_values[-2]) / 2)
        exact_probabilities[adjusted_max_stat] = exact_probabilities.pop(stat_values[-1])

        return exact_probabilities   

    def _convert_odds_dict_to_implied_probability(self, oddsDict, devig: bool = False):
        implied_probabilities = {
            int(value.replace('+', '')): self._convert_to_implied_probability(odds) 
            for value, odds in oddsDict.items()
        }

        if devig:
            implied_probabilities = self._devig_multiplicative(implied_probabilities)

        # Assume 100% chance to for at least some value, assign only after adjusting lines
        assumed_min = self._find_assumptions(implied_probabilities)

        # Better represent the true expectation at each odd (primarily for yardage lines)
        if self.adjust_probs:
            implied_probabilities = self._adjust_probabiltiies(implied_probabilities)

        # Assigning min from earlier
        implied_probabilities[assumed_min] = 1.00

        return implied_probabilities

    def _convert_cumulative_to_exact(self, cumulative_probabilities):
        exact_probabilities = {}
        cumulative_probabilities_keys = sorted(cumulative_probabilities.keys())
        for i in range(len(cumulative_probabilities_keys) - 1):
            stat_value = cumulative_probabilities_keys[i]
            next_highest_stat_value = cumulative_probabilities_keys[i + 1]
            exact_probabilities[stat_value] = cumulative_probabilities[stat_value] - cumulative_probabilities[next_highest_stat_value]

        upper_range = max(cumulative_probabilities_keys)
        exact_probabilities[upper_range] = cumulative_probabilities[upper_range]        
        return exact_probabilities

    def _find_expected_value(self, exact_probabilities):
        ev = 0
        for k, v in exact_probabilities.items():
            ev += (k * v)

        return ev

    def _find_expected_fantasy_points(self, statistic_value):
        return statistic_value * self.fantasy_value

    def get_player_expectations(self, name: str, devig: bool = False):
        """
        Calculates the expected passing touchdowns for a given player based on provided data.
        
        This function processes the odds data for a specific player, converting it into implied 
        probabilities, then into exact probabilities for each touchdown total. Finally, it calculates 
        the expected value of passing touchdowns.

        Args:
            data (dict): JSON-like dictionary containing the odds and other details for passing touchdowns.
            name (str): The name of the player for whom the expected passing touchdowns are calculated.
            devig (bool): Whether to apply devigging to remove the house edge. Defaults to True.

        Returns:
            float: The expected number of passing touchdowns for the player.
        """
        cumulative_odds = self._parse_player_cumulative_odds_json(name)
        implied_probabilities = self._convert_odds_dict_to_implied_probability(cumulative_odds, devig=devig)
        exact_probabilities = self._convert_cumulative_to_exact(implied_probabilities)
        return self._find_expected_value(exact_probabilities)

    def get_all_expectations(self, devig: bool = False):
        """
        Retrieves the expected passing touchdowns for all players in the provided data.

        This function iterates through each participant in the data, computing the expected passing 
        touchdowns for players who have not yet been processed. Each player's expected touchdowns are 
        stored in a dictionary with the player's name as the key.

        Args:
            data (dict): JSON-like dictionary containing player data, including participants and their stats.
            devig (bool): Whether to apply devigging to remove the house edge. Defaults to True.

        Returns:
            dict: A dictionary where keys are player names and values are their expected passing touchdowns.
        """
        expectations = {}
        for s in self.data["selections"]:
            participants = s["participants"]
            for p in participants:
                if p["name"] not in expectations:
                    expectations[p["name"]] = self.get_player_expectations(p["name"], devig=devig)

        return expectations

    def get_all_expected_fantasy_points(self, devig: bool = False):
        """
        Calculates the expected fantasy points from passing touchdowns for all players in the provided data.

        This function first computes the expected passing touchdowns for each player, then converts these 
        into fantasy points using a predefined fantasy scoring weight. The results are stored in a dictionary 
        where the keys are player names and values are their expected fantasy points.

        Args:
            data (dict): JSON-like dictionary containing player data, including their expected touchdowns.
            devig (bool): Whether to apply devigging to remove the house edge. Defaults to True.

        Returns:
            dict: A dictionary where keys are player names and values are their expected fantasy points from passing touchdowns.
        """
        expectations = self.get_all_expectations(devig=devig)
        expected_fantasy_points = {
            player: self._find_expected_fantasy_points(value)
            for player, value in expectations.items()
        }
        return expected_fantasy_points
