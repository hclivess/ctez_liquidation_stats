import time
import requests
import json


def qualify(candidates):
    liquidations_list = []
    for c in candidates:
        if c["body"]["network"] == "mainnet" and (c["body"]["destination"]) == "KT1GWnsoFZVHGh7roXEER3qeCcgJgrXT3de2":
            liquidations_list.append(c["body"]["hash"])
    return liquidations_list

    
def parse_search():
    ts = int(time.time())
    url = f"https://api.better-call.dev/v1/search?q=liquidate&s={(ts - 604800)}&i=operation"  # week to date
    parsed = requests.get(url).text
    parsed_json = json.loads(parsed)
    return parsed_json["items"]

def parse_operations(hash_list):
    for operation in hash_list:
        url = f"https://api.better-call.dev/v1/opg/{operation}"
        parsed = requests.get(url).text
        parsed_json = json.loads(parsed)
        print(parsed_json)
        print(parsed_json[0])

if __name__ == "__main__":
    candidates = parse_search()
    hashes = qualify(candidates)
    liquidations = parse_operations(hashes)

    #print(hashes)
