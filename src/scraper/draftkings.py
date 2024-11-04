import requests

# Default request headers
DEFAULT_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8,es;q=0.7",
    "Origin": "https://sportsbook.draftkings.com",
    "Referer": "https://sportsbook-nash.draftkings.com/",
    "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not:A_Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# Endpoints
PASSING_TDS_ENDPOINT = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkuswatl/v1/leagues/88808/categories/1000/subcategories/15987"
PASSING_YDS_ENDPOINT = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkuswatl/v1/leagues/88808/categories/1000/subcategories/14119"
RUSHING_YDS_ENDPOINT = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkuswatl/v1/leagues/88808/categories/1001/subcategories/14118"
RECEIVING_YDS_ENDPOINT = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkuswatl/v1/leagues/88808/categories/1342/subcategories/14117"

# Handles requests for statistics. This is a growing list
# Statistics can be ['PASS_YDS', 'PASS_TDS', 'RUSH_YDS' ...]
class DraftKingsRequest:
    def __init__(self, request):
      self.request = request

    def get_generic_draftkings_request(self, url: str, headers: dict = DEFAULT_HEADERS):
        """
            Sends a GET request to Draftkings with the specified URL and the provided headers.
            
            Args:
                url (str): The API endpoint URL.
                headers (dict): The headers for the request, with a default to mimic a browser request.
            
            Returns:
                dict or str: If successful, returns the response in JSON format. 
                            If unsuccessful, returns a string with the status code of the failure.
        """
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to retrieve data: {response.status_code}"
  
    def get_draftkings_passing_tds(self, headers: dict = DEFAULT_HEADERS):
        """
        Retrieves passing touchdowns data from DraftKings.

        Args:
            headers (dict): Optional. Custom headers for the request, defaults to DEFAULT_HEADERS.

        Returns:
            dict or str: Passing touchdowns data in JSON format if the request is successful,
                        otherwise an error message with the HTTP status code.
        """
        return self.get_generic_draftkings_request(url=PASSING_TDS_ENDPOINT, headers=headers)

    def get_draftkings_passing_yds(self, headers: dict = DEFAULT_HEADERS):
        """
        Retrieves passing yards data from DraftKings.

        Args:
            headers (dict): Optional. Custom headers for the request, defaults to DEFAULT_HEADERS.

        Returns:
            dict or str: Passing touchdowns data in JSON format if the request is successful,
                            otherwise an error message with the HTTP status code.
        """
        return self.get_generic_draftkings_request(url=PASSING_YDS_ENDPOINT, headers=headers)
    
    def get_draftkings_rushing_yds(self, headers: dict = DEFAULT_HEADERS):
        """
        Retrieves rushing yards data from DraftKings.

        Args:
            headers (dict): Optional. Custom headers for the request, defaults to DEFAULT_HEADERS.

        Returns:
            dict or str: Passing touchdowns data in JSON format if the request is successful,
                            otherwise an error message with the HTTP status code.
        """
        return self.get_generic_draftkings_request(url=RUSHING_YDS_ENDPOINT, headers=headers)
    
    def get_draftkings_receiving_yds(self, headers: dict = DEFAULT_HEADERS):
        """
        Retrieves receiving yards data from DraftKings.

        Args:
            headers (dict): Optional. Custom headers for the request, defaults to DEFAULT_HEADERS.

        Returns:
            dict or str: Passing touchdowns data in JSON format if the request is successful,
                            otherwise an error message with the HTTP status code.
        """
        return self.get_generic_draftkings_request(url=RECEIVING_YDS_ENDPOINT, headers=headers)
    
    def execute(self):

        requestHandler = {
            'PASS_TDS' : self.get_draftkings_passing_tds,
            'PASS_YDS' : self.get_draftkings_passing_yds,
            'RUSH_YDS' : self.get_draftkings_rushing_yds,
            'REC_YDS' : self.get_draftkings_receiving_yds,
        }

        if self.request not in requestHandler:
            raise Exception(f"Request {self.request} is not a valid request")
        
        return requestHandler[self.request]()