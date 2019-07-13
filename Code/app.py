import requests
import configparser
# import json


def read_config_file():
    print("Entered config file")
    app_key = ""
    app_id = ""
    language = ""
    config = configparser.ConfigParser()
    try:
        config.read_file(open(r'config/config.ini'))
        app_id = config.get("APP", "APP_ID")
        app_key = config.get("APP", "APP_KEY")
        language = str(config.get("APP", "LANGUAGE"))
        print("Read config file successfully")
    except IOError:
        print("Unable to access config file")
    print("Returning creds: " + app_id, app_key, language)
    return app_id, app_key, language


def get_result(word):
    app_id, app_key, language = read_config_file()

    search_word = word.lower()
    print(search_word)

    try:
        url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + '/' + search_word #+ '/' + "regions=us"
        credentials = {'app_id': app_id, 'app_key': app_key}
        response = requests.get(url, headers=credentials)

        print("code {}\n".format(response.status_code))
        # print("text \n" + response.text)
        # print("json \n" + json.dumps(response.json()))

    except requests.RequestException:
        handle_exception(response.status_code)

    if response.status_code == 200:
        # print("Response in text format: \n" + response.text)
        # print("Response in json format: \n" + json.dumps(response.json()))
        json_result = response.json()
        long_meanings = list(get_definitions(json_result, 'definitions'))
        short_meanings = list(get_definitions(json_result, 'short_definitions'))
        # audioFile = get_definitions(json_result, "audioFile")
        # print(audioFile)
        # print(long_meanings)

        long_definitions = []
        short_definitions = []

        for items in long_meanings:
            for each_item in items:
                if each_item not in long_definitions:
                    long_definitions.append(str(each_item))
                    # print(str(each_item))
        print(long_definitions)

        for items in short_meanings:
            for each_item in items:
                if each_item not in short_definitions:
                    short_definitions.append(str(each_item))
                    # print(str(each_item))
        print(short_definitions)
    elif response.status_code == 404:
        print("Word not found. Please enter another word")
        word = input("Enter the word to be searched: ")
        get_result(word)


def get_definitions(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    definitions = []

    for key, value in search_dict.items():

        if key == field:
            definitions.append(value)

        elif isinstance(value, dict):
            results = get_definitions(value, field)
            for result in results:
                definitions.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_definitions(item, field)
                    for another_result in more_results:
                        definitions.append(another_result)

    return definitions


def handle_exception(status_code):
    if status_code == 200:
        print(""" Success  
                """)
    elif status_code == 400:
        print(""" Bad Request: The request was invalid or cannot be otherwise served. 
                    An accompanying error message will explain further.
                    For example, when the filters provided are unknown, 
                    the source and target languages in the translation endpoint are the same, 
                    or a numeric parameter such as offset and limit in the wordlist 
                    endpoint cannot be evaluated as a number.""")
    elif status_code == 403:
        print(
            "Authentication Failed"
        )
    elif status_code == 404:
        print(
            "Not found"
        )
    elif status_code == 414:
        print(
            "Request URL too long"
        )
    elif status_code == 500:
        print(
            "Internal Server Error."
        )
    elif status_code == 502:
        print(
            "Bad Gateway"
        )
    elif status_code == 503:
        print(
            "Service Unavailable"
        )
    elif status_code == 504:
        print(
            "Gateway Timeout"
        )
    else:
        print("Other Unknown Exception")


if __name__ == '__main__':
    word = input("Enter the word to be searched: ")
    # logger.info("Word Searched: %s", word)
    get_result(word)

# print("code: {}\n".format(response.status_code))
# print("text: \n" + response.text)
# print("json: \n" + json.dumps(response.json()))
