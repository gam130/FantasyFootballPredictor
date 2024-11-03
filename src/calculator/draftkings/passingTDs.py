

class PassingTDsWeekPredictor:
    def __init__(self, data, fantasy_value = 4):
        self.data = data
        self.fantasy_value = fantasy_value

    def _parse_qb_passing_tds_json(self, name: str):
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

    def _convert_odds_dict_to_implied_probability(self, oddsDict, atLeast: int = 0, devig: bool = False):
        implied_probabilities = {
            tds: self._convert_to_implied_probability(odds) 
            for tds, odds in oddsDict.items()
        }

        if devig:
            implied_probabilities = self._devig_multiplicative(implied_probabilities)
        
        implied_probabilities[str(atLeast) + '+'] = 1.00  # 100% chance to for at least 0 TDs

        return implied_probabilities

    def _convert_cumulative_to_exact(self, cumulative_probabilities):
        cumulative_probabilities = {int(k[0]): v for k, v in cumulative_probabilities.items()}
        exact_probabilities = {}
        upper_td_range = max(cumulative_probabilities)  # some have 4+ td props, some have only 3
        for i in range(0, upper_td_range):
            exact_probabilities[i] = cumulative_probabilities[i] - cumulative_probabilities[i + 1]

        exact_probabilities[upper_td_range] = cumulative_probabilities[upper_td_range]
        return exact_probabilities

    def _find_expected_value_passing_tds(self, exact_probabilities):
        ev = 0
        for k, v in exact_probabilities.items():
            ev += (k * v)

        return ev

    def _find_expected_fantasy_points_passing_tds(self, statistic_value):
        return statistic_value * self.fantasy_value

    def find_expected_passing_tds(self, name: str, devig: bool = False):
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
        qb_passing_td_odds = self._parse_qb_passing_tds_json(name)
        implied_probabilities = self._convert_odds_dict_to_implied_probability(qb_passing_td_odds, devig=devig)
        exact_qb_td_probabilities = self._convert_cumulative_to_exact(implied_probabilities)
        return self._find_expected_value_passing_tds(exact_qb_td_probabilities)

    def get_all_expected_passing_tds(self, devig: bool = False):
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
        expected_tds = {}
        for s in self.data["selections"]:
            participants = s["participants"]
            for p in participants:
                if p["name"] not in expected_tds:
                    expected_tds[p["name"]] = self.find_expected_passing_tds(p["name"], devig=devig)

        return expected_tds

    def get_all_expected_passing_td_fantasy_points(self, devig: bool = False):
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
        expected_tds = self.get_all_expected_passing_tds(devig=devig)
        expected_fantasy_points = {
            player: self._find_expected_fantasy_points_passing_tds(tds)
            for player, tds in expected_tds.items()
        }
        return expected_fantasy_points
