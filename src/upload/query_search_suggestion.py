# Copyright (c) 2024 bilive.

import requests
from src.log.logger import upload_log

def get_bilibili_suggestions(term):
    """use the bilibili search suggestion api to get the most popular search suggestions

    Args:
        term: str,the keyword of the search.
    Returns:
        dict or None: if the request is successful and the response content is in JSON format, return the parsed JSON data (usually a dictionary or list structure),
                      if the request fails, return None
    """
    url = "https://s.search.bilibili.com/main/suggest"
    params = {
        "term": term
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            suggestions = response.json()
            values_list = [item['value'][:20] for item in suggestions['result']['tag']]
            result = ",".join(values_list)
            return result
        upload_log.error(f"Request get_bilibili_suggestions failed with status code: {response.status_code}")
        return None
    except requests.RequestException as e:
        upload_log.error(f"Request get_bilibili_suggestions failed with exception: {e}")
        return None

if __name__ == "__main__":
    suggestions = get_bilibili_suggestions("bilive")
    print(suggestions)
