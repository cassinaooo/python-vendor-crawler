"""This module returns a company URL, given a company name"""

import requests
import config


class URLFinder:

    """
    Uses the azure search API to search for company url given name
    """

    def __init__(self):
        self.subscription_key = config.azure_subscription_key
        self.search_url = "https://api.bing.microsoft.com/v7.0/search"

    def choose_url(self, results_json, url_count=0):
        """
        Extracts the url most likely to be the company website

        :param results_json: output from the API
        :type results_json: dict
        :param url_count: iterative parameter to select url in search results
        :type url_count: int

        :return url string
        """

        excluded_words = ["wikipedia", "linkedin", "bloomberg"]
        url = results_json["webPages"]["value"][url_count]["url"]

        if url_count >= 10:
            url = results_json["webPages"]["value"][0]["url"]
        elif any(substring in url for substring in excluded_words):
            return self.choose_url(results_json, url_count=url_count + 1)

        return url

    def run(self, company):
        """
        Calls the Azure API and returns the url

        :param company: company name
        :type company: str

        :return: most likely company URL
        """

        # access API
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        params = {
            "q": company,
            "textDecorations": True,
            "textFormat": "HTML",
            "mkt": "en-US",
        }
        response = requests.get(
            self.search_url, headers=headers, params=params, timeout=10
        )
        results = response.json()

        # error handling
        if "error" in results:
            raise ValueError(results["error"]["message"])

        # extract url from response
        url = self.choose_url(results_json=results)

        return url
